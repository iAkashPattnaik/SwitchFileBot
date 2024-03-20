# FilwSwitchBot - Github
# Copyright (C) 2024 Akash Pattnaik
# This file is a part of < https://github.com/iAkashPattnaik/SwitchFileBot/ >
# PLease read the GNU General Public License v3.0 in <https://www.github.com/iAkashPattnaik/SwitchFileBot/blob/main/LICENSE/>.

# Inbuilt
from os import environ

class Config(object):
    telegramBotToken: str = environ.get('telegramBotToken')
    switchBotToken: str = environ.get('switchBotToken')
    apiId: str = environ.get('apiId')
    apiHash: str = environ.get('apiHash')
    databaseUrl: str = environ.get('databaseUrl')
    switchAdminId: int = int(environ.get('switchAdminId'))
    telegramAdminId: int = int(environ.get('telegramAdminId'))