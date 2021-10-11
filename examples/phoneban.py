import selfbotUtils
import asyncio


async def main():
    await client.run("token")

    await client.phoneban("working_invite")

    await client.close()


client = selfbotUtils.Client()
asyncio.run(main())
