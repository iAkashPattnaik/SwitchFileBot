# FilwSwitchBot - Github
# Copyright (C) 2024 Akash Pattnaik
# This file is a part of < https://github.com/iAkashPattnaik/SwitchFileBot/ >
# PLease read the GNU General Public License v3.0 in <https://www.github.com/iAkashPattnaik/SwitchFileBot/blob/main/LICENSE/>.

# site-packages
import motor.motor_asyncio

# SwitchFileBot
from config import Config

client = motor.motor_asyncio.AsyncIOMotorClient(Config.databaseUrl)