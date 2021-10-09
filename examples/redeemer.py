import selfbotUtils
import asyncio


async def main():
    client = selfbotUtils.Client()
    await client.run("token")

    print(
        await client.redeem_gift("avbc")
    )  # Redeems a discord gift; (Nitro); might raise exceptions.

    await client.close()


asyncio.run(main())
