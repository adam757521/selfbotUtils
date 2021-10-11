import selfbotUtils
import asyncio


async def main():
    print(
        await client.redeem_gift("avbc")
    )  # Redeems a discord gift; (Nitro); might raise exceptions.

    await client.close()


client = selfbotUtils.Client("token")
asyncio.run(main())
