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

from typing import Optional

from .enums import NitroServerResponse

__all__ = ("NitroResponse",)


class NitroResponse:
    """
    Represents a Nitro response.
    """

    __slots__ = ("server_response", "raw")

    def __init__(
        self, server_response: NitroServerResponse, raw_response: dict
    ) -> None:
        self.server_response = server_response
        self.raw = raw_response

    def __str__(self):
        return f"<{self.__class__.__name__} response={self.server_response}>"

    @property
    def nitro_type(self) -> Optional[str]:
        """
        Returns the nitro type of the claim, if applicable.

        :return: The nitro type, if applicable.
        :rtype: Optional[str]
        """

        if self.server_response != NitroServerResponse.CLAIMED:
            return

        return self.raw["subscription_plan"]["name"]

    @classmethod
    def from_response(cls, response: dict) -> NitroResponse:
        """
        Creates a NitroResponse object from the response dict.

        :param dict response: The response dict.
        :return: The nitro response.
        :rtype: NitroResponse
        """

        return cls(NitroServerResponse.from_response(response), response)
