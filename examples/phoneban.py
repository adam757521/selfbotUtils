import selfbotUtils
import asyncio


async def main():
    await client.phoneban("working_invite")

    await client.close()


client = selfbotUtils.Client("token")
asyncio.run(main())
