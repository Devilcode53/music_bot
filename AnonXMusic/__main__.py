import asyncio
import importlib
import os

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from AnonXMusic import LOGGER, app, userbot
from AnonXMusic.core.call import Anony
from AnonXMusic.misc import sudo
from AnonXMusic.plugins import ALL_MODULES
from AnonXMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# Ensure Node.js is available
def check_node():
    if os.system("node --version") != 0:
        LOGGER(__name__).error("❌ Node.js is not installed. Please install it before running the bot.")
        exit(1)

check_node()  # Run check at startup


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("❌ Assistant client variables not defined. Exiting...")
        exit(1)

    await sudo()

    try:
        users = await get_gbanned()
        BANNED_USERS.update(users)
        users = await get_banned_users()
        BANNED_USERS.update(users)
    except:
        pass

    await app.start()
    
    for module in ALL_MODULES:
        importlib.import_module("AnonXMusic.plugins" + module)

    LOGGER("AnonXMusic.plugins").info("✅ Successfully imported modules.")
    
    await userbot.start()
    await Anony.start()

    try:
        await Anony.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("AnonXMusic").error("❌ Please turn on the video chat of your log group/channel.\n\nStopping Bot...")
        exit(1)
    except Exception as e:
        LOGGER("AnonXMusic").error(f"⚠️ Error starting stream: {e}")

    await Anony.decorators()

    LOGGER("AnonXMusic").info("🎵 AnonX Music Bot Started Successfully! 🎵")

    await idle()

    await app.stop()
    await userbot.stop()
    LOGGER("AnonXMusic").info("🛑 Stopping AnonX Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
