import selfbotUtils
import asyncio


async def main():
    await client.run("token")

    print(repr(await client.http.get_invite("invite_code")))

    print(
        await client.join_invite("invite_code")
    )  # Joins an invite without phonebanning.

    await client.close()


client = selfbotUtils.Client()
asyncio.run(main())
