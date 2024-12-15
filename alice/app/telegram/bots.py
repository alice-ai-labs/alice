import asyncio
import logging
import sys
import random

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.routers import generate_text
from .config import Cfg, CfgBot, CfgButton


class BotInst(object):
    def __init__(self, bot: Bot, cfg: CfgBot)->None:
        self.bot = bot
        self.cfg = cfg


bots: list[BotInst] = []
photos: list[str] = []
buttons_builder = None


async def run_bot(buttons: list[CfgButton], images: list[str], greetings: list[str], botCfg: CfgBot)-> None:
    dp = Dispatcher()

    global photos
    global buttons_builder

    btns_builder = InlineKeyboardBuilder()
    for btn in buttons:
        btns_builder.button(text=btn.text,url=btn.url)
    btns_builder.adjust(2, 3) # TODO layout automatically

    buttons_builder = btns_builder
    photos = images

    @dp.message(CommandStart())
    async def cmd_start(message: Message) -> None:
        if not message.from_user:
            return
        await message.answer(f'Hello, {html.bold(message.from_user.full_name)}!')

    @dp.message(Command("info"))
    async def cmd_info(message: Message) -> None:
        await message.reply_photo(
            photo=random.choice(images),
            caption=botCfg.intro,
            reply_markup=btns_builder.as_markup(),
        )

    @dp.message()
    async def message_handler(message: Message) -> None:
        # check
        if not message:
            return
        
        # left us
        if message.left_chat_member:
            print(message.left_chat_member)
            return

        # join us
        if message.new_chat_members:
            for u in message.new_chat_members:
                if u.is_bot:
                    continue
                await bot.send_message(message.chat.id, random.choice(greetings) % u.full_name)
            return

        # reply to alice
        if message.reply_to_message and message.reply_to_message.from_user and message.text:
            text = generate_text(message.text)
            await message.reply(text)
            return

        # mentioned alice
        if message.entities and message.text:
            # entities=[
            #   MessageEntity(
            #       type='mention', offset=0,
            #       ength=13, url=None, user=None, language=None,
            #       custom_emoji_id=None)
            # ]
            users = []
            max_pos = 0
            for e in message.entities:
                pos = e.offset + e.length
                max_pos = max(max_pos, pos)

                if e.type != 'mention':
                    continue

                users.append(message.text[e.offset:e.offset+e.length])
            text = message.text[max_pos:]
            if text and '@'+botCfg.username in users:
                reply = generate_text(text)
                await message.reply(reply)
            return

        # check
        if not message.text or not message.from_user or message.from_user.is_bot:
            return
        # randomly reply unmentioned message
        if random.randint(0, 10) > botCfg.freechat_rate:
            return

        try:
            reply = generate_text(message.text)
            await message.answer(text=reply)
        except Exception as e:
            print(f'reply exception:{e}')

    global bots
    bot = Bot(token=botCfg.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    bots.append(BotInst(bot=bot, cfg=botCfg))
    await dp.start_polling(bot, handle_signals=False)


async def send_channel(channel_id :int, text :str) -> None:
    # search bot by channel id
    if not bots:
        print('there is no bots')
        return
    if not text:
        print('text is empty')
        return
    
    the_bot = None
    if channel_id:
        for bot in bots:
            if bot.cfg.channel.id == channel_id:
                the_bot = bot.bot
                break
    else:
        the_bot = bots[0].bot
        channel_id = bots[0].cfg.channel.id

    if not the_bot:
        print('not found the bot')
        return
    
    global buttons_builder
    global photos

    if buttons_builder and photos:
        await the_bot.send_photo(
            chat_id=channel_id,
            photo=random.choice(photos),
            caption=text,
            reply_markup=buttons_builder.as_markup(),
        )


async def send_group(group_id :int, text :str) -> None:
    # search bot by channel id
    if not bots:
        print('there is no bots')
        return
    if not text:
        print('text is empty')
        return
    
    the_bot = None
    if group_id:
        for bot in bots:
            if bot.cfg.group.id == group_id:
                the_bot = bot.bot
                break
    else:
        the_bot = bots[0].bot
        group_id = bots[0].cfg.group.id

    if not the_bot:
        print('not found the bot')
        return
    
    global buttons_builder
    global photos

    if buttons_builder and photos:
        await the_bot.send_photo(
            chat_id=group_id,
            photo=random.choice(photos),
            caption=text,
            reply_markup=buttons_builder.as_markup(),
        )


async def run(cfg: Cfg) -> None:
    tasks = []
    for bot in cfg.bots:
        tasks.append(run_bot(
            cfg.buttons,
            cfg.images,
            cfg.greetings,
            bot,
        ))
    if tasks:
        await asyncio.gather(*tasks)
