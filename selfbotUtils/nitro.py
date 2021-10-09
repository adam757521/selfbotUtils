from __future__ import annotations

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

    @classmethod
    def from_response(cls, response: dict) -> NitroResponse:
        """
        Creates a NitroResponse object from the response dict.

        :param dict response: The response dict.
        :return: The nitro response.
        :rtype: NitroResponse
        """

        return cls(NitroServerResponse.from_response(response), response)
