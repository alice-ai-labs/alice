import asyncio
import logging
import sys
import random

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .const import Greetings


bot: Bot = None
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(f'Hello, {html.bold(message.from_user.full_name)}!')


@dp.message()
async def message_handler(message: Message) -> None:
    if message.left_chat_member:
        print(message.left_chat_member)
        return

    builder = InlineKeyboardBuilder()
    for index in range(1, 11):
        builder.button(text="google", url='https://google.com')
    builder.adjust(3, 2)

    if message.new_chat_members:
        for u in message.new_chat_members:
            if u.is_bot:
                continue
            await bot.send_message(message.chat.id, random.choice(Greetings) % u.full_name)
        return

    if message.entities:
        # entities=[
        #   MessageEntity(
        #       type='mention', offset=0, 
        #       ength=13, url=None, user=None, language=None, 
        #       custom_emoji_id=None)
        # ]
        users = []
        max_pos = 0
        for e in message.entities:
            print(e)
            pos = e.offset + e.length
            max_pos = max(max_pos, pos)

            if e.type != 'mention':
                continue

            users.append(message.text[e.offset:e.offset+e.length])
        text = message.text[max_pos:]
        print(users, text)
        # TODO reply if @alice is included while text is not empty
        return
         
    try:
        # TODO: ordinary message, reply randomly if sender if not bot and text is not empty
        await message.reply_photo(
            photo='https://www.ea.com/games/alice/alice-madness-returns', 
            caption='''
Alice

Network: Solana

Welcome!

''', 
            reply_markup=builder.as_markup(),
        )
    except TypeError:
        await message.answer('Nice try!')


async def start(token):
    global bot
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)
