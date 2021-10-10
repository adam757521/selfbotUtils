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
from typing import Optional

import discord

from .http import HTTPClient, HTTPException, json_or_text
from .nitro import NitroResponse

__all__ = ("Client",)


class Client:
    """
    Represents a selfbot client.
    """

    __slots__ = ("loop", "http")

    def __init__(self, loop: asyncio.AbstractEventLoop = None) -> None:
        self.loop = loop or asyncio.get_event_loop()
        self.http = None

    async def run(self, token: str) -> None:
        """
        |coro|

        Runs the bot with the token.

        :param str token: The token.
        :return: None
        :rtype: None
        """

        self.http = HTTPClient(token)

        try:
            await self.http.get_me()
        except HTTPException as e:
            await self.http.close()

            if e.status == 401:
                raise discord.LoginFailure("Improper token has been passed.")

            raise

    async def close(self) -> None:
        """
        |coro|

        Closes the client.

        :return: None
        :rtype: None
        """

        await self.http.close()

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
                state=None, data=await self.http.get_invite(invite_code)
            )
        except AttributeError:
            return

    async def join_invite(self, invite_code: str) -> Optional[discord.Invite]:
        """
        |coro|

        Joins an invite.

        :param str invite_code: The invite code.
        :return: The invite information.
        :rtype: discord.Invite
        """

        try:
            return discord.Invite(
                state=None, data=await self.http.join_invite(invite_code)
            )
        except AttributeError:
            return

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
