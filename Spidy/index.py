import logging
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from info import ADMINS
from info import INDEX_REQ_CHANNEL as LOG_CHANNEL
from database.ia_filterdb import save_file
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import temp
import re
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lock = asyncio.Lock()


@Client.on_callback_query(filters.regex(r'^index'))
async def index_files(bot, query):
    if query.data.startswith('index_cancel'):
        temp.CANCEL = True
        return await query.answer("Cᴀɴᴄᴇʟʟɪɴɢ Iɴᴅᴇxɪɴɢ")
    _, raju, chat, lst_msg_id, from_user = query.data.split("#")
    if raju == 'reject':
        await query.message.delete()
        await bot.send_message(int(from_user),
                               f'Yᴏᴜʀ Sᴜʙᴍɪssɪᴏɴ Fᴏʀ Iɴᴅᴇxɪɴɢ {chat} Hᴀs Bᴇᴇɴ Dᴇᴄʟɪᴇɴᴇᴅ Bʏ Oᴜʀ Mᴏᴅᴇʀᴀᴛᴏʀs.',
                               reply_to_message_id=int(lst_msg_id))
        return

    if lock.locked():
        return await query.answer('Wᴀɪᴛ Uɴᴛɪʟ Pʀᴇᴠɪᴏᴜs Pʀᴏᴄᴇss Cᴏᴍᴘʟᴇᴛᴇ.', show_alert=True)
    msg = query.message

    await query.answer('Pʀᴏᴄᴇssɪɴɢ...⏳', show_alert=True)
    if int(from_user) not in ADMINS:
        await bot.send_message(int(from_user),
                               f'Yᴏᴜʀ Sᴜʙᴍɪssɪᴏɴ Fᴏʀ Iɴᴅᴇxɪɴɢ {chat} Hᴀs Bᴇᴇɴ Aᴄᴄᴇᴘᴛᴇᴅ Bʏ Oᴜʀ Mᴏᴅᴇʀᴀᴛᴏʀs Aɴᴅ Wɪʟʟ Bᴇ Aᴅᴅᴇᴅ Sᴏᴏɴ.',
                               reply_to_message_id=int(lst_msg_id))
    await msg.edit(
        "Sᴛᴀʀᴛɪɴɢ Iɴᴅᴇxɪɴɢ",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('Cᴀɴᴄᴇʟ', callback_data='index_cancel')]]
        )
    )
    try:
        chat = int(chat)
    except:
        chat = chat
    await index_files_to_db(int(lst_msg_id), chat, msg, bot)


@Client.on_message((filters.forwarded | (filters.regex("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")) & filters.text ) & filters.private & filters.incoming)
async def send_for_index(bot, message):
    if message.text:
        regex = re.compile("(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(message.text)
        if not match:
            return await message.reply('Iɴᴠᴀʟɪᴅ Lɪɴᴋ')
        chat_id = match.group(4)
        last_msg_id = int(match.group(5))
        if chat_id.isnumeric():
            chat_id  = int(("-100" + chat_id))
    elif message.forward_from_chat.type == enums.ChatType.CHANNEL:
        last_msg_id = message.forward_from_message_id
        chat_id = message.forward_from_chat.username or message.forward_from_chat.id
    else:
        return
    try:
        await bot.get_chat(chat_id)
    except ChannelInvalid:
        return await message.reply('Tʜɪs Mᴀʏ Bᴇ A Pʀɪᴠᴀᴛᴇ Cʜᴀɴɴᴇʟ / Gʀᴏᴜᴘ. Mᴀᴋᴇ Mᴇ Aɴ Aᴅᴍɪɴ Oᴠᴇʀ Tʜᴇʀᴇ Tᴏ Iɴᴅᴇx Tʜᴇ Fɪʟᴇs.')
    except (UsernameInvalid, UsernameNotModified):
        return await message.reply('Iɴᴠᴀʟɪᴅ Lɪɴᴋ Sᴘᴇᴄɪғɪᴇᴅ.')
    except Exception as e:
        logger.exception(e)
        return await message.reply(f'Eʀʀᴏʀs - {e}')
    try:
        k = await bot.get_messages(chat_id, last_msg_id)
    except:
        return await message.reply('Mᴀᴋᴇ Sᴜʀᴇ Tʜᴀᴛ Iᴀᴍ Aɴ Aᴅᴍɪɴ Iɴ Tʜᴇ Cʜᴀɴɴᴇʟ, Iғ Cʜᴀɴɴᴇʟ Is Pʀɪᴠᴀᴛᴇ')
    if k.empty:
        return await message.reply('Tʜɪs Mᴀʏ Bᴇ Gʀᴏᴜᴘ Aɴᴅ Iᴀᴍ Nᴏᴛ A Aᴅᴍɪɴ Oғ Tʜᴇ Gʀᴏᴜᴘ.')

    if message.from_user.id in ADMINS:
        buttons = [
            [
                InlineKeyboardButton('Yᴇs',
                                     callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')
            ],
            [
                InlineKeyboardButton('Cʟᴏsᴇ', callback_data='close_data'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        return await message.reply(
            f'Dᴏ Yᴏᴜ Wᴀɴᴛ Tᴏ Iɴᴅᴇx Tʜɪs Cʜᴀɴɴᴇʟ/ Gʀᴏᴜᴘ ?\n\nCʜᴀᴛ Iᴅ/ Usᴇʀɴᴀᴍᴇ: <code>{chat_id}</code>\nLᴀsᴛ Mᴇssᴀɢᴇ Iᴅ: <code>{last_msg_id}</code>',
            reply_markup=reply_markup)

    if type(chat_id) is int:
        try:
            link = (await bot.create_chat_invite_link(chat_id)).invite_link
        except ChatAdminRequired:
            return await message.reply('Mᴀᴋᴇ Sᴜʀᴇ Iᴀᴍ Aɴ Aᴅᴍɪɴ Iɴ Tʜᴇ Cʜᴀᴛ Aɴᴅ Hᴀᴠᴇ Pᴇʀᴍɪssɪᴏɴ Tᴏ Iɴᴠɪᴛᴇ Usᴇʀs.')
    else:
        link = f"@{message.forward_from_chat.username}"
    buttons = [
        [
            InlineKeyboardButton('Aᴄᴄᴇᴘᴛ Iɴᴅᴇx',
                                 callback_data=f'index#accept#{chat_id}#{last_msg_id}#{message.from_user.id}')
        ],
        [
            InlineKeyboardButton('Rᴇᴊᴇᴄᴛ Iɴᴅᴇx',
                                 callback_data=f'index#reject#{chat_id}#{message.id}#{message.from_user.id}'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await bot.send_message(LOG_CHANNEL,
                           f'#IndexRequest\n\nBʏ : {message.from_user.mention} (<code>{message.from_user.id}</code>)\nCʜᴀᴛ Iᴅ/ Usᴇʀɴᴀᴍᴇ - <code> {chat_id}</code>\Lᴀsᴛ Mᴇssᴀɢᴇ Iᴅ - <code>{last_msg_id}</code>\nIɴᴠɪᴛᴇʟɪɴᴋ - {link}',
                           reply_markup=reply_markup)
    await message.reply('Tʜᴀɴᴋʏᴏᴜ Fᴏʀ Tʜᴇ Cᴏɴᴛʀɪʙᴜᴛɪᴏɴ, Wᴀɪᴛ Fᴏʀ Mʏ Mᴏᴅᴇʀᴀᴛᴏʀs Tᴏ Vᴇʀɪғʏ Tʜᴇ Fɪʟᴇs.')


@Client.on_message(filters.command('setskip') & filters.user(ADMINS))
async def set_skip_number(bot, message):
    if ' ' in message.text:
        _, skip = message.text.split(" ")
        try:
            skip = int(skip)
        except:
            return await message.reply("Sᴋɪᴘ Nᴜᴍʙᴇʀ Sʜᴏᴜʟᴅ Bᴇ Aɴ Iɴᴛᴇɢᴇʀ.")
        await message.reply(f"Sᴜᴄᴄᴇssғᴜʟʟʏ Sᴇᴛ Sᴋɪᴘ Nᴜᴍʙᴇʀ As {skip}")
        temp.CURRENT = int(skip)
    else:
        await message.reply("Gɪᴠᴇ Mᴇ A Sᴋɪᴘ Nᴜᴍʙᴇʀ")


async def index_files_to_db(lst_msg_id, chat, msg, bot):
    total_files = 0
    duplicate = 0
    errors = 0
    deleted = 0
    no_media = 0
    unsupported = 0
    async with lock:
        try:
            current = temp.CURRENT
            temp.CANCEL = False
            async for message in bot.iter_messages(chat, lst_msg_id, temp.CURRENT):
                if temp.CANCEL:
                    await msg.edit(f"<b>Sᴜᴄᴄᴇssғᴜʟʟʏ Cᴀɴᴄᴇʟʟᴇᴅ!!\n\nSᴀᴠᴇᴅ <code>{total_files}</code> Fɪʟᴇs Tᴏ Dᴀᴛᴀʙᴀsᴇ!\nDᴜᴘʟɪᴄᴀᴛᴇ Fɪʟᴇs Sᴋɪᴘᴘᴇᴅ: <code>{duplicate}</code>\nDᴇʟᴇᴛᴇᴅ Mᴇssᴀɢᴇs Sᴋɪᴘᴘᴇᴅ: <code>{deleted}</code>\nNᴏɴ-ᴍᴇᴅɪᴀ Mᴇssᴀɢᴇs Sᴋɪᴘᴘᴇᴅ: <code>{no_media + unsupported}</code>(Uɴsᴜᴘᴘᴏʀᴛᴇᴅ Mᴇᴅɪᴀ - `{unsupported}` )\nEʀʀᴏʀs Oᴄᴄᴜʀʀᴇᴅ: <code>{errors}</code></b>")
                    break
                current += 1
                if current % 20 == 0:
                    can = [[InlineKeyboardButton('Cᴀɴᴄᴇʟ', callback_data='index_cancel')]]
                    reply = InlineKeyboardMarkup(can)
                    await msg.edit_text(
                        text=f"<b>Tᴏᴛᴀʟ Mᴇssᴀɢᴇs Fᴇᴛᴄʜᴇᴅ: <code>{current}</code>\nTᴏᴛᴀʟ Mᴇssᴀɢᴇs Sᴀᴠᴇᴅ: <code>{total_files}</code>\nDᴜᴘʟɪᴄᴀᴛᴇ Fɪʟᴇs Sᴋɪᴘᴘᴇᴅ: <code>{duplicate}</code>\nDᴇʟᴇᴛᴇᴅ Mᴇssᴀɢᴇs Sᴋɪᴘᴘᴇᴅ: <code>{deleted}</code>\nNᴏɴ-ᴍᴇᴅɪᴀ Mᴇssᴀɢᴇs Sᴋɪᴘᴘᴇᴅ: <code>{no_media + unsupported}</code>(Uɴsᴜᴘᴘᴏʀᴛᴇᴅ Mᴇᴅɪᴀ - `{unsupported}` )\nEʀʀᴏʀs Oᴄᴄᴜʀʀᴇᴅ: <code>{errors}</code></b>",
                        reply_markup=reply)
                if message.empty:
                    deleted += 1
                    continue
                elif not message.media:
                    no_media += 1
                    continue
                elif message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.AUDIO, enums.MessageMediaType.DOCUMENT]:
                    unsupported += 1
                    continue
                media = getattr(message, message.media.value, None)
                if not media:
                    unsupported += 1
                    continue
                media.file_type = message.media.value
                media.caption = message.caption
                aynav, vnay = await save_file(media)
                if aynav:
                    total_files += 1
                elif vnay == 0:
                    duplicate += 1
                elif vnay == 2:
                    errors += 1
        except Exception as e:
            logger.exception(e)
            await msg.edit(f'Error: {e}')
        else:
            await msg.edit(f'<b>Sᴜᴄᴄᴇsғᴜʟʟʏ Sᴀᴠᴇᴅ <code>{total_files}</code> Tᴏ Dᴀᴛᴀʙᴀsᴇ!\nDᴜᴘʟɪᴄᴀᴛᴇ Fɪʟᴇs Sᴋɪᴘᴘᴇᴅ: <code>{duplicate}</code>\nDᴇʟᴇᴛᴇᴅ Mᴇssᴀɢᴇs Sᴋɪᴘᴘᴇᴅ: <code>{deleted}</code>\nNᴏɴ-ᴍᴇᴅɪᴀ Mᴇssᴀɢᴇs Sᴋɪᴘᴘᴇᴅ: <code>{no_media + unsupported}</code>(Uɴsᴜᴘᴘᴏʀᴛᴇᴅ Mᴇᴅɪᴀ - `{unsupported}` )\nEʀʀᴏʀs Oᴄᴄᴜʀʀᴇᴅ: <code>{errors}</code></b>')
