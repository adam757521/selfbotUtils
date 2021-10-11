import selfbotUtils
import asyncio


async def main():
    await client.join_invite("invite_code", accept_membership_screening=True)

    await client.accept_membership_screening("snowflake")

    await client.close()


client = selfbotUtils.Client("token")
asyncio.run(main())
