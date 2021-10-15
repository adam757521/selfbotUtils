from setuptools import setup

f = open("README.md", "r")
README = f.read()

setup(
    name="selfbotUtils",
    packages=["selfbotUtils"],
    package_data={},
    include_package_data=True,
    version="0.0.2",
    license="MIT",
    description="A python module that makes selfbot creation extremely easy, without risking your account being phonebanned!",
    long_description=README,
    long_description_content_type="text/markdown",
    author="adam7100",
    url="https://github.com/adam757521/selfbotUtils",
    download_url="https://github.com/adam757521/selfbotUtils/archive/refs/tags/v0.0.1.tar.gz",
    keywords=[
        "python",
        "sniper",
        "discord",
        "selfbot",
        "discord-py",
        "invite",
        "user-friendly",
        "friendly",
        "discordbots",
    ],
    install_requires=[
        "aiohttp",
        "discord.py",
    ],
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
