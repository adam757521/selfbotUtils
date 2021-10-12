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

from __future__ import annotations

import asyncio
from typing import Optional, List

import discord
import discord.state

from .exceptions import InvalidLimit
from .http import HTTPClient, HTTPException, json_or_text
from .nitro import NitroResponse

__all__ = ("Client",)


class Client:
    """
    Represents a selfbot client.
    """

    __slots__ = ("loop", "http", "state")

    def __init__(
        self,
        token: str,
        loop: asyncio.AbstractEventLoop = None,
        state: discord.state.ConnectionState = None,
    ) -> None:
        self.loop = loop or asyncio.get_event_loop()
        self.state = state
        self.http = HTTPClient(token)

    async def close(self) -> None:
        """
        |coro|

        Closes the client.

        :return: None
        :rtype: None
        """

        await self.http.close()

    async def phoneban(self, invite_code: str) -> None:
        """
        |coro|

        Phone bans the account.
        CAUTION: This method is dangerous and will flag/lock the account permanently.

        :param str invite_code: The working invite code.
        :return: None
        :rtype: None
        """

        await self.http.phone_ban_account(invite_code)

    async def accept_membership_screening(self, guild_id: int) -> None:
        """
        |coro|

        Accepts the membership screening.

        :param int guild_id: The guild id.
        :return: None
        :rtype: None
        """

        await self.http.accept_membership_screening(guild_id)

    async def get_discoverable_guilds(self, limit: int = 48) -> List[dict]:
        """
        |coro|

        Returns the discoverable guilds.

        :param int limit: The fetch limit.
        :return: The discoverable guilds.
        :rtype: List[dict]
        """

        if limit < 0:
            raise InvalidLimit(f"Limit {limit} is invalid.")

        if limit <= 48:
            return (await self.http.get_discoverable_guilds(0, limit))["guilds"]

        initial_fetch = await self.http.get_discoverable_guilds(0, 48)
        total_guilds = initial_fetch["total"]

        guilds = []
        fetches = list(
            await asyncio.gather(
                *[
                    self.http.get_discoverable_guilds(offset, min(limit - offset, 48))
                    for offset in range(48, min(limit, total_guilds), 48)
                ]
            )
        )

        fetches.insert(0, initial_fetch)

        for fetch in fetches:
            guilds += fetch.get("guilds")

        return guilds

    async def get_invite(self, invite_code: str) -> Optional[discord.Invite]:
        """
        |coro|

        Gets the invite information.

        :param str invite_code: The invite code.
        :return: The invite information.
        :rtype: discord.Invite
        """

        try:
            return discord.Invite(
                state=self.state, data=await self.http.get_invite(invite_code)
            )
        except AttributeError:
            return

    async def join_invite(
        self, invite_code: str, accept_membership_screening: bool = False
    ) -> Optional[discord.Invite]:
        """
        |coro|

        Joins an invite.

        :param bool accept_membership_screening:
            Indicating if the join should accept the membership screening automatically.
        :param str invite_code: The invite code.
        :return: The invite information.
        :rtype: discord.Invite
        """

        try:
            invite_data = await self.http.join_invite(invite_code)

            if accept_membership_screening:
                await self.accept_membership_screening(invite_data["guild"]["id"])

            return discord.Invite(state=self.state, data=invite_data)
        except AttributeError:
            return

    async def send_friend_request(self, tag: str) -> dict:
        """
        |coro|

        Sends a friend request to the user.

        :param str tag: The user tag (username#discriminator)
        :return: The server response.
        :rtype: dict
        """

        return await self.http.send_friend_request(*tag.split('#')[:2])

    async def redeem_gift(
        self, gift_code: str, payment_source_id: int = None
    ) -> NitroResponse:
        """
        |coro|

        Redeems a gift code.

        :param str gift_code: The gift code.
        :param int payment_source_id: The payment source id.
        :return: The nitro response.
        :rtype: NitroResponse
        """

        try:
            response = await self.http.redeem_code(gift_code, payment_source_id)
        except HTTPException as e:
            response = await json_or_text(e.response)

        return NitroResponse.from_response(response)
