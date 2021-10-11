import selfbotUtils
from selfbotUtils.http import HTTPException
import asyncio


async def main():
    await client.run("token")

    # You can of course fetch these payloads, by using discord client states.
    # discord.Guild(state=discord_client._connection, data=guild)
    # selfbotUtils does not have client states!

    counter = 0
    for guild in await client.get_discoverable_guilds(150):
        try:
            # Please do not join a lot of guilds in a short period of time, your account WILL be phonebanned!
            # There is no way of avoiding this, except proxies.
            # Incase you really want to do this for some reason, you should take breaks between joining guilds.
            # For example, join 10 guilds -> wait an hour, continue, etc...
            # That method will lower the chances of phonebanning, but, still risky.

            # You can fetch the invite using client.get_invite(invite_code).
            await client.join_invite(guild["vanity_url_code"])
            print(f"Joined {guild['name']}")

        except HTTPException as e:
            if e.code == 40002:  # NOT_VERIFIED
                print("We have been phonebanned...")
                break

            if e.code == 30001:  # Maximum number of guilds reached
                print("Joined 100 guilds...")
                break

            print("ignoring", guild["vanity_url_code"], "error while joining")

        counter += 1

        if counter % 10 == 0:
            print("Joined 10 guilds, sleeping for an hour.")
            await asyncio.sleep(60 * 60)

    # Another good way of joining a lot of guilds is making an "invite sniper", pretty similar to a nitro sniper,
    # but instead of sniping gifts, it snipes invites. (you will still need to make a cooldown/sleep system, of course)

    await client.close()


client = selfbotUtils.Client()
asyncio.run(main())
