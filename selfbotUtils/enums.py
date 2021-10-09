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
