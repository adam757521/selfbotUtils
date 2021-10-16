import selfbotUtils
import asyncio


async def main():
    await client.set_hypesquad(selfbotUtils.HypeSquad.BRILLIANCE)
    # await client.set_hypesquad(None)  To leave hypesquad.

    await client.close()


client = selfbotUtils.Client("token")
asyncio.run(main())
