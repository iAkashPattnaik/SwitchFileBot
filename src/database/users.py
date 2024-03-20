# FilwSwitchBot - Github
# Copyright (C) 2024 Akash Pattnaik
# This file is a part of < https://github.com/iAkashPattnaik/SwitchFileBot/ >
# PLease read the GNU General Public License v3.0 in <https://www.github.com/iAkashPattnaik/SwitchFileBot/blob/main/LICENSE/>.

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
class User(Document):
    user_id = fields.IntField(attribute='_id', unique=True)
    platform = fields.StrField(required=True)

    class Meta:
        indexes = ('$user_id', ) # (,) marks a tuple
        collection_name = 'users'

async def new_user(user_id, platform):
    try:
        user = User(
            user_id=user_id,
            platform=platform,
        )
    except ValidationError:
        return False
    else:
        try:
            await user.commit()
        except DuplicateKeyError:      
            return False
        else:
            return True

async def is_user_exist(user_id: int) -> bool:
    user = await User.find_one({ 'user_id': int(user_id) })
    return bool(user)

async def get_user(user_id):
    return await User.find_one({ 'user_id': user_id })

async def get_all_users():
    return db.users.find({})

async def total_users_count() -> dict:
    telegram = await db.users.count_documents({ 'platform': 'TELEGRAM' })
    switch = await db.users.count_documents({ 'platform': 'SWITCH' })
    return { 'total': telegram + switch, 'telegram': telegram, 'switch': switch }

async def get_db_size() -> float:
    return (await client['FileStreamBot'].command("dbstats"))['dataSize']
