# FilwSwitchBot - Github
# Copyright (C) 2024 Akash Pattnaik
# This file is a part of < https://github.com/iAkashPattnaik/SwitchFileBot/ >
# PLease read the GNU General Public License v3.0 in <https://www.github.com/iAkashPattnaik/SwitchFileBot/blob/main/LICENSE/>.

# Inbuilt
import asyncio

# site-packages
from pyrogram import idle
import dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Load the [.env] data before importing the Config!
dotenv.load_dotenv()

# SwitchFileBot
from src.telegram_bot.main import app as telegram_bot
from src.switch_bot.main import app as switch_bot
from src.database import files

loop = asyncio.get_event_loop()

async def runTelegramBot():
    await telegram_bot.start()
    await idle()

async def runSwitchBot():
    await switch_bot.start()
    # swibots lib performs the idle() task by default

async def start_services():
    await asyncio.gather(
        runTelegramBot(),
        runSwitchBot(),
    )

async def stop_services():
    await telegram_bot.stop()
    await switch_bot.stop()

if __name__ == "__main__":
    print("Starting ...")
    try:
        scheduler = AsyncIOScheduler()
        scheduler.add_job(files.remove_expired_files, 'interval', seconds=60 * 60) # Check every hour
        scheduler.start()
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        exit()
    finally:
        loop.run_until_complete(stop_services())
        loop.stop()
