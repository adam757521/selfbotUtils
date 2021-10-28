import selfbotUtils
import asyncio


async def main():
    await client.leave_guild("snowflake")

    await client.close()


client = selfbotUtils.Client("token")
asyncio.run(main())
