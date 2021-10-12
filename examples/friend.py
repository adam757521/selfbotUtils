import selfbotUtils
import asyncio


async def main():
    await client.send_friend_request("username#discriminator")

    await client.close()


client = selfbotUtils.Client("token")
asyncio.run(main())
