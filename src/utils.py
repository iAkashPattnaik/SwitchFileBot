# FilwSwitchBot - Github
# Copyright (C) 2024 Akash Pattnaik
# This file is a part of < https://github.com/iAkashPattnaik/SwitchFileBot/ >
# PLease read the GNU General Public License v3.0 in <https://www.github.com/iAkashPattnaik/SwitchFileBot/blob/main/LICENSE/>.

# Inbuilt
import datetime
from time import time
from os import path, makedirs

# site-packages
import psutil
from requests import get
from swibots import BotApp

class FileObject(object):
    file_name = None
    file_id = None
    file_name = None
    file_size = None
    file_type = None
    platform = None
    start_time = None
    fetch_id = None
    download_link = None

class SwitchBot(BotApp):
    async def download_media(self, media: FileObject):
        if not path.exists('./downloads'):
            makedirs('./downloads')
        with open(f'downloads/{media.file_name}', 'wb') as file:
            data = get(media.download_link)
            file.write(data.content)
            file.flush()
            file.close()
        return path.abspath(f'./downloads/{media.file_name}')

def get_size(size):
    """
    Get size in readable format
    """

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def get_time_left(start_time):
    return datetime.timedelta(seconds=start_time + (60 * 60 * 24) - int(time()))

def uptime():
    return datetime.timedelta(seconds=int(time()) - psutil.boot_time())

def get_registered_time(start_time):
    return datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')