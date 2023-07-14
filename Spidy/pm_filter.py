import asyncio
import re
import ast
import math

from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import ADMINS, AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, MSG_ALRT, AUTH_GROUPS, P_TTI_SHOW_OFF, GRP_LNK, CHNL_LNK, NOR_IMG, SPELL_IMG, IMDB, \
    SINGLE_BUTTON, SPELL_CHECK_REPLY, IMDB_TEMPLATE, SUPPORT_GROUP, SUPPORT_CHAT, FILE_CHANNEL_LINK, FILE_CHANNEL, DELETE_TIME, SPL_DELETE_TIME
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, temp, get_settings, save_group_settings, search_gagala
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results, get_bad_files
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters
)
from database.gfilters_mdb import (
    del_allg,
    find_gfilter,
    get_gfilters
)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}

@Client.on_message(filters.private & filters.text & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.private & filters.text & filters.incoming)
async def pv_filter(client, message):
    kd = await global_filters(client, message)
    if kd == False:
        await auto_filter(client, message)

@Client.on_message(filters.group & filters.text & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.group & filters.text & filters.incoming)
async def give_filter(client, message):
    if message.chat.id != SUPPORT_GROUP:
        await global_filters(client, message)
    mf = await manual_filters(client, message)
    if mf == False:
        settings = await get_settings(message.chat.id)
        try:
            if settings['auto_ffilter']:
                await auto_filter(client, message)
        except KeyError:
            grpid = await active_connection(str(message.from_user.id))
            await save_group_settings(grpid, 'auto_ffilter', True)
            settings = await get_settings(message.chat.id)
            if settings['auto_ffilter']:
                await auto_filter(client, message)

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT, show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer(script.OLD_ALRT_TXT, show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    settings = await get_settings(query.message.chat.id)
    reqnxt  = query.from_user.id if query.from_user else 0
    if settings['button']:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{reqnxt}#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}", callback_data=f'files#{reqnxt}#{file.file_id}'
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'files#{reqnxt}#{file.file_id}',
                ),
            ]
            for file in files
        ]
    try:
        if settings['auto_delete']:
            btn.insert(0, 
                [
                    InlineKeyboardButton(f'Iɴғᴏ', 'reqinfo'),
                    InlineKeyboardButton(f'Mᴏᴠɪᴇ', 'minfo'),
                    InlineKeyboardButton(f'Sᴇʀɪᴇs', 'sinfo')
                ]
            )

        else:
            btn.insert(0, 
                [
                    InlineKeyboardButton(f'Mᴏᴠɪᴇ', 'minfo'),
                    InlineKeyboardButton(f'Sᴇʀɪᴇs', 'sinfo'),
                    InlineKeyboardButton(f'Iɴғᴏ', 'reqinfoo')
                ]
            )
                
    except KeyError:
        grpid = await active_connection(str(message.from_user.id))
        await save_group_settings(grpid, 'auto_delete', True)
        settings = await get_settings(message.chat.id)
        if settings['auto_delete']:
            btn.insert(0, 
                [
                    InlineKeyboardButton(f'Iɴғᴏ', 'reqinfo'),
                    InlineKeyboardButton(f'Mᴏᴠɪᴇ', 'minfo'),
                    InlineKeyboardButton(f'Sᴇʀɪᴇs', 'sinfo')
                ]
            )

        else:
            btn.insert(0, 
                [
                    InlineKeyboardButton(f'Mᴏᴠɪᴇ', 'minfo'),
                    InlineKeyboardButton(f'Mᴏᴠɪᴇ', 'sinfo'),
                    InlineKeyboardButton(f'Iɴғᴏ', 'reqinfoo')
                ]
            )

    if 0 < offset <= 10:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 10
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("Bᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages")]
        )
    elif off_set is None:
        btn.append([InlineKeyboardButton("Pᴀɢᴇs", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"), InlineKeyboardButton("Nᴇxᴛ", callback_data=f"next_{req}_{key}_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("Bᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"),
                InlineKeyboardButton("Nᴇxᴛ", callback_data=f"next_{req}_{key}_{n_offset}")
            ],
        )
    btn.insert(0, [
        InlineKeyboardButton("⚡ Sᴜʙsᴄʀɪʙᴇ Cʜᴀɴɴᴇʟ ⚡", url=f"https://t.me/{temp.U_NAME}")
    ])
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()


@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer(script.ALRT_TXT, show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer(script.OLD_ALRT_TXT, show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer(script.TOP_ALRT_MSG)
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            await auto_filter(bot, query, k)
        else:
            k = await query.message.edit(script.MVE_NT_FND)

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        try:
            await query.message.reply_to_message.delete()
            await query.message.delete()
        except:
            await query.message.delete()
    elif query.data == "gfiltersdeleteallconfirm":
        await del_allg(query.message, 'gfilters')
        await query.answer("Done !")
        return
    elif query.data == "gfiltersdeleteallcancel": 
        await query.message.reply_to_message.delete()
        await query.message.delete()
        await query.answer("Process Cancelled !")
        return
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Mᴀᴋᴇ Sᴜʀᴇ I'ᴍ Pʀᴇsᴇɴᴛ Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ!!", quote=True)
            else:
                await query.message.edit_text(
                    "I'ᴍ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴀɴʏ ɢʀᴏᴜᴘs!\nCʜᴇᴄᴋ /connections Oʀ Cᴏɴɴᴇᴄᴛ Tᴏ Aɴʏ Gʀᴏᴜᴘs",
                    quote=True
                )

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("Yᴏᴜ Nᴇᴇᴅ Tᴏ Bᴇ Gʀᴏᴜᴘ Wᴡɴᴇʀ Oʀ Aɴ Aᴜᴛʜ Usᴇʀ Tᴏ Dᴏ Tʜᴀᴛ!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("Tʜᴀᴛ's Nᴏᴛ Fᴏʀ Yᴏᴜ!!", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "Cᴏɴɴᴇᴄᴛ"
            cb = "connectcb"
        else:
            stat = "Dɪsᴄᴏɴɴᴇᴄᴛ"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("Dᴇʟᴇᴛᴇ", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Gʀᴏᴜᴘ Nᴀᴍᴇ : **{title}**\nGʀᴏᴜᴘ Iᴅ : `{group_id}`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text('Sᴏᴍᴇ Eʀʀᴏʀ Oᴄᴄᴜʀʀᴇᴅ!!', parse_mode=enums.ParseMode.MARKDOWN)
        return 
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Dɪsᴄᴏɴɴᴇᴄᴛᴇᴅ Fʀᴏᴍ **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text(
                f"Sᴏᴍᴇ Eʀʀᴏʀ Oᴄᴄᴜʀʀᴇᴅ!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return 
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ Cᴏɴɴᴇᴄᴛɪᴏɴ !"
            )
        else:
            await query.message.edit_text(
                f"Sᴏᴍᴇ Eʀʀᴏʀ Oᴄᴄᴜʀʀᴇᴅ!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "Tʜᴇʀᴇ Aʀᴇ Nᴏ Aᴄᴛɪᴠᴇ Cᴏɴɴᴇᴄᴛɪᴏɴs!! Cᴏɴɴᴇᴄᴛ Tᴏ Sᴏᴍᴇ Gʀᴏᴜᴘs Fɪʀsᴛ.",
            )
            return
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - Aᴄᴛɪᴠᴇ" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Yᴏᴜʀ Cᴏɴɴᴇᴄᴛᴇᴅ Gʀᴏᴜᴘ Dᴇᴛᴀɪʟs ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "gfilteralert" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_gfilter('gfilters', keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    if query.data.startswith("file"):
        ident, req, file_id = query.data.split("#")
        if int(req) != 0 and query.from_user.id != int(req):
            return await query.answer(script.ALRT_TXT, show_alert=True)
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('Nᴏ Sᴜᴄʜ Fɪʟᴇ Exɪsᴛ.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"

        try:
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            elif settings['botpm']:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            else:
                mh = await client.send_cached_media(
                    chat_id=FILE_CHANNEL,
                    file_id=file_id,
                    caption=script.FILE_CHANNEL_TXT.format(title, size, query.from_user.mention, query.message.chat.title, temp.U_NAME),
                    protect_content=True if ident == "filep" else False,
                    reply_markup=InlineKeyboardMarkup(
                        [[
                          InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=GRP_LNK),
                          InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=CHNL_LNK)
                        ]]
                    )
                )
                mh8 = await query.message.reply(script.FILE_READY_TXT.format(query.from_user.mention, title, size),
                True,
                enums.ParseMode.HTML,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📥  Dᴏᴡɴʟᴏᴀᴅ Lɪɴᴋ  📥", url=f"{mh.link}")
                        ],
                        [
                            InlineKeyboardButton("⚠️ Cᴀɴ'ᴛ Aᴄᴄᴇss ❓ Jᴏɪɴ Cʜᴀɴɴᴇʟ ⚠️", url=f"{FILE_CHANNEL_LINK}")
                        ]
                    ]
                )
            )
            await asyncio.sleep(DELETE_TIME)
            await mh8.delete()
            await mh.delete()
            del mh8, mh
        except Exception as e:
            logger.exception(e, exc_info=True)
                
    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer("Fɪʀsᴛ Jᴏɪɴ Oᴜʀ Bᴀᴄᴋ Uᴘ Cʜᴀɴɴᴇʟ !", show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('Nᴏ Sᴜᴄʜ Fɪʟᴇ Exɪsᴛ.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        await query.answer()
        await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            protect_content=True if ident == 'checksubp' else False,
            reply_markup=InlineKeyboardMarkup(
                [
                 [
                  InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=GRP_LNK),
                  InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=CHNL_LNK)
               ]
                ]
            )
        )
            
    elif query.data == "pages":
        await query.answer(text=script.PAGEINFO, show_alert=True)

    elif query.data == "reqinfo":
        await query.answer(text=script.REQINFO, show_alert=True)

    elif query.data == "reqinfoo":
        await query.answer(text=script.REQINFO2, show_alert=True)

    elif query.data == "minfo":
        await query.answer(text=script.MINFO, show_alert=True)

    elif query.data == "sinfo":
        await query.answer(text=script.SINFO, show_alert=True)

    elif query.data == "splmd":
        await query.answer(text=script.SPLMD, show_alert=True)
        
    elif query.data == "doneupld":
        await query.answer(text=script.DONE_UPLOAD, show_alert=True)
        
    elif query.data == "rjctreq":
        await query.answer(text=script.REQ_REJECT, show_alert=True)
        
    elif query.data == "notavl":
        await query.answer(text=script.REQ_NO, show_alert=True)
        
    elif query.data == "donealrd":
        await query.answer(text=script.DONE_ALREADY, show_alert=True)
    elif query.data == "donealrd2":
        await query.answer(text=script.DONE_ALREADY, show_alert=True)
    elif query.data == "start":
        buttons = [[
                    InlineKeyboardButton('➕ Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
                ],[
                    InlineKeyboardButton('🍁 Oᴡɴᴇʀ', callback_data="owner_info"),
                    InlineKeyboardButton('🌿 Sᴜᴘᴘᴏʀᴛ', callback_data="kd_cnl")
                ],[
                    InlineKeyboardButton('❗ Hᴇʟᴘ', callback_data='help'),
                    InlineKeyboardButton('🕵️ Aʙᴏᴜᴛ', callback_data='about'),
                ],[
                    InlineKeyboardButton('🔒 Cʟᴏsᴇ Mᴇɴᴜ', callback_data='close_data')
                  ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('Mᴀɴᴜᴀʟ Fɪʟᴛᴇʀ', callback_data='manuelfilter'),
            InlineKeyboardButton('Aᴜᴛᴏ Fɪʟᴛᴇʀ', callback_data='autofilter')
        ], [
            InlineKeyboardButton('Cᴏɴɴᴇᴄᴛɪᴏɴ', callback_data='coct'),
            InlineKeyboardButton('Fɪʟᴇ Sᴛᴏʀᴇ', callback_data='kd_filstr')
        ], [
            InlineKeyboardButton('Iᴍᴅʙ', callback_data='kd_imdb'),
            InlineKeyboardButton('Mɪsᴄ', callback_data='kd_misc')
        ], [
            InlineKeyboardButton('Gᴏ Tᴏ Hᴏᴍᴇ', callback_data='start')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "about":
        buttons = [[
            InlineKeyboardButton('Sᴛᴀᴛᴜs', callback_data='stats')
        ],[
            InlineKeyboardButton('Rᴇᴘᴏʀᴛ Bᴜɢs & Fᴇᴇᴅʙᴀᴄᴋ', url=GRP_LNK)
        ],[
            InlineKeyboardButton('Hᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('Cʟᴏsᴇ', callback_data='close_data')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.B_LINK),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "manuelfilter":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help'),
            InlineKeyboardButton('Bᴜᴛᴛᴏɴs', callback_data='button')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MANUELFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "button":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='manuelfilter')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.BUTTON_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "coct":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CONNECTION_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "extra":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='help'),
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.EXTRAMOD_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "admin":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='owner_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ADMIN_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='about'),
            InlineKeyboardButton('⟲ Rᴇғʀᴇsʜ', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "rfrsh":
        await query.answer("Fᴇᴛᴄʜɪɴɢ Mᴏɴɢᴏᴅʙ Dᴀᴛᴀʙᴀsᴇ")
        buttons = [[
            InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='about'),
            InlineKeyboardButton('⟲ Rᴇғʀᴇsʜ', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "owner_info":
            btn = [[
                    InlineKeyboardButton("⟸ Bᴀᴄᴋ", callback_data="start"),
                    InlineKeyboardButton('Sᴜᴅᴏ', callback_data='admin')
                  ]]
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.OWNER_INFO),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "kd_filstr":
            filbtn = [[
                       InlineKeyboardButton("⟸ Bᴀᴄᴋ", callback_data="help")
                     ]]
            reply_markup = InlineKeyboardMarkup(filbtn)
            await query.message.edit_text(
                text=(script.KD_FILSTR),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "kd_imdb":
            imdbbtn = [[
                       InlineKeyboardButton("⟸ Bᴀᴄᴋ", callback_data="help")
                     ]]
            reply_markup = InlineKeyboardMarkup(imdbbtn)
            await query.message.edit_text(
                text=(script.KD_IMDB),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "kd_misc":
            miscbtn = [[
                       InlineKeyboardButton("⟸ Bᴀᴄᴋ", callback_data="help")
                     ]]
            reply_markup = InlineKeyboardMarkup(miscbtn)
            await query.message.edit_text(
                text=(script.KD_MISC),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "kd_cnl":
            cnlbtn = [[
                      InlineKeyboardButton('Gʀᴏᴜᴘ', url='https://t.me/+LpSH9qCWed4xM2Vh'),
                      InlineKeyboardButton('Cʜᴀɴɴᴇʟ', url='t.me/Binge_Pirates')
                     ], [
                      InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ', url='https://t.me/+LpSH9qCWed4xM2Vh'),
                      InlineKeyboardButton('Uᴘᴅᴀᴛᴇs', url='t.me/Binge_Pirates')
                     ], [
                      InlineKeyboardButton("⟸ Bᴀᴄᴋ", callback_data="start")
                     ]]
            reply_markup = InlineKeyboardMarkup(cnlbtn)
            await query.message.edit_text(
                text=(script.KD_CNL),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "closedata":
        if query.from_user.id not in ADMINS:
            await query.answer("ʏᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Rɪɢʜᴛs Tᴏ Cʟᴏsᴇ Tʜɪs.", show_alert = True)
            return
        await query.message.delete()

    elif query.data.startswith("req_upld"):
        if query.from_user.id not in ADMINS:
            await query.answer("ʏᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Rɪɢʜᴛs Tᴏ Tʜɪs", show_alert = True)
            return
        mess_id = query.data.split()[1]
        bmess_id = query.data.split()[2]
        await client.delete_messages(SUPPORT_GROUP, message_ids=int(bmess_id))
        ind=query.message.text.index("\n")
        await query.edit_message_text(text=f"<b>#COMPLETED\n\n<s>{query.message.text[ind+1:]}</s></b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="✅️ Uᴘʟᴏᴀᴅᴇᴅ ✅️", callback_data="doneupld")]])
        )
        await client.send_message(SUPPORT_GROUP, text=script.DONE_UPLOAD2,
            reply_to_message_id=int(mess_id),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="✅️ Cᴏᴍᴘʟᴇᴛᴇᴅ Rᴇǫᴜᴇsᴛ ✅️", url=f"{query.message.link}")]]),
        )            
    elif query.data.startswith("req_unabl"):
        if query.from_user.id not in ADMINS:
            await query.answer("Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Rɪɢʜᴛs Tᴏ Tʜɪs", show_alert = True)
            return
        mess_id = query.data.split()[1]
        bmess_id = query.data.split()[2]
        await client.delete_messages(SUPPORT_GROUP, message_ids=int(bmess_id))
        ind=query.message.text.index("\n")
        await query.edit_message_text(text=f"<b>#UNAVAILABLE\n\n<s>{query.message.text[ind+1:]}</s></b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="⚠️ Uɴᴀᴠᴀɪʟᴀʙʟᴇ ⚠️", callback_data="notavl")]])
        )
        await client.send_message(SUPPORT_GROUP, text=script.REQ_NO2,
            reply_to_message_id=int(mess_id),            
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Cʜᴇᴄᴋ Yᴏᴜʀ Rᴇǫᴜᴇsᴛ ⚠️", url=f"{query.message.link}")]]),
        )
    elif query.data.startswith("req_dcln"):
        if query.from_user.id not in ADMINS:
            await query.answer("Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Rɪɢʜᴛs Tᴏ Tʜɪs", show_alert = True)
            return
        mess_id = query.data.split()[1]
        bmess_id = query.data.split()[2]
        await client.delete_messages(SUPPORT_GROUP, message_ids=int(bmess_id))
        ind=query.message.text.index("\n")
        await query.edit_message_text(text=f"<b>#REJECTED\n\n<s>{query.message.text[ind+1:]}</s></b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="❌ Rᴇᴊᴇᴄᴛᴇᴅ ❌", callback_data="rjctreq")]])
        )
        await client.send_message(SUPPORT_GROUP, text=script.REQ_REJECT2,
            reply_to_message_id=int(mess_id),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Cʜᴇᴄᴋ Yᴏᴜʀ Rᴇǫᴜᴇsᴛ ❌", url=f"{query.message.link}")]]),
        )
    elif query.data.startswith("req_aval2"):
        if query.from_user.id not in ADMINS:
            await query.answer("Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Rɪɢʜᴛs Tᴏ Tʜɪs", show_alert = True)
            return
        mess_id = query.data.split()[1]
        bmess_id = query.data.split()[2]
        await client.delete_messages(SUPPORT_GROUP, message_ids=int(bmess_id))
        ind=query.message.text.index("\n")
        await query.edit_message_text(text=f"<b>#ALREADY\n\n<s>{query.message.text[ind+1:]}</s></b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="♻️ Aʟʀᴇᴀᴅʏ Aᴠᴀɪʟᴀʙʟᴇ Iɴ Cʜᴀɴɴᴇʟ ♻️", callback_data="donealrd2")]])
        )
        await client.send_message(SUPPORT_GROUP, text="""<b>Rᴇǫᴜᴇsᴛ Aʟʀᴇᴀᴅʏ Uᴘʟᴏᴀᴅᴇᴅ ❗,
Kɪɴᴅʟʏ Cʜᴇᴄᴋ Tʜᴇ Cʜᴀɴɴᴇʟ Bᴇғᴏʀᴇ Rᴇǫᴜᴇsᴛɪɴɢ.</b>""", reply_to_message_id=int(mess_id),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Cʜᴇᴄᴋ Yᴏᴜʀ Rᴇǫᴜᴇsᴛ ♻️", url=f"{query.message.link}")]]),
        )
    elif query.data.startswith("req_aval"):
        if query.from_user.id not in ADMINS:
            await query.answer("Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Rɪɢʜᴛs Tᴏ Tʜɪs", show_alert = True)
            return
        mess_id = query.data.split()[1]
        bmess_id = query.data.split()[2]
        await client.delete_messages(SUPPORT_GROUP, message_ids=int(bmess_id))
        ind=query.message.text.index("\n")
        await query.edit_message_text(text=f"<b>#ALREADY\n\n<s>{query.message.text[ind+1:]}</s></b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="♻️ Aʟʀᴇᴀᴅʏ Aᴠᴀɪʟᴀʙʟᴇ ♻️", callback_data="donealrd")]])
        )
        await client.send_message(SUPPORT_GROUP, text=script.DONE_ALREADY2,
            reply_to_message_id=int(mess_id),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Cʜᴇᴄᴋ Yᴏᴜʀ Rᴇǫᴜᴇsᴛ ♻️", url=f"{query.message.link}")]]),
        )
    elif query.data.startswith("morbtn"):
        if query.from_user.id not in ADMINS:
            await query.answer("Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Rɪɢʜᴛs Tᴏ Tʜɪs", show_alert = True)
            return
        mess_id = query.data.split()[1]
        bmess_id = query.data.split()[2]
        mrbtn = [[
                  InlineKeyboardButton(text="Aʟʀᴇᴀᴅʏ Aᴠᴀɪʟᴀʙʟᴇ Iɴ Bᴏᴛ", callback_data=f"req_aval {mess_id} {bmess_id}"),
                  InlineKeyboardButton(text="Aʟʀᴇᴀᴅʏ Aᴠᴀɪʟᴀʙʟᴇ Iɴ Cʜᴀɴɴᴇʟ", callback_data=f"req_aval2 {mess_id} {bmess_id}"),
                ],
                [
                  InlineKeyboardButton(text="Uɴᴀᴠᴀɪʟᴀʙʟᴇ", callback_data=f"req_unabl {mess_id} {bmess_id}"),
                  InlineKeyboardButton(text="Rᴇᴊᴇᴄᴛ", callback_data=f"req_dcln {mess_id} {bmess_id}")
                ],[
                  InlineKeyboardButton(text="Uᴘʟᴏᴀᴅᴇᴅ", callback_data=f"req_upld {mess_id} {bmess_id}")
                ]]
        reply_markup = InlineKeyboardMarkup(mrbtn)
        await query.message.edit_reply_markup(reply_markup)
    
    elif query.data == "predvd":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Dᴇʟᴇᴛɪɴɢ...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'predvd',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('Pʀᴇᴅᴠᴅ Fɪʟᴇ Fᴏᴜɴᴅ ! Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ Fʀᴏᴍ Dᴀᴛᴀʙᴀsᴇ.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ {deleted} PʀᴇDVD Fɪʟᴇs.</b>")

    elif query.data == "camrip":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Dᴇʟᴇᴛɪɴɢ...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'camrip',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('Cᴀᴍʀɪᴘ Fɪʟᴇ Fᴏᴜɴᴅ ! Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ Fʀᴏᴍ Dᴀᴛᴀʙᴀsᴇ.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ {deleted} CᴀᴍRɪᴘ Fɪʟᴇs.</b>")

    elif query.data == "predvdrip":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Dᴇʟᴇᴛɪɴɢ...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'Predvdrip',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('Pʀᴇᴅᴠᴅʀɪᴘ Fɪʟᴇ Fᴏᴜɴᴅ ! Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ Fʀᴏᴍ Dᴀᴛᴀʙᴀsᴇ.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ {deleted} PʀᴇDVDRɪᴘ Fɪʟᴇs.</b>")

    elif query.data == "hdcam":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Dᴇʟᴇᴛɪɴɢ...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'HDCam',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('Hᴅᴄᴀᴍs Fɪʟᴇ Fᴏᴜɴᴅ ! Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ Fʀᴏᴍ Dᴀᴛᴀʙᴀsᴇ.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ {deleted} HDCᴀᴍ Fɪʟᴇs.</b>")

    elif query.data == "hdcams":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Dᴇʟᴇᴛɪɴɢ...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'HD-Cam',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('Hᴅ-ᴄᴀᴍs Fɪʟᴇ Fᴏᴜɴᴅ ! Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ Fʀᴏᴍ Dᴀᴛᴀʙᴀsᴇ.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ {deleted} HD-Cᴀᴍ Fɪʟᴇs.</b>")

    elif query.data == "sprint":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Dᴇʟᴇᴛɪɴɢ...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'S-print',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('S-ᴘʀɪɴᴛ Fɪʟᴇ Fᴏᴜɴᴅ ! Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ Fʀᴏᴍ Dᴀᴛᴀʙᴀsᴇ.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ {deleted} S-Pʀɪɴᴛ Fɪʟᴇs.</b>")

    elif query.data == "hdts":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Dᴇʟᴇᴛɪɴɢ...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'HDTS',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('Hᴅᴛs Fɪʟᴇ Fᴏᴜɴᴅ ! Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ Fʀᴏᴍ Dᴀᴛᴀʙᴀsᴇ.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ {deleted} HDTS Fɪʟᴇs.</b>")

    elif query.data == "hdtss":
        k = await client.send_message(chat_id=query.message.chat.id, text="<b>Dᴇʟᴇᴛɪɴɢ...</b>")
        files, next_offset, total = await get_bad_files(
                                                  'HD-TS',
                                                  offset=0)
        deleted = 0
        for file in files:
            file_ids = file.file_id
            result = await Media.collection.delete_one({
                '_id': file_ids,
            })
            if result.deleted_count:
                logger.info('Hᴅ-ᴛs Fɪʟᴇ Fᴏᴜɴᴅ ! Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ Fʀᴏᴍ Dᴀᴛᴀʙᴀsᴇ.')
            deleted+=1
        deleted = str(deleted)
        await k.edit_text(text=f"<b>Sᴜᴄᴄᴇssғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ {deleted} HD-TS Fɪʟᴇs.</b>")
        
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("<b>Yᴏᴜʀ Aᴄᴛɪᴠᴇ Cᴏɴɴᴇᴄᴛɪᴏɴ Hᴀs Bᴇᴇɴ Cʜᴀɴɢᴇᴅ. Gᴏ Tᴏ /connections.</b>")

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Fɪʟᴛᴇʀ Bᴜᴛᴛᴏɴ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Sɪɴɢʟᴇ' if settings["button"] else 'Dᴏᴜʙʟᴇ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Fɪʟᴇ Mᴏᴅᴇ', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Sᴛᴀʀᴛ' if settings["botpm"] else 'Cʜᴀɴɴᴇʟ',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Fɪʟᴇ Sᴇᴄᴜʀᴇ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Eɴᴀʙʟᴇ' if settings["file_secure"] else 'Dɪsᴀʙʟᴇ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Iᴍᴅʙ Pᴏsᴛᴇʀ', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Eɴᴀʙʟᴇ' if settings["imdb"] else 'Dɪsᴀʙʟᴇ',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Sᴘᴇʟʟ Cʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Eɴᴀʙʟᴇ' if settings["spell_check"] else 'Dɪsᴀʙʟᴇ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Wᴇʟᴄᴏᴍᴇ Msɢ', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Eɴᴀʙʟᴇ' if settings["welcome"] else 'Dɪsᴀʙʟᴇ',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aᴜᴛᴏ Fɪʟᴛᴇʀ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Eɴᴀʙʟᴇ' if settings["auto_ffilter"] else 'Dɪsᴀʙʟᴇ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Aᴜᴛᴏ Fɪʟᴛᴇʀ Dᴇʟ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Eɴᴀʙʟᴇ' if settings["auto_delete"] else 'Dɪsᴀʙʟᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Fɪʟᴛᴇʀs Aᴜᴛᴏ Dᴇʟ',
                                         callback_data=f'setgs#mauto_delete#{settings["mauto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Eɴᴀʙʟᴇ' if settings["mauto_delete"] else 'Dɪsᴀʙʟᴇ',
                                         callback_data=f'setgs#mauto_delete#{settings["mauto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Cʟᴏsᴇ Sᴇᴛᴛɪɴɢs', callback_data='close_data')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)

    
async def auto_filter(client, msg, spoll=False):
    if not spoll:
        message = msg
        settings = await get_settings(message.chat.id)
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if len(message.text) < 100:
            search = message.text
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)
            if not files:
                if settings["spell_check"]:
                    return await advantage_spell_chok(msg)
                else:
                    return
        else:
            return
    else:
        settings = await get_settings(msg.message.chat.id)
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
    pre = 'filep' if settings['file_secure'] else 'file'
    req = message.from_user.id if message.from_user else 0
    if settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'{pre}#{req}#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}",
                    callback_data=f'{pre}#{req}#{file.file_id}',
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'{pre}#{req}#{file.file_id}',
                ),
            ]
            for file in files
        ]

    try:
        if settings['auto_delete']:
            btn.insert(0, 
                [
                    InlineKeyboardButton(f'Iɴғᴏ', 'reqinfo'),
                    InlineKeyboardButton(f'Mᴏᴠɪᴇ', 'minfo'),
                    InlineKeyboardButton(f'Sᴇʀɪᴇs', 'sinfo')
                ]
            )

        else:
            btn.insert(0, 
                [
                    InlineKeyboardButton(f'Mᴏᴠɪᴇ', 'minfo'),
                    InlineKeyboardButton(f'Sᴇʀɪᴇs', 'sinfo'),
                    InlineKeyboardButton(f'Iɴғᴏ', 'reqinfoo')
                ]
            )
                
    except KeyError:
        grpid = await active_connection(str(message.from_user.id))
        await save_group_settings(grpid, 'auto_delete', True)
        settings = await get_settings(message.chat.id)
        if settings['auto_delete']:
            btn.insert(0, 
                [
                    InlineKeyboardButton(f'Iɴғᴏ', 'reqinfo'),
                    InlineKeyboardButton(f'Mᴏᴠɪᴇ', 'minfo'),
                    InlineKeyboardButton(f'Sᴇʀɪᴇs', 'sinfo')
                ]
            )

        else:
            btn.insert(0, 
                [
                    InlineKeyboardButton(f'Mᴏᴠɪᴇ', 'minfo'),
                    InlineKeyboardButton(f'Sᴇʀɪᴇs', 'sinfo'),
                    InlineKeyboardButton(f'Iɴғᴏ', 'reqinfoo')
                ]
            )

    btn.insert(0, [
        InlineKeyboardButton("⚡ Sᴜʙsᴄʀɪʙᴇ Cʜᴀɴɴᴇʟ ⚡", url=f"https://t.me/{temp.U_NAME}")
    ])

    if offset != "":
        key = f"{message.chat.id}-{message.id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton("Pᴀɢᴇs", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="Nᴇxᴛ",callback_data=f"next_{req}_{key}_{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="Nᴏ Mᴏʀᴇ Pᴀɢᴇs Aᴠᴀɪʟᴀʙʟᴇ",callback_data="pages")]
        )
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(
            query=search,
            mention=message.from_user.mention if message.from_user else message.chat.title,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
    else:
        try:
            if settings['auto_delete']:
                cap = script.CAP_DLT_TXT.format(search, message.from_user.mention if message.from_user else message.chat.title)
            else:
                cap = script.CAP_TXT.format(search, message.from_user.mention if message.from_user else message.chat.title)
        except KeyError:
            grpid = await active_connection(str(message.from_user.id))
            await save_group_settings(grpid, 'auto_delete', True)
            settings = await get_settings(message.chat.id)
            if settings['auto_delete']:
                cap = script.CAP_DLT_TXT.format(search, message.from_user.mention if message.from_user else message.chat.title)
            else:
                cap = script.CAP_TXT.format(search, message.from_user.mention if message.from_user else message.chat.title)
    if imdb and imdb.get('poster'):
        try:
            if settings['auto_delete']:
                hehe = await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
                await asyncio.sleep(DELETE_TIME)
                await hehe.delete()
                await message.delete()
            else:
                await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
        except KeyError:
            grpid = await active_connection(str(message.from_user.id))
            await save_group_settings(grpid, 'auto_delete', True)
            settings = await get_settings(message.chat.id)
            if settings['auto_delete']:
                hehe = await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
                await asyncio.sleep(DELETE_TIME)
                await hehe.delete()
                await message.delete()
            else:
                await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            try:
                if settings['auto_delete']:
                    hmm = await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
                    await asyncio.sleep(DELETE_TIME)
                    await hmm.delete()
                    await message.delete()
                else:
                    await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
            except KeyError:
                grpid = await active_connection(str(message.from_user.id))
                await save_group_settings(grpid, 'auto_delete', True)
                settings = await get_settings(message.chat.id)
                if settings['auto_delete']:
                    hmm = await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
                    await asyncio.sleep(DELETE_TIME)
                    await hmm.delete()
                    await message.delete()
                else:
                    await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
        except Exception as e:
            logger.exception(e)
            fek = await message.reply_text(text=cap, reply_markup=InlineKeyboardMarkup(btn))
            try:
                if settings['auto_delete']:
                    await asyncio.sleep(DELETE_TIME)
                    await fek.delete()
                    await message.delete()
            except KeyError:
                grpid = await active_connection(str(message.from_user.id))
                await save_group_settings(grpid, 'auto_delete', True)
                settings = await get_settings(message.chat.id)
                if settings['auto_delete']:
                    await asyncio.sleep(DELETE_TIME)
                    await fek.delete()
                    await message.delete()
    else:
        fuk = await message.reply_text(text=cap, reply_markup=InlineKeyboardMarkup(btn))
        try:
            if settings['auto_delete']:
                await asyncio.sleep(DELETE_TIME)
                await fuk.delete()
                await message.delete()
        except KeyError:
            grpid = await active_connection(str(message.from_user.id))
            await save_group_settings(grpid, 'auto_delete', True)
            settings = await get_settings(message.chat.id)
            if settings['auto_delete']:
                await asyncio.sleep(DELETE_TIME)
                await fuk.delete()
                await message.delete()
    if spoll:
        await msg.message.delete()

async def advantage_spell_chok(msg):
    search = msg.text.replace(" ", "+")
    btn = [[
        InlineKeyboardButton(
            text="Iɴsᴛʀᴜᴄᴛɪᴏɴs",
            callback_data="splmd"
        ),
            InlineKeyboardButton(
            text="Gᴏᴏɢʟᴇ",
            url=f"https://google.com/search?q={search}"
        )
    ]]
    spl = await msg.reply(
        text=script.CUDNT_FND,
        reply_markup=InlineKeyboardMarkup(btn)
    )
    await asyncio.sleep(SPL_DELETE_TIME)
    await spl.delete()
    await msg.delete()
    return

async def manual_filters(client, message, text=False):
    settings = await get_settings(message.chat.id)
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            kunal = await client.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                protect_content=True if settings["file_secure"] else False,
                                reply_to_message_id=reply_id
                            )
                            try:
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_ffilter', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                            try:
                                if settings['mauto_delete']:
                                    await asyncio.sleep(DELETE_TIME)
                                    await message.delete()
                                    await kunal.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'mauto_delete', True)
                                settings = await get_settings(message.chat.id)
                                if settings['mauto_delete']:
                                    await asyncio.sleep(DELETE_TIME)
                                    await message.delete()
                                    await kunal.delete()

                        else:
                            button = eval(btn)
                            hmm = await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                protect_content=True if settings["file_secure"] else False,
                                reply_to_message_id=reply_id
                            )
                            try:
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_ffilter', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                            try:
                                if settings['mauto_delete']:
                                    await asyncio.sleep(DELETE_TIME)
                                    await message.delete()
                                    await hmm.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'mauto_delete', True)
                                settings = await get_settings(message.chat.id)
                                if settings['mauto_delete']:
                                    await asyncio.sleep(DELETE_TIME)
                                    await message.delete()
                                    await hmm.delete()

                    elif btn == "[]":
                        oto = await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            protect_content=True if settings["file_secure"] else False,
                            reply_to_message_id=reply_id
                        )
                        try:
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)
                        except KeyError:
                            grpid = await active_connection(str(message.from_user.id))
                            await save_group_settings(grpid, 'auto_ffilter', True)
                            settings = await get_settings(message.chat.id)
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)
                        try:
                            if settings['mauto_delete']:
                                await asyncio.sleep(DELETE_TIME)
                                await message.delete()
                                await oto.delete()
                        except KeyError:
                            grpid = await active_connection(str(message.from_user.id))
                            await save_group_settings(grpid, 'mauto_delete', True)
                            settings = await get_settings(message.chat.id)
                            if settings['mauto_delete']:
                                await asyncio.sleep(DELETE_TIME)
                                await message.delete()
                                await oto.delete()

                    else:
                        button = eval(btn)
                        dlt = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                        try:
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)
                        except KeyError:
                            grpid = await active_connection(str(message.from_user.id))
                            await save_group_settings(grpid, 'auto_ffilter', True)
                            settings = await get_settings(message.chat.id)
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)
                        try:
                            if settings['mauto_delete']:
                                await asyncio.sleep(DELETE_TIME)
                                await message.delete()
                                await dlt.delete()
                        except KeyError:
                            grpid = await active_connection(str(message.from_user.id))
                            await save_group_settings(grpid, 'mauto_delete', True)
                            settings = await get_settings(message.chat.id)
                            if settings['mauto_delete']:
                                await asyncio.sleep(DELETE_TIME)
                                await message.delete()
                                await dlt.delete()

                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False

async def global_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_gfilters('gfilters')
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_gfilter('gfilters', keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            knd3 = await client.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                reply_to_message_id=reply_id
                            )
                            await asyncio.sleep(DELETE_TIME)
                            await knd3.delete()
                            await message.delete()

                        else:
                            button = eval(btn)
                            knd2 = await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                            await asyncio.sleep(DELETE_TIME)
                            await knd2.delete()
                            await message.delete()

                    elif btn == "[]":
                        knd1 = await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                        await asyncio.sleep(DELETE_TIME)
                        await knd1.delete()
                        await message.delete()

                    else:
                        button = eval(btn)
                        knd = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                        await asyncio.sleep(DELETE_TIME)
                        await knd.delete()
                        await message.delete()

                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False
