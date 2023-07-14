import asyncio
import math
import os
import psutil
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from info import ADMINS, LOG_CHANNEL, SUPPORT_CHAT, MELCOW_NEW_USERS, CHNL_LNK, GRP_LNK, NEWGRP
from database.users_chats_db import db
from database.ia_filterdb import Media
from utils import get_size, temp, get_settings, get_readable_time
from Script import script
from pyrogram.errors import ChatAdminRequired

"""-----------------------------------------https://t.me/GetTGLink/4179 --------------------------------------"""

@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    r_j_check = [u.id for u in message.new_chat_members]
    if temp.ME in r_j_check:
        if not await db.get_chat(message.chat.id):
            total=await bot.get_chat_members_count(message.chat.id)
            r_j = message.from_user.mention if message.from_user else "Anonymous" 
            await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, r_j))       
            await db.add_chat(message.chat.id, message.chat.title)
        if message.chat.id in temp.BANNED_CHATS:
            # Inspired from a boat of a banana tree
            buttons = [[
                InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ', url=f'{SUPPORT_CHAT}')
            ]]
            reply_markup=InlineKeyboardMarkup(buttons)
            k = await message.reply(
                text='<b>🚫 CHAT NOT ALLOWED 🚫\n\nMʏ Aᴅᴍɪɴs Hᴀs Rᴇsᴛʀɪᴄᴛᴇᴅ Mᴇ Fʀᴏᴍ Wᴏʀᴋɪɴɢ Hᴇʀᴇ ! Iғ Yᴏᴜ Wᴀɴᴛ Tᴏ Kɴᴏᴡ Mᴏʀᴇ Aʙᴏᴜᴛ Iᴛ Cᴏɴᴛᴀᴄᴛ Sᴜᴘᴘᴏʀᴛ..</b>',
                reply_markup=reply_markup,
            )

            try:
                await k.pin()
            except:
                pass
            await bot.leave_chat(message.chat.id)
            return
        buttons = [[
                    InlineKeyboardButton('📣 Uᴘᴅᴀᴛᴇs', url=CHNL_LNK),
                    InlineKeyboardButton('❓ Hᴇʟᴘ', url=f"https://t.me/{temp.U_NAME}?start=help")
                  ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=f"<b>Tʜᴀɴᴋ Yᴏᴜ Fᴏʀ Aᴅᴅɪɴɢ Mᴇ Iɴ {message.chat.title} ❣️\n\n➪ Dᴏɴ'ᴛ Fᴏʀɢᴇᴛ Tᴏ Mᴀᴋᴇ Mᴇ Aᴅᴍɪɴ ⚠️\n➪ Iғ Yᴏᴜ Hᴀᴠᴇ Aɴʏ Dᴏᴜʙᴛ Yᴏᴜ Cʟᴇᴀʀ Iᴛ Usɪɴɢ Bᴇʟᴏᴡ Bᴜᴛᴛᴏɴs</b>",
            reply_markup=reply_markup)
    else:
        settings = await get_settings(message.chat.id)
        if settings["welcome"]:
            for u in message.new_chat_members:
                buttons = [[
                InlineKeyboardButton("Sᴜʙsᴄʀɪʙᴇ Cʜᴀɴɴᴇʟ", url="https://t.me/Binge_Pirates")
            ]]
                if (temp.MELCOW).get('welcome') is not None:
                    try:
                        await (temp.MELCOW['welcome']).delete()
                    except:
                        pass
                temp.MELCOW['welcome'] = await message.reply_text(
                text=f"<b>🔖 Hᴇʟʟᴏ Mʏ Fʀɪᴇɴᴅ {u.mention}, </b>\n<b>Wᴇʟᴄᴏᴍᴇ Tᴏ {message.chat.title} !</b>",
                reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(60)
                await temp.MELCOW['welcome'].delete()

@Client.on_message(filters.command('leave') & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Gɪᴠᴇ Mᴇ A Cʜᴀᴛ Iᴅ')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        chat = chat
    try:
        buttons = [[
            InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ', url=f'{SUPPORT_CHAT}')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat,
            text='<b>Hᴇʟʟᴏ Fʀɪᴇɴᴅs,\n\nMʏ Aᴅᴍɪɴs Hᴀs Tᴏʟᴅ Mᴇ Tᴏ Lᴇᴀᴠᴇ Fʀᴏᴍ Gʀᴏᴜᴘ Sᴏ I Gᴏ! Iғ Yᴏᴜ Wᴀɴɴᴀ Aᴅᴅ Mᴇ Aɢᴀɪɴ Cᴏɴᴛᴀᴄᴛ Mʏ Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ.</b>',
            reply_markup=reply_markup,
        )

        await bot.leave_chat(chat)
        await message.reply(f"Lᴇғᴛ Tʜᴇ Cʜᴀᴛ `{chat}`")
    except Exception as e:
        await message.reply(f'Eʀʀᴏʀ - {e}')

@Client.on_message(filters.command('disable') & filters.user(ADMINS))
async def disable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Gɪᴠᴇ Mᴇ A Cʜᴀᴛ Iᴅ')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "Nᴏ Rᴇᴀsᴏɴ Pʀᴏᴠɪᴅᴇᴅ"
    try:
        chat_ = int(chat)
    except:
        return await message.reply('Gɪᴠᴇ Mᴇ A Vᴀʟɪᴅ Cʜᴀᴛ Iᴅ')
    cha_t = await db.get_chat(int(chat_))
    if not cha_t:
        return await message.reply("Cʜᴀᴛ Nᴏᴛ Fᴏᴜɴᴅ Iɴ Dʙ")
    if cha_t['is_disabled']:
        return await message.reply(f"Tʜɪs Cʜᴀᴛ Is Aʟʀᴇᴀᴅʏ Dɪsᴀʙʟᴇᴅ:\n\nRᴇᴀsᴏɴ-<code> {cha_t['reason']} </code>")
    await db.disable_chat(int(chat_), reason)
    temp.BANNED_CHATS.append(int(chat_))
    await message.reply('Cʜᴀᴛ Sᴜᴄᴄᴇssғᴜʟʟʏ Dɪsᴀʙʟᴇᴅ')
    try:
        buttons = [[
            InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ', url=f'{SUPPORT_CHAT}')
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat_, 
            text=f'<b>Hᴇʟʟᴏ Fʀɪᴇɴᴅs,\n\nMʏ Aᴅᴍɪɴs Hᴀs Tᴏʟᴅ Mᴇ Tᴏ Lᴇᴀᴠᴇ Fʀᴏᴍ Gʀᴏᴜᴘ Sᴏ I Gᴏ! Iғ Yᴏᴜ Wᴀɴɴᴀ Aᴅᴅ Mᴇ Aɢᴀɪɴ Cᴏɴᴛᴀᴄᴛ Mʏ Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ.\n\nRᴇᴀsᴏɴ :</b> <code>{reason}</code>',
            reply_markup=reply_markup)
        await bot.leave_chat(chat_)
        await bot.send_message(LOG_CHANNEL, script.BANG_LOG_TXT.format(chat_, reason, message.from_user.mention))
    except Exception as e:
        await message.reply(f"Error - {e}")


@Client.on_message(filters.command('enable') & filters.user(ADMINS))
async def re_enable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Gɪᴠᴇ Mᴇ A Cʜᴀᴛ Iᴅ')
    chat = message.command[1]
    try:
        chat_ = int(chat)
    except:
        return await message.reply('Gɪᴠᴇ Mᴇ A Vᴀʟɪᴅ Cʜᴀᴛ Iᴅ')
    sts = await db.get_chat(int(chat))
    if not sts:
        return await message.reply("Cʜᴀᴛ Nᴏᴛ Fᴏᴜɴᴅ Iɴ Dʙ !")
    if not sts.get('is_disabled'):
        return await message.reply('Tʜɪs Cʜᴀᴛ Is Nᴏᴛ Yᴇᴛ Dɪsᴀʙʟᴇᴅ.')
    await db.re_enable_chat(int(chat_))
    temp.BANNED_CHATS.remove(int(chat_))
    await message.reply("Cʜᴀᴛ Sᴜᴄᴄᴇssғᴜʟʟʏ Rᴇ-ᴇɴᴀʙʟᴇᴅ")
    await bot.send_message(LOG_CHANNEL, script.UNBANG_LOG_TXT.format(chat_, message.from_user.mention))


@Client.on_message(filters.command('stats') & filters.user(ADMINS) & filters.incoming)
async def get_ststs(bot, message):
    buttons = [[
            InlineKeyboardButton('Uᴘᴅᴀᴛᴇs', url=CHNL_LNK)
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    kdbotz = await message.reply('Fᴇᴛᴄʜɪɴɢ Sᴛᴀᴛs..')
    now = datetime.now()
    delta = now - bot.uptime
    uptime = get_readable_time(delta.seconds)
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    total_users = await db.total_users_count()
    totl_chats = await db.total_chat_count()
    files = await Media.count_documents()
    size = await db.get_db_size()
    free = 536870912 - size
    size = get_size(size)
    free = get_size(free)
    await kdbotz.edit_text(
            text=script.ADMIN_STATUS_TXT.format(uptime, ram, cpu, files, total_users, totl_chats, size, free),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

@Client.on_message(filters.command('invite') & filters.user(ADMINS))
async def gen_invite(bot, message):
    if len(message.command) == 1:
        return await message.reply('Gɪᴠᴇ Mᴇ A Cʜᴀᴛ Iᴅ')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        return await message.reply('Gɪᴠᴇ Mᴇ A Vᴀʟɪᴅ Cʜᴀᴛ Iᴅ')
    try:
        link = await bot.create_chat_invite_link(chat)
    except ChatAdminRequired:
        return await message.reply("Iɴᴠɪᴛᴇ Lɪɴᴋ Gᴇɴᴇʀᴀᴛɪᴏɴ Fᴀɪʟᴇᴅ, Iᴀᴍ Nᴏᴛ Hᴀᴠɪɴɢ Sᴜғғɪᴄɪᴇɴᴛ Rɪɢʜᴛs")
    except Exception as e:
        return await message.reply(f'Error {e}')
    await message.reply(f'Hᴇʀᴇ Is Yᴏᴜʀ Iɴᴠɪᴛᴇ Lɪɴᴋ {link.invite_link}')

@Client.on_message(filters.command('ban_user') & filters.user(ADMINS))
async def ban_a_user(bot, message):
    # https://t.me/GetTGLink/4185
    if len(message.command) == 1:
        return await message.reply('Gɪᴠᴇ Mᴇ A Usᴇʀ Iᴅ / Usᴇʀɴᴀᴍᴇ')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "Nᴏ Rᴇᴀsᴏɴ Pʀᴏᴠɪᴅᴇᴅ"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("Tʜɪs Is Aɴ Iɴᴠᴀʟɪᴅ Usᴇʀ, Mᴀᴋᴇ Sᴜʀᴇ Iᴀ Hᴀᴠᴇ Mᴇᴛ Hɪᴍ Bᴇғᴏʀᴇ.")
    except IndexError:
        return await message.reply("Tʜɪs Mɪɢʜᴛ Bᴇ A Cʜᴀɴɴᴇʟ, Mᴀᴋᴇ Sᴜʀᴇ Iᴛs A Usᴇʀ.")
    except Exception as e:
        return await message.reply(f'Eʀʀᴏʀ - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if jar['is_banned']:
            return await message.reply(f"{k.mention} Is Aʟʀᴇᴀᴅʏ Bᴀɴɴᴇᴅ\nRᴇᴀsᴏɴ: {jar['ban_reason']}")
        await db.ban_user(k.id, reason)
        temp.BANNED_USERS.append(k.id)
        await message.reply(f"Sᴜᴄᴄᴇssғᴜʟʟʏ Bᴀɴɴᴇᴅ {k.mention}")
        await bot.send_message(LOG_CHANNEL, script.BANP_LOG_TXT.format(message.from_user.mention, k.mention, reason))


    
@Client.on_message(filters.command('unban_user') & filters.user(ADMINS))
async def unban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('Gɪᴠᴇ Mᴇ A Usᴇʀ Iᴅ / Usᴇʀɴᴀᴍᴇ')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "Nᴏ Rᴇᴀsᴏɴ Pʀᴏᴠɪᴅᴇᴅ"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("Tʜɪs Is Aɴ Iɴᴠᴀʟɪᴅ Usᴇʀ, Mᴀᴋᴇ Sᴜʀᴇ Iᴀ Hᴀᴠᴇ Mᴇᴛ Hɪᴍ Bᴇғᴏʀᴇ.")
    except IndexError:
        return await message.reply("Tʜɪs Mɪɢʜᴛ Bᴇ A Cʜᴀɴɴᴇʟ, Mᴀᴋᴇ Sᴜʀᴇ Iᴛs A Usᴇʀ.")
    except Exception as e:
        return await message.reply(f'Eʀʀᴏʀ - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if not jar['is_banned']:
            return await message.reply(f"{k.mention} Is Nᴏᴛ Yᴇᴛ Bᴀɴɴᴇᴅ.")
        await db.remove_ban(k.id)
        temp.BANNED_USERS.remove(k.id)
        await message.reply(f"Sᴜᴄᴄᴇssғᴜʟʟʏ Uɴʙᴀɴɴᴇᴅ {k.mention}")
        await bot.send_message(LOG_CHANNEL, script.UNBANP_LOG_TXT.format(message.from_user.mention, k.mention))


    
@Client.on_message(filters.command('users') & filters.user(ADMINS))
async def list_users(bot, message):
    # https://t.me/GetTGLink/4184
    raju = await message.reply('Getting List Of Users')
    users = await db.get_all_users()
    out = "Usᴇʀs Sᴀᴠᴇᴅ Iɴ Dʙ Aʀᴇ:\n\n"
    async for user in users:
        out += f"<a href=tg://user?id={user['id']}>{user['name']}</a>"
        if user['ban_status']['is_banned']:
            out += '( Bᴀɴɴᴇᴅ Usᴇʀ )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('users.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('users.txt', caption="Lɪsᴛ Oғ Usᴇʀs")

@Client.on_message(filters.command('chats') & filters.user(ADMINS))
async def list_chats(bot, message):
    raju = await message.reply('Getting List Of chats')
    chats = await db.get_all_chats()
    out = "Cʜᴀᴛs Sᴀᴠᴇᴅ Iɴ Dʙ Aʀᴇ:\n\n"
    async for chat in chats:
        out += f"**Tɪᴛʟᴇ:** `{chat['title']}`\n**- Iᴅ:** `{chat['id']}`"
        if chat['chat_status']['is_disabled']:
            out += '( Dɪsᴀʙʟᴇᴅ Cʜᴀᴛ )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('chats.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('chats.txt', caption="Lɪsᴛ Oғ Cʜᴀᴛs")
