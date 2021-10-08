import logging

import selfbotUtils
import asyncio


async def main():
    client = selfbotUtils.HTTPClient(
        "ODk2MDMzMDIxOTg2MjM4NTA0.YWBOBw.i2fR9LV5mMGXJbSRjBfxC8pL0vc"
    )

    await client.get_invite("abc")  # Gets an invite.
    # print(repr(discord.Invite(state=None, data=invite)))

    await client.join_invite("abc")  # Joins a guild.
    await client.redeem_code("ABCD")  # Redeems a discord gift; (Nitro)

    await client.close()


asyncio.run(main())
