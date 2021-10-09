from __future__ import annotations

import asyncio

from discord import LoginFailure

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
                raise LoginFailure("Improper token has been passed.")

            raise

    async def close(self) -> None:
        """
        |coro|

        Closes the client.

        :return: None
        :rtype: None
        """

        await self.http.close()

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
