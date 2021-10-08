import json
import datetime
import re


def get_ratelimit_time(request, use_clock=False):
    reset_after = request.headers.get("X-Ratelimit-Reset-After")

    if use_clock or not reset_after:
        utc = datetime.timezone.utc
        now = datetime.datetime.now(utc)
        reset = datetime.datetime.fromtimestamp(
            float(request.headers["X-Ratelimit-Reset"]), utc
        )

        return (reset - now).total_seconds()

    return float(reset_after)


async def get_build_number(session):
    login_page_request = await session.request(
        "GET",
        "https://discord.com/login",
        headers={"Accept-Encoding": "gzip, deflate"},
        timeout=10,
    )
    login_page = await login_page_request.text()
    build_url = (
        "https://discord.com/assets/"
        + re.compile(r"assets/+([a-z0-9]+)\.js").findall(login_page)[-2]
        + ".js"
    )
    build_request = await session.request(
        "GET", build_url, headers={"Accept-Encoding": "gzip, deflate"}, timeout=10
    )
    build_file = await build_request.text()
    build_index = build_file.find("buildNumber") + 14
    return int(build_file[build_index : build_index + 5])


async def get_user_agent(session, default: bool = False):
    default_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"

    try:
        if default:
            return default_user_agent

        request = await session.request(
            "GET", "https://jnrbsn.github.io/user-agents/user-agents.json", timeout=10
        )
        response = json.loads(await request.text())
        return response[0]
    except IndexError:
        return default_user_agent


async def get_browser_version(session, default: bool = False):
    default_version = "91.0.4472.77"
    if default:
        return default_version

    request = await session.request(
        "GET", "https://omahaproxy.appspot.com/all.json", timeout=10
    )
    response = json.loads(await request.text())
    if response[0]["versions"][4]["channel"] == "stable":
        return response[0]["versions"][4]["version"]

    return default_version
