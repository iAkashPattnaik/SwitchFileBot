# FilwSwitchBot - Github
# Copyright (C) 2024 Akash Pattnaik
# This file is a part of < https://github.com/iAkashPattnaik/SwitchFileBot/ >
# PLease read the GNU General Public License v3.0 in <https://www.github.com/iAkashPattnaik/SwitchFileBot/blob/main/LICENSE/>.

# Inbuilt
from os import remove
import time

# site-packages
import uuid
from swibots import BotContext, CommandEvent, BotCommand, InlineKeyboardButton, InlineMarkup, filters, CallbackQueryEvent, MessageEvent

# SwitchFileBot
from config import Config
from src.database import users, files
from src import utils
from src.telegram_bot.main import app as telegramBotClient

app = utils.SwitchBot(
    Config.switchBotToken,
    "Telegram to Switch FileShareBot!"
)

def callback_filter(data: str):
    async def func(flt, data):
        return flt.data == data.event.callback_data
    return filters.create(func, data=data)

@app.on_command('start')
async def start_command(context: BotContext[CommandEvent]):
    if not (await users.is_user_exist(context.event.user_id)):
        await users.new_user(context.event.user_id, 'SWITCH')
    await context.event.message.reply_text(
        'Hello and welcome to *SwitchFileBot*\n'
        '\n'
        'Here you can send me files and generate a 24 hour valid token! Use this token to retreive the file in *switch* or *telegram*',
        inline_markup=InlineMarkup([
            [
                InlineKeyboardButton('🔥 Channel', url='https://switch.click/thegiganoobprojects'),
            ],
            [
                InlineKeyboardButton('💰 Donate', callback_data='donate'),
                InlineKeyboardButton('📺 Telegram Bot', url='https://telegram.dog/SwitchFileBot'),
            ],
            [
                InlineKeyboardButton('🧑‍💻 Source Code', url='https://github.com/iAkashPattnaik/SwitchFileBot'),
            ]
        ])
    )

@app.on_command('stats')
async def stats_command(context: BotContext[CommandEvent]):
    if not (await users.is_user_exist(context.event.user_id)):
        await users.new_user(context.event.user_id, 'SWITCH')
    _users = await users.total_users_count()
    _files = await files.total_files_count()
    await context.event.message.reply_text(
        '*Bot Stats*\n'
        '\n'
        f'*Total users*: `{_users["total"]}`\n'
        f'*Telegram users*: `{_users["telegram"]}`\n'
        f'*Switch users*: `{_users["switch"]}`\n'
        f'*Current Registred Files*: `{_files}`\n'
        f'*System Uptime*: `{utils.uptime()}`'
    )

@app.on_command('fetch')
async def fetch_file(context: BotContext[CommandEvent]):
    if not (await users.is_user_exist(context.event.user_id)):
        await users.new_user(context.event.user_id, 'SWITCH')
    if context.event.params == '':
        return await context.event.message.reply_text('❌ Invalid Fetch ID')
    file = await files.get_file_details(context.event.params)
    if len(file) == 0:
        return await context.event.message.reply_text('❌ Invalid Fetch ID')
    file: utils.FileObject = file[0]
    infoMssage = await context.event.message.send(f'📩 Donwloading File from *{file.platform}*')
    if file.platform == 'TELEGRAM':
        file_path = await telegramBotClient.download_media(file.file_id, file_name=file.file_name)
    else:
        file_path = await app.download_media(media=file)
    await infoMssage.edit_text('⬆️ Uploading File to *Switch*')
    await app.send_message(
        f'*File Name*: `{file.file_name}`\n'
        f'*File Size*: `{utils.get_size(file.file_size)}`\n'
        f'*Fetch ID*: `{file.fetch_id}`\n'
        f'*Register Time*: `{utils.get_registered_time(file.start_time)}`\n'
        f'*Register Platform*: `{file.platform}`\n'
        f'*Time Left*: `{utils.get_time_left(file.start_time)}`',
        inline_markup=InlineMarkup([
            [InlineKeyboardButton('🔥 Community', 'https://switch.click/thegiganoobprojects')],
            [InlineKeyboardButton('📺 Telegram Bot', 'https://telegram.dog/SwitchFileBot')],
        ]),
        user_id=context.event.user_id,
        document=file_path,
    )
    await infoMssage.delete()
    remove(file_path)

@app.on_command('cast')
async def cast_command(context: BotContext[CommandEvent]):
    if not (await users.is_user_exist(context.event.user_id)):
        await users.new_user(context.event.user_id, 'TELEGRAM')
    if context.event.user_id != Config.switchAdminId:
        return await context.event.message.reply_text('You don\'t have access to use this command!')
    total = await users.total_users_count()
    _users = await (await users.get_all_users()).to_list(total['total'])
    blocked = { 'switch': 0, 'telegram': 0 }
    for user in _users:
        if user['platform'] == 'TELEGRAM':
            try:
                await telegramBotClient.send_message(user['_id'], context.event.message.message.partition('/cast')[-1])
            except Exception as _:
                blocked['telegram'] += 1
        else:
            try:
                await app.send_message(context.event.message.message.partition('/cast')[-1], user_id=user['_id'])
            except Exception as _:
                blocked['switch'] += 1
    await context.event.message.reply_text(
        '*Broadcast Completed [Status]*\n'
        '\n'
        f'*Total*: `{total["total"]}`\n'
        f'*Successfull*: `{total["total"] - blocked["switch"] - blocked["telegram"]}`\n'
        f'*Blocked on switch*: `{blocked["switch"]}`\n',
        f'*Blocked on telegram*: `{blocked["telegram"]}`',
    )

@app.on_callback_query(callback_filter('btc'))
async def donate_btc(context: BotContext[CallbackQueryEvent]):
    await context.event.answer()
    await context.event.message.edit_text(
        text='Donate Bitcoin to this address\n\n`1ETrSu55o9Gfc2CjaSgwco1Qqz9Y9VgLrA`',
        inline_markup=InlineMarkup([
            [
                InlineKeyboardButton('Go back', callback_data='back_to_donate')
            ]
        ])
    )

@app.on_callback_query(callback_filter('donate'))
@app.on_callback_query(callback_filter('back_to_donate'))
async def donate(context: BotContext[CallbackQueryEvent]):
    await context.event.answer()
    await context.event.message.edit_text(
        '❤️ Thank You!\n'
        '\n'
        'We value your donation!',
        inline_markup=InlineMarkup([
            [
                InlineKeyboardButton('☕ Kofi', url='https://ko-fi.com/akashpattnaik'),
            ],
            [
                InlineKeyboardButton('💰 Bitcoin', callback_data='btc'),
                InlineKeyboardButton('🔷 Paypal', url='https://paypal.me/akasham1?country.x=IN&locale.x=en_GB'),
            ]
        ]),
    )

@app.on_message((filters.document | filters.photo | filters.video | filters.audio) & filters.personal)
async def handle_file(context: BotContext[MessageEvent]):
    # file = getattr(context.event.message.media_info, context.event.message.media_info.file_name, None)
    file = utils.FileObject()
    file.file_name = context.event.message.media_info.file_name
    if 'image' in context.event.message.media_info.mime_type:
        file.file_name = 'photo.png'
    file.file_id = str(context.event.message.media_id)
    file.file_ref = None
    file.file_size = context.event.message.media_info.file_size
    file.file_type = context.event.message.media_info.mime_type
    file.start_time = int(time.time())
    file.fetch_id = uuid.uuid4().hex[:7] # A 7 characters long random ID to fetch the file
    file.download_link = context.event.message.media_link
    await files.save_file(file, 'SWITCH')
    await app.send_message(
        '✅ *Success*\n'
        '\n'
        'Your file has been registered!\n'
        f'*Fetch ID*: <copy>{file.fetch_id}</copy>\n'
        '*Expires In*: `24h hours from now`'
        '\n'
        'Use this Fetch ID in our telegram bot to fetch the file there!',
        user_id=context.event.message.user_id,
        reply_to_message_id=context.event.message_id,
        inline_markup=InlineMarkup([
            [InlineKeyboardButton('📺 Telegram Bot', url='https://telegram.dog/SwitchFileBot')]
        ]),
    )

app.set_bot_commands([
    BotCommand('start', 'Start the bot'),
    BotCommand('fetch', 'Fetch a file from telegram'),
    BotCommand('stats', 'Get bot stats'),
])