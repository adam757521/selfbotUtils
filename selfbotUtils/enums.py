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

from enum import Enum

__all__ = ("NitroServerResponse",)


class NitroServerResponse(Enum):
    INVALID_GIFT = 1
    ALREADY_CLAIMED = 2
    NO_PAYMENT_SOURCE = 3
    ALREADY_PURCHASED = 4
    NOT_VERIFIED = 5
    CLAIMED = 6
    UNKNOWN = 7

    @classmethod
    def from_response(cls, response: dict) -> NitroServerResponse:
        """
        Returns the server response from the response dict.

        :param dict response: The server response.
        :return: The nitro server response type.
        :rtype: NitroServerResponse
        """

        error_codes = {
            10038: cls.INVALID_GIFT,
            50050: cls.ALREADY_CLAIMED,
            50070: cls.NO_PAYMENT_SOURCE,
            100011: cls.ALREADY_PURCHASED,
            40002: cls.NOT_VERIFIED,
        }

        for error_code, error_response in error_codes.items():
            if response.get("code") == error_code:
                return error_response

        if response.get("subscription_plan"):
            return cls.CLAIMED

        return cls.UNKNOWN
