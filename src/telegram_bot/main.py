# FilwSwitchBot - Github
# Copyright (C) 2024 Akash Pattnaik
# This file is a part of < https://github.com/iAkashPattnaik/SwitchFileBot/ >
# PLease read the GNU General Public License v3.0 in <https://www.github.com/iAkashPattnaik/SwitchFileBot/blob/main/LICENSE/>.

# Inbuilt
import time
import uuid
from os import remove

# site-packages
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from pyrogram.enums import ParseMode
from pyrogram import Client

# SwitchFileBot
from src.database import users, files
from src import utils
from config import Config

app = Client(
    'FileShareBot',
    api_id=Config.apiId,
    api_hash=Config.apiHash,
    bot_token=Config.telegramBotToken,
)
switchBotApp = utils.SwitchBot(Config.switchBotToken, 'Telegram to Switch FileShareBot!')

import logging  # noqa: E402

logging.basicConfig(level=logging.WARNING)

async def checkUserJoinStatus(user_id):
    try:
        channel = await app.get_chat_member("TrashProjects", user_id)
    except Exception as _:
        channel = False
    if channel:
        return True
    return False

def callback_filter(data: list):
    async def func(flt, _, query):
        return query.data in flt.data
    return filters.create(func, data=data)

@app.on_message(filters.command("start"))
async def start_command(_, message: Message):
    if not (await users.is_user_exist(message.from_user.id)):
        await users.new_user(message.from_user.id, 'TELEGRAM')
    await message.reply(
        'Hello and welcome to **SwitchFileBot**\n'
        '\n'
        'Here you can send me files and generate a 24 hour valid token! Use this token to retreive the file in **switch** or **telegram**',
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton('🔥 Channel', url='https://t.me/TrashProjects'),
            ],
            [
                InlineKeyboardButton('💰 Donate', callback_data='donate'),
                InlineKeyboardButton('📺 Switch Bot', url='https://myswitch.click/ELHC'),
            ],
            [
                InlineKeyboardButton('🧑‍💻 Source Code', url='https://github.com/iAkashPattnaik/SwitchFileBot'),
            ]
        ])
    )

@app.on_message(filters.command("fetch"))
async def fetch_command(_, message: Message):
    if not (await users.is_user_exist(message.from_user.id)):
        await users.new_user(message.from_user.id, 'TELEGRAM')
    file = await files.get_file_details(message.command[-1])
    if len(file) == 0:
        return await message.reply('❌ Invalid Fetch ID')
    file: utils.FileObject = file[0]
    if file.platform == 'SWITCH': # If file was registered on switch
        infoMssage = await message.reply(
            f'📩 Donwloading File from **{file.platform}**',
            parse_mode=ParseMode.MARKDOWN,
        )
        file_path = await switchBotApp.download_media(media=file)
        await infoMssage.edit_text(
            '⬆️ Uploading File to **Switch**',
            parse_mode=ParseMode.MARKDOWN,
        )
        sender = app.send_document
        if 'image' in file.file_type:
            sender = app.send_photo
        elif 'video' in file.file_type:
            sender = app.send_video
        elif 'audio' in file.file_type:
            sender = app.send_audio
        await sender(
            message.chat.id,
            file_path,
            caption=f'**File Name**: `{file.file_name}`\n'
            f'**File Size**: `{utils.get_size(file.file_size)}`\n'
            f'**Fetch ID**: `{file.fetch_id}`\n'
            f'**Register Time**: `{utils.get_registered_time(file.start_time)}`\n'
            f'**Register Platform**: `{file.platform}`\n'
            f'**Time Left**: `{utils.get_time_left(file.start_time)}`',
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=message.id,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('🔥 Channel', url='https://t.me/TrashProjects')],
                [InlineKeyboardButton('📺 Switch Bot', url='https://myswitch.click/ELHC')],
            ])
        )
        await infoMssage.delete()
        remove(file_path)
        return True
    # For telegram registred files
    await message.reply_cached_media(
        file.file_id,
        caption=f'**File Name**: `{file.file_name}`\n'
        f'**File Size**: `{utils.get_size(file.file_size)}`\n'
        f'**Fetch ID**: `{file.fetch_id}`\n'
        f'**Register Time**: `{utils.get_registered_time(file.start_time)}`\n'
        f'**Register Platform**: `{file.platform}`\n'
        f'**Time Left**: `{utils.get_time_left(file.start_time)}`',
        parse_mode=ParseMode.MARKDOWN,
        reply_to_message_id=message.id,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('🔥 Channel', url='https://t.me/TrashProjects')],
            [InlineKeyboardButton('📺 Switch Bot', url='https://myswitch.click/ELHC')],
        ])
    )

@app.on_message(filters.command('stats'))
async def stats_command(_, message: Message):
    if not (await users.is_user_exist(message.from_user.id)):
        await users.new_user(message.from_user.id, 'TELEGRAM')
    _users = await users.total_users_count()
    _files = await files.total_files_count()
    await message.reply(
        '**Bot Stats**\n'
        '\n'
        f'**Total users**: `{_users["total"]}`\n'
        f'**Telegram users**: `{_users["telegram"]}`\n'
        f'**Switch users**: `{_users["switch"]}`\n'
        f'**Current Registred Files**: `{_files}`\n'
        f'**System Uptime**: `{utils.uptime()}`',
        parse_mode=ParseMode.MARKDOWN,
    )

@app.on_message(filters.command('cast'))
async def cast_command(_, message: Message):
    if not (await users.is_user_exist(message.from_user.id)):
        await users.new_user(message.from_user.id, 'TELEGRAM')
    if message.from_user.id != Config.telegramAdminId:
        return await message.reply('You don\'t have access to use this command!')
    total = await users.total_users_count()
    _users = await (await users.get_all_users()).to_list(total['total'])
    blocked = { 'switch': 0, 'telegram': 0 }
    for user in _users:
        if user['platform'] == 'TELEGRAM':
            try:
                await app.send_message(user['_id'], message.text.partition('/cast')[-1])
            except Exception as _:
                blocked['telegram'] += 1
        else:
            try:
                await switchBotApp.send_message(message.text.message.partition('/cast')[-1], user_id=user['_id'])
            except Exception as _:
                blocked['switch'] += 1
    await message.reply(
        '**Broadcast Completed [Status]**\n'
        '\n'
        f'**Total**: `{total["total"]}`\n'
        f'**Successfull**: `{total["total"] - blocked["switch"] - blocked["telegram"]}`\n'
        f'**Blocked on switch**: `{blocked["switch"]}`\n',
        f'**Blocked on telegram**: `{blocked["telegram"]}`',
    )

@app.on_callback_query(callback_filter(['btc']))
async def donate_btc(_, query: CallbackQuery):
    await query.answer()
    await query.message.edit_text(
        'Donate Bitcoin to this address\n\n`1ETrSu55o9Gfc2CjaSgwco1Qqz9Y9VgLrA`',
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton('Go back', callback_data='back_to_donate')
            ]
        ]),
        parse_mode=ParseMode.MARKDOWN,
    )

@app.on_callback_query(callback_filter(['donate']))
@app.on_callback_query(callback_filter(['back_to_donate']))
async def donate(_, query: CallbackQuery):
    await query.answer()
    await app.edit_message_text(
        query.message.chat.id,
        query.message.id,
        '❤️ Thank You!'
        '\n'
        'We value your donation!',
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton('☕ Kofi', url='https://ko-fi.com/akashpattnaik'),
            ],
            [
                InlineKeyboardButton('💰 Bitcoin', callback_data='btc'),
                InlineKeyboardButton('🔷 Paypal', url='https://paypal.me/akasham1?country.x=IN&locale.x=en_GB'),
            ]
        ])
    )

@app.on_callback_query(callback_filter(['channel_check']))
async def chennel_check(_, query: CallbackQuery):
    userjoinStatus = await checkUserJoinStatus(query.from_user.id)
    if not userjoinStatus:
        return await query.answer('Please Join Channel to use bot!')
    await app.delete_messages(query.message.chat.id, [query.message.id])
    await app.send_message(
        query.message.chat.id,
        '✅ Success! Try sending a file now!'
    )

# The file should be sent in private and must be one of [document, photo, video]
@app.on_message(filters=(filters.document | filters.photo | filters.video | filters.audio) & filters.private)
async def handle_files(_, message: Message):
    userjoinStatus = await checkUserJoinStatus(message.from_user.id)
    if not userjoinStatus:
        return await message.reply(
            "Join the exciting community and unlock 🔓 all the power of this bot",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton('🔥 Join Channel', url='https://t.me/TrashProjects'),
                ],
                [
                    InlineKeyboardButton('✅ Done', callback_data='channel_check')
                ]
            ])
        )
    media = message.document or message.photo or message.video or message.audio
    file = utils.FileObject()
    if message.media.value == 'photo':
        file.file_name = getattr(media, 'file_name', 'photo.png') # Sometimes it's empty
    else:
        file.file_name = media.file_name
    file.file_id = media.file_id
    file.file_size = media.file_size
    file.file_type = message.media.value
    file.start_time = int(time.time())
    file.download_link = None
    file.fetch_id = uuid.uuid4().hex[:7] # A 7 characters long random ID to fetch the file
    await files.save_file(file, 'TELEGRAM')
    await message.reply(
        '✅ **Success**\n'
        '\n'
        'Your file has been registered!\n'
        f'**Fetch ID**: `{file.fetch_id}`\n'
        '**Expires In**: `24h hours from now`'
        '\n'
        'Use this Fetch ID in our switch bot to fetch the file there!',
        reply_to_message_id=message.id,
        parse_mode=ParseMode.MARKDOWN,
    )
