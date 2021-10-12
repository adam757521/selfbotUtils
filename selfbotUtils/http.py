"""
MIT License

Copyright (c) 2021-present adam7100

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncio
import json
import logging
from base64 import b64encode
from typing import Union, Optional

import discord
from discord.errors import HTTPException, Forbidden, NotFound, DiscordServerError
from discord.http import json_or_text

import aiohttp

from selfbotUtils import utils

log = logging.getLogger(__name__)


class HTTPClient:
    """
    Represents an HTTP client that mimics users accessing the Discord API that avoids phonebans.
    """

    BASE = "https://discord.com/api/v9"

    def __init__(self, token, connector=None, use_default_values: bool = False):
        self.use_default_values = use_default_values
        self.connector = connector
        self._initialized = False
        self.session = None

        self.token = token

    async def _initialize(self) -> None:
        if not self.session:
            self.session = aiohttp.ClientSession(connector=self.connector)

        if self._initialized:
            return

        self.user_agent = ua = await utils.get_user_agent(
            self.session, self.use_default_values
        )
        self.client_build_number = bn = await utils.get_build_number(self.session)
        self.browser_version = bv = await utils.get_browser_version(
            self.session, self.use_default_values
        )
        self.super_properties = super_properties = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "browser_user_agent": ua,
            "browser_version": bv,
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "system_locale": "en-US",
            "client_build_number": bn,
            "client_event_source": None,
        }
        self.encoded_super_properties = b64encode(
            json.dumps(super_properties).encode()
        ).decode("utf-8")

    def _create_request_arguments(self, kwargs: dict) -> dict:
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Origin": "https://discord.com",
            "Pragma": "no-cache",
            "Referer": "https://discord.com/",
            "Sec-CH-UA": '"Google Chrome";v="{0}", "Chromium";v="{0}", ";Not A Brand";v="99"'.format(
                self.browser_version.split(".")[0]
            ),
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": self.user_agent,
            "X-Super-Properties": self.encoded_super_properties,
        }

        if kwargs.pop("auth", False):
            headers["Authorization"] = self.token or "undefined"

        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs["data"] = json.dumps(
                kwargs.pop("json"), separators=(",", ":"), ensure_ascii=True
            )

        kwargs["headers"] = headers

        return kwargs

    async def _handle_server_response(self, r, response, current_tries):
        # Check if we have rate limit information
        remaining = r.headers.get("X-Ratelimit-Remaining")
        if remaining == "0" and r.status != 429:
            delta = utils.get_ratelimit_time(r)
            log.debug("Auth ratelimit has been hit (retry: %s).", delta)
            await asyncio.sleep(delta)

        # Rate limited
        if r.status == 429:
            if not r.headers.get("Via"):
                # Banned by Cloudflare more than likely
                raise HTTPException(r, response)

            retry_after = response["retry_after"] / 1000.0
            log.warning(
                'We are being rate limited. Retrying in %.2f seconds. Handled under the bucket "None"',
                retry_after,
            )
            await asyncio.sleep(retry_after)
            return

        # Unconditional retry
        if r.status in {500, 502}:
            await asyncio.sleep(1 + current_tries * 2)
            return

        # Usual error cases
        if r.status == 401:
            await self.close()
            raise discord.LoginFailure("An improper token has been passed")

        if r.status == 403:
            raise Forbidden(r, response)

        if r.status == 404:
            raise NotFound(r, response)

        if r.status == 503:
            raise DiscordServerError(r, response)

        raise HTTPException(r, response)

    async def request(
        self, method: str, url: str, replace_headers: bool = True, **kwargs
    ) -> Union[dict, str]:
        """
        |coro|

        Sends a request to the url.

        :param bool replace_headers: A bool indicating if it should replace the headers to simulate users.
        :param str method: The request method.
        :param str url: The request url.
        :param kwargs: The key arguments to overwrite.
        :return: The request response.
        :rtype: Union[dict, str]
        """

        await self._initialize()

        url = self.BASE + url

        request_arguments = (
            kwargs if not replace_headers else self._create_request_arguments(kwargs)
        )

        for tries in range(5):
            try:
                async with self.session.request(method, url, **request_arguments) as r:
                    log.debug(
                        "%s %s with %s has returned %s",
                        method,
                        url,
                        request_arguments.get("data"),
                        r.status,
                    )

                    data = await json_or_text(r)

                    # Request was successful so just return the text/json
                    if 300 > r.status >= 200:
                        log.debug("%s %s has received %s", method, url, data)
                        return data

                    await self._handle_server_response(r, data, tries)

            # This is handling exceptions from the request
            except OSError as e:
                # Connection reset by peer
                if tries < 4 and e.errno in (54, 10054):
                    continue
                raise

            # We've run out of retries, raise
        if r.status >= 500:
            raise DiscordServerError(r, data)

        raise HTTPException(r, data)

    async def close(self) -> None:
        """
        |coro|

        Closes the session.

        :return: None
        :rtype: None
        """

        if self.session:
            await self.session.close()

    async def send_friend_request(self, username: str, discriminator: int) -> dict:
        """
        |coro|

        Sends a friend request to the user.

        :param str username: The username.
        :param int discriminator: The discriminator.
        :return: The server response.
        :rtype: dict
        """

        return await self.request(
            "POST",
            "/users/@me/relationships",
            json={
                "username": username,
                "discriminator": discriminator
            },
            auth=True
        )

    async def join_invite(self, invite_code: str) -> dict:
        """
        |coro|

        Joins an invite.

        :param str invite_code: The invite code.
        :return: The guild information.
        :rtype: dict
        """

        return await self.request(
            "POST",
            f"/invites/{invite_code}",
            json={},
            auth=True,
        )

    async def accept_membership_screening(self, guild_id: int) -> None:
        """
        |coro|

        Accepts the membership screening in the guild.

        :param int guild_id: The guild id.
        :return: None
        :rtype: None
        """

        screening_fields = await self.request(
            "GET", f"/guilds/{guild_id}/member-verification?with_guild=false", auth=True
        )

        screening_fields.pop("description")  # Not needed in payload.
        screening_fields["form_fields"][0]["response"] = True

        await self.request(
            "PUT", f"/guilds/{guild_id}/requests/@me", auth=True, json=screening_fields
        )

    async def phone_ban_account(self, invite_code: str) -> None:
        """
        |coro|

        Phone bans the account.

        :param str invite_code: A working invite code to phoneban the account with.
        :return: None
        :rtype: None
        """

        headers = {"Authorization": self.token}

        await self.request(
            "POST",
            f"/invites/{invite_code}",
            replace_headers=False,
            json={},
            headers=headers,
        )

    async def get_invite(self, invite_code: str) -> dict:
        """
        |coro|

        Gets the invite information.

        :param str invite_code: The invite code.
        :return: The invite information.
        :rtype: dict
        """

        return await self.request(
            "GET",
            f"/invites/{invite_code}?inputValue={invite_code}&with_counts=true&with_expiration=true",
        )

    async def get_discoverable_guilds(self, offset: int = 0, limit: int = 48) -> dict:
        """
        |coro|

        Returns the discoverable guilds.

        :param int offset: The offset.
        :param int limit: The fetch limit, max is 48.
        :return: The fetch data.
        :rtype: dict
        """

        return await self.request(
            "GET", f"/discoverable-guilds?offset={offset}&limit={limit}", auth=True
        )

    async def get_me(self) -> dict:
        """
        |coro|

        Returns the token information.

        :return: The token information.
        :rtype: dict
        """

        return await self.request("GET", "/users/@me", auth=True)

    async def redeem_code(
        self, gift_code: str, payment_source_id: Optional[Union[str, int]] = None
    ) -> dict:
        """
        |coro|

        Redeems a code.

        :param str gift_code: The code to redeem.
        :param Union[str, int] payment_source_id: The payment source id, used when redeeming 3 month codes.
        :return: The code information.
        :rtype: dict
        """

        return await self.request(
            "POST",
            f"/entitlements/gift-codes/{gift_code}/redeem",
            json={
                "channel_id": None,
                "payment_source_id": payment_source_id,
            },
            auth=True,
        )
