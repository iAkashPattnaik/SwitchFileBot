# FilwSwitchBot - Github
# Copyright (C) 2024 Akash Pattnaik
# This file is a part of < https://github.com/iAkashPattnaik/SwitchFileBot/ >
# PLease read the GNU General Public License v3.0 in <https://www.github.com/iAkashPattnaik/SwitchFileBot/blob/main/LICENSE/>.

# Inbuilt
from time import time

# site-packages
from pymongo.errors import DuplicateKeyError
from marshmallow.exceptions import ValidationError
from umongo import Instance, Document, fields

# SwitchFileBot
from . import client

# Database name - SwitchFileBot
db = client['SwitchFileBot']
instance = Instance.from_db(db)

@instance.register
class Files(Document):
    file_id = fields.StrField(attribute='_id', unique=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=False)
    file_type = fields.StrField(allow_none=False)
    platform = fields.StrField(allow_none=False)
    download_link = fields.StrField(allow_none=True)
    start_time = fields.IntField(allow_none=False)
    fetch_id = fields.StrField(allow_none=False, unique=True)

    class Meta:
        indexes = ('$file_name', ) # (,) marks a tuple
        collection_name = 'files'

async def save_file(file, platform):
    try:
        file = Files(
            file_id=file.file_id,
            file_name=file.file_name,
            file_size=file.file_size,
            file_type=file.file_type,
            start_time=file.start_time,
            fetch_id=file.fetch_id,
            download_link=file.download_link,
            platform=platform,
        )
    except ValidationError:
        return False
    else:
        try:
            await file.commit()
        except DuplicateKeyError:  
            return False
        else:
            return True

async def get_file_details(fetch_id):
    filter = { 'fetch_id': fetch_id }
    cursor = Files.find(filter)
    filedetails = await cursor.to_list(length=1)
    return filedetails

async def total_files_count():
    count = await db.files.count_documents({})
    return count

async def remove_expired_files():
    files = await (db.files.find({})).to_list(await total_files_count())
    for i in files:
        if (time() - i['start_time']) >= 60 * 60 * 24:
            await db.files.delete_one({ 'fetch_id': i['fetch_id']})
