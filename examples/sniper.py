from typing import List

import discord
import selfbotUtils
import re


client = discord.Client()  # Used a client, because we do not need any commands.
LINKS = ('discord.gift', 'discordapp.com/gifts', 'discord.com/gifts')
GIFT_RE = re.compile(fr'({"|".join(LINKS)})/\w{{16,24}}')


def remove_links(text: str) -> str:
    for link in LINKS:
        text = text.replace(link + '/', '')

    return text


def find_codes(text: str) -> List[str]:
    codes = []

    for match in GIFT_RE.finditer(text):
        current_code = match.group(0)

        codes.append(remove_links(current_code))

    return codes


@client.event
async def on_ready():
    await client.selfbot.run(token)
    print("Sniper is ready.")


@client.event
async def on_message(message):
    # The on_message event wont be called when using discord.py, because discord has blocked selfbots.
    # I recommend using discord.py-self, to unblock it.

    if not client.selfbot.http:
        return  # Client has not been initialized yet.

    codes = find_codes(message.content)
    for code in codes:
        # I do not recommend redeeming every nitro code you receive, for example, you can save codes in cache to not
        # redeem them twice, block specific users if they send too many codes, etc...

        code_status = await client.selfbot.redeem_gift(code)

        print(code, message.author, code_status)
        if code_status.server_response == selfbotUtils.NitroServerResponse.CLAIMED:
            print(f"Claimed {code_status.nitro_type}")


# If you are using discord.py-self, make sure you remove the bot argument!
token = "token"
client.selfbot = selfbotUtils.Client(state=client._connection)
# You should always pass the state, if you are sure you will use a discord client.
# Passing the client connection state helps in the guild/invite fetching progress.

client.run(token)
