class script(object):
    START_TXT = """<b>Hᴇʟʟᴏ {}

I Cᴀɴ Pʀᴏᴠɪᴅᴇ Mᴏᴠɪᴇs Aɴᴅ Sᴇʀɪᴇs,
I Wᴏʀᴋ Oɴ Bᴏᴛʜ Gʀᴏᴜᴘ Aɴᴅ Pᴍ.
Fᴏʀ Hᴇʟᴘ Cᴏɴsɪᴅᴇʀ Tʜᴇ Fᴏʟʟᴏᴡɪɴɢ Bᴜᴛᴛᴏɴs 🔻</b>"""

    HELP_TXT = """<b>Hᴇʏ {}

Hᴇʀᴇ Is Tʜᴇ Hᴇʟᴘ Fᴏʀ Mʏ Cᴏᴍᴍᴀɴᴅs.</b>"""

    ABOUT_TXT = """<b>✯ Mʏ Nᴀᴍᴇ : {}</b>

<b>✯ Cʀᴇᴀᴛᴏʀ : <a href=https://t.me/Mathew_Murdockk>Mᴀᴛʜᴇᴡ Mᴜʀᴅᴏᴄᴋ</a></b>

<b>✯ Uᴘᴅᴀᴛᴇs : <a href=https://t.me/Binge_Pirates>Binge Pirates</a></b>"""
 
    MANUELFILTER_TXT = """<b>Hᴇʟᴘ: Fɪʟᴛᴇʀs
- Fɪʟᴛᴇʀ Is A Fᴇᴀᴛᴜʀᴇ Wʜᴇʀᴇ Usᴇʀs Cᴀɴ Sᴇᴛ Aᴜᴛᴏᴍᴀᴛᴇᴅ Rᴇᴘʟɪᴇᴅ Fᴏʀ A Pᴀʀᴛɪᴄᴜʟᴀʀ Kᴇʏᴡᴏʀᴅ Aɴᴅ I Wɪʟʟ Rᴇsᴘᴏɴᴅ Wʜᴇɴᴇᴠᴇʀ A Kᴇʏᴡᴏʀᴅ Is Fᴏᴜɴᴅ Iɴ Tʜᴇ Mᴇssᴀɢᴇ.
Nᴏᴛᴇ:
1. Tʜɪs Bᴏᴛ Sʜᴏᴜʟᴅ Hᴀᴠᴇ Aᴅᴍɪɴ Pʀɪᴠɪʟᴇɢᴇ.
2. Oɴʟʏ Aᴅᴍɪɴs Cᴀɴ Aᴅᴅ Fɪʟᴛᴇʀs Iɴ A Cʜᴀᴛ.
3. Aʟᴇʀᴛ Bᴜᴛᴛᴏɴs Hᴀᴠᴇ A Lɪᴍɪᴛ Oғ 64 Cʜᴀʀᴀᴄᴛᴇʀs.

Cᴏᴍᴍᴀɴᴅs Aɴᴅ Usᴀɢᴇ:
• /filter - Aᴅᴅ A Fɪʟᴛᴇʀ Iɴ A Cʜᴀᴛ
• /filters - Lɪsᴛ Aʟʟ Tʜᴇ Fɪʟᴛᴇʀs Oғ A Cʜᴀᴛ
• /del - Dᴇʟᴇᴛᴇ A Sᴘᴇᴄɪғɪᴄ Fɪʟᴛᴇʀ Iɴ A Cʜᴀᴛ
• /delall - Dᴇʟᴇᴛᴇ Tʜᴇ Wʜᴏʟᴇ Fɪʟᴛᴇʀs Iɴ A (Cʜᴀᴛ Cʜᴀᴛ Oᴡɴᴇʀ Oɴʟʏ)

~ Aᴅᴅ Tʜᴇ Bᴏᴛ As Aᴅᴍɪɴ Oɴ Yᴏᴜʀ Gʀᴏᴜᴘ.
~ Usᴇ /connect Aɴᴅ Cᴏɴɴᴇᴄᴛ Yᴏᴜʀ Gʀᴏᴜᴘ Tᴏ Tʜᴇ Bᴏᴛ.
~ Usᴇ /settings Oɴ Bᴏᴛ's Pᴍ Aɴᴅ Tᴜʀɴ Oɴ/Oғғ Aᴜᴛᴏ Dᴇʟᴇᴛᴇ Mᴀɴᴜᴀʟ Fɪʟᴛᴇʀs Oɴ Tʜᴇ Sᴇᴛᴛɪɴɢs Mᴇɴᴜ.</b>"""

    BUTTON_TXT = """<b>Hᴇʟᴘ: Bᴜᴛᴛᴏɴꜱ

- Tʜɪꜱ Bᴏᴛ Sᴜᴘᴘᴏʀᴛꜱ Bᴏᴛʜ Uʀʟ Aɴᴅ Aʟᴇʀᴛ Iɴʟɪɴᴇ Bᴜᴛᴛᴏɴꜱ.

Nᴏᴛᴇ:
1. Tᴇʟᴇɢʀᴀᴍ Wɪʟʟ Nᴏᴛ Aʟʟᴏᴡꜱ Yᴏᴜ Tᴏ Sᴇɴᴅ Bᴜᴛᴛᴏɴꜱ Wɪᴛʜᴏᴜᴛ Aɴʏ Cᴏɴᴛᴇɴᴛ, Sᴏ Cᴏɴᴛᴇɴᴛ Iꜱ Mᴀɴᴅᴀᴛᴏʀʏ.
2. Tʜɪꜱ Bᴏᴛ Sᴜᴘᴘᴏʀᴛꜱ Bᴜᴛᴛᴏɴꜱ Wɪᴛʜ Aɴʏ Tᴇʟᴇɢʀᴀᴍ Mᴇᴅɪᴀ Tʏᴘᴇ.
3. Bᴜᴛᴛᴏɴꜱ Sʜᴏᴜʟᴅ Bᴇ Pʀᴏᴘᴇʀʟʏ Pᴀʀꜱᴇᴅ Aꜱ Mᴀʀᴋᴅᴏᴡɴ Fᴏʀᴍᴀᴛ.

Uʀʟ Bᴜᴛᴛᴏɴꜱ:
<code>[Button Text](buttonurl:https://t.me/Binge_Pirates)</code>

Aʟᴇʀᴛ Bᴜᴛᴛᴏɴꜱ:
<code>[Button Text](buttonalert:This Is Alert Message)</code></b>"""

    AUTOFILTER_TXT = """<b>Hᴇʟᴘ: ᴀᴜᴛᴏ Fɪʟᴛᴇʀ

Nᴏᴛᴇ: Fɪʟᴇ Iɴᴅᴇx
1. Mᴀᴋᴇ Mᴇ Tʜᴇ Aᴅᴍɪɴ Oꜰ Yᴏᴜʀ Cʜᴀɴɴᴇʟ Iꜰ Iᴛ'ꜱ Pʀɪᴠᴀᴛᴇ.
2. Mᴀᴋᴇ Sᴜʀᴇ Tʜᴀᴛ Yᴏᴜʀ Cʜᴀɴɴᴇʟ Dᴏᴇꜱ Nᴏᴛ Cᴏɴᴛᴀɪɴꜱ Cᴀᴍʀɪᴘꜱ, Pᴏʀɴ Aɴᴅ Fᴀᴋᴇ Fɪʟᴇꜱ.
3. Fᴏʀᴡᴀʀᴅ Tʜᴇ Lᴀꜱᴛ Mᴇꜱꜱᴀɢᴇ Tᴏ Mᴇ Wɪᴛʜ Qᴜᴏᴛᴇꜱ. I'ʟʟ Aᴅᴅ Aʟʟ Tʜᴇ Fɪʟᴇꜱ Iɴ Tʜᴀᴛ Cʜᴀɴɴᴇʟ Tᴏ Mʏ Dʙ.

Nᴏᴛᴇ: AᴜᴛᴏFɪʟᴛᴇʀ
1. Aᴅᴅ Tʜᴇ Bᴏᴛ As Aᴅᴍɪɴ Oɴ Yᴏᴜʀ Gʀᴏᴜᴘ.
2. Usᴇ /connect Aɴᴅ Cᴏɴɴᴇᴄᴛ Yᴏᴜʀ Gʀᴏᴜᴘ Tᴏ Tʜᴇ Bᴏᴛ.
3. Usᴇ /settings Oɴ Bᴏᴛ's PM Aɴᴅ Tᴜʀɴ Oɴ/Oғғ AᴜᴛᴏFɪʟᴛᴇʀ & Aᴜᴛᴏ Dᴇʟᴇᴛᴇ Oɴ Tʜᴇ Sᴇᴛᴛɪɴɢs Mᴇɴᴜ.
4. Usᴇ /set_template Tᴏ Sᴇᴛ Yᴏᴜʀ ᴄᴜsᴛᴏᴍ Iᴍᴅʙ Tᴇᴍᴘʟᴀᴛᴇ</b>"""

    CONNECTION_TXT = """<b>Hᴇʟᴘ: Cᴏɴɴᴇᴄᴛɪᴏɴꜱ

- Uꜱᴇᴅ Tᴏ Cᴏɴɴᴇᴄᴛ Bᴏᴛ Tᴏ Pᴍ Fᴏʀ Mᴀɴᴀɢɪɴɢ Fɪʟᴛᴇʀꜱ 
- ɪᴛ ʜᴇʟᴘꜱ ᴛᴏ ᴀᴠᴏɪᴅ ꜱᴘᴀᴍᴍɪɴɢ ɪɴ ɢʀᴏᴜᴘꜱ.

Nᴏᴛᴇ:
1. Oɴʟʏ Aᴅᴍɪɴꜱ Cᴀɴ Aᴅᴅ A Cᴏɴɴᴇᴄᴛɪᴏɴ.
2. Sᴇɴᴅ <code>/connect</code> Fᴏʀ Cᴏɴɴᴇᴄᴛɪɴɢ Mᴇ Tᴏ Yᴏᴜʀ Pᴍ

Cᴏᴍᴍᴀɴᴅs Aɴᴅ Usᴀɢᴇ:
• /connect  - Cᴏɴɴᴇᴄᴛ A Pᴀʀᴛɪᴄᴜʟᴀʀ Cʜᴀᴛ Tᴏ Yᴏᴜʀ Pᴍ
• /disconnect  - Dɪꜱᴄᴏɴɴᴇᴄᴛ Fʀᴏᴍ ᴀ Cʜᴀᴛ
• /connections - Lɪꜱᴛ Aʟʟ Yᴏᴜʀ Cᴏɴɴᴇᴄᴛɪᴏɴꜱ</b>"""

    ADMIN_TXT = """<b>Tʜɪs Mᴏᴅᴜʟᴇ Oɴʟʏ Wᴏʀᴋs Fᴏʀ Mʏ Aᴅᴍɪɴs

• /logs - Tᴏ Gᴇᴛ Tʜᴇ Rᴇᴄᴇɴᴛ Eʀʀᴏʀꜱ
• /stats - Tᴏ Gᴇᴛ Sᴛᴀᴛᴜꜱ Oꜰ Fɪʟᴇꜱ Iɴ Dʙ.
• /delete - Tᴏ Dᴇʟᴇᴛᴇ A Sᴇᴄɪꜰɪᴄ Fɪʟᴇ Fʀᴏᴍ Dʙ.
• /deleteall - Tᴏ Dᴇʟᴇᴛᴇ Aʟʟ Fɪʟᴇs Fʀᴏᴍ Dʙ.
• /users - Tᴏ Gᴇᴛ Lɪꜱᴛ Oꜰ Mʏ Uꜱᴇʀꜱ Aɴᴅ Iᴅꜱ.
• /chats - Tᴏ Gᴇᴛ Lɪꜱᴛ Oꜰ Mʏ Cʜᴀᴛꜱ Aɴᴅ Iᴅꜱ
• /channel - Tᴏ Gᴇᴛ Lɪꜱᴛ Oꜰ Tᴏᴛᴀʟ Cᴏɴɴᴇᴄᴛᴇᴅ Cʜᴀɴɴᴇʟꜱ
• /setskip - Tᴏ Sᴋɪᴘ Nᴜᴍʙᴇʀ Oғ Mᴇssᴀɢᴇs Wʜᴇɴ Iɴᴅᴇxɪɴɢ Fɪʟᴇs.
• /leave  - Tᴏ Lᴇᴀᴠᴇ Fʀᴏᴍ A Cʜᴀᴛ.
• /disable  -  Tᴏ Dɪꜱᴀʙʟᴇ A Cʜᴀᴛ.
• /invite - Tᴏ Gᴇᴛ Tʜᴇ Iɴᴠɪᴛᴇ Lɪɴᴋ Oғ Aɴʏ Cʜᴀᴛ Wʜᴇʀᴇ Tʜᴇ Bᴏᴛ Is Aᴅᴍɪɴ.
• /ban_user  - Tᴏ Bᴀɴ A Usᴇʀ.
• /unban_user  - Tᴏ Uɴʙᴀɴ A Usᴇʀ.
• /usend - Tᴏ Sᴇɴᴅ A Mᴇssᴀɢᴇ Tᴏ Pᴇʀᴛɪᴄᴜʟᴀʀ Usᴇʀ
• /gsend - Tᴏ Sᴇɴᴅ A Mᴇssᴀɢᴇ Tᴏ Pᴇʀᴛɪᴄᴜʟᴀʀ Cʜᴀᴛ
• /broadcast - Tᴏ Bʀᴏᴀᴅᴄᴀsᴛ A Mᴇssᴀɢᴇ Tᴏ Aʟʟ Usᴇʀs
• /group_broadcast - Tᴏ Bʀᴏᴀᴅᴄᴀsᴛ A Mᴇssᴀɢᴇ Tᴏ Aʟʟ Gʀᴏᴜᴘs
• /gfilter - Tᴏ Aᴅᴅ Gʟᴏʙᴀʟ Fɪʟᴛᴇʀs
• /gfilters - Tᴏ Vɪᴇᴡ Lɪsᴛ Oғ Aʟʟ Gʟᴏʙᴀʟ Fɪʟᴛᴇʀs
• /delg - Tᴏ Dᴇʟᴇᴛᴇ A Sᴘᴇᴄɪғɪᴄ Gʟᴏʙᴀʟ Fɪʟᴛᴇʀ
• /delallg - Tᴏ Dᴇʟᴇᴛᴇ Aʟʟ Gʟᴏʙᴀʟ Fɪʟᴛᴇʀs</b>"""

    STATUS_TXT = """<b>📂 Fɪʟᴇs Sᴀᴠᴇᴅ:</b> <code>{}</code>
<b>👤 Usᴇʀs:</b> <code>{}</code>
<b>👥 Gʀᴏᴜᴘs:</b> <code>{}</code>
<b>📉 Oᴄᴄᴜᴘɪᴇᴅ:</b> <code>{}</code>

<b><a href=https://t.me/Binge_Pirates>~ Mᴀɪɴᴛᴀɪɴᴇᴅ Bʏ Bɪɴɢᴇ Pɪʀᴀᴛᴇs</a></b>"""

    ADMIN_STATUS_TXT = """<b>⍟────[ ʙᴏᴛ sᴛᴀᴛᴜ𝗌 ]────⍟</b>

<b>⏳ Bᴏᴛ Uᴘᴛɪᴍᴇ:</b> <code>{}</code>

<b>☣️ Cᴘᴜ:</b> <code>{}%</code>

<b>☢️ Rᴀᴍ:</b> <code>{}%</code>

<b>📊 Fɪʟᴇs Sᴀᴠᴇᴅ:</b> <code>{}</code>

<b>👤 Usᴇʀs:</b> <code>{}</code>

<b>👥 Gʀᴏᴜᴘs:</b> <code>{}</code>

<b>♻️ Tᴏᴛᴀʟ:</b> <code>512 MB</code>

<b>🉐 Oᴄᴄᴜᴘɪᴇᴅ:</b> <code>{}</code>

<b>🆓 Fʀᴇᴇ:</b> <code>{}</code>

<b>⍟────[ @Binge_Pirates ]─────⍟</b>"""

    LOG_TEXT_G = """<b>#NewGroup
    
Gʀᴏᴜᴘ = {} (<code>{}</code>)

Tᴏᴛᴀʟ Mᴇᴍʙᴇʀs = <code>{}</code>

Aᴅᴅᴇᴅ Bʏ - {}</b>
"""
    LOG_TEXT_P = """<b>#NewUser
    
ID - <code>{}</code>

Nᴀᴍᴇ - {}</b>
"""
    ALRT_TXT = """⚠️ 𝖧ᴇʏ !
    
𝖲ᴇᴀʀᴄʜ 𝖸ᴏᴜʀ 𝖮ᴡɴ 𝖥ɪʟᴇ, 
    
𝖣ᴏɴ'ᴛ 𝖢ʟɪᴄᴋ 𝖮ᴛʜᴇʀ𝗌 𝖱ᴇ𝗌ᴜʟᴛ𝗌 😬
"""

    OLD_ALRT_TXT = """⚠️ 𝖧ᴇʏ ! 
    
𝖸ᴏᴜ Aʀᴇ U𝗌ɪɴɢ Oɴᴇ Oғ Mʏ Oʟᴅ Mᴇ𝗌𝗌ᴀɢᴇ𝗌, 
    
Sᴇɴᴅ Tʜᴇ Rᴇǫᴜᴇ𝗌ᴛ Aɢᴀɪɴ
"""

    CUDNT_FND = """<b>Sᴏʀʀʏ Nᴏ Fɪʟᴇ Wᴇʀᴇ Fᴏᴜɴᴅ
    
Cʜᴇᴄᴋ Yᴏᴜʀ Sᴘᴇʟʟɪɴɢ Iɴ Gᴏɢʟᴇ Aɴᴅ Tʀʏ Aɢᴀɪɴ

Rᴇᴀᴅ Iɴsᴛʀᴜᴄᴛɪᴏɴs Fᴏʀ Tʜᴇ Bᴇᴛᴛᴇʀ Rᴇsᴜʟᴛs ☟</b>
"""

    I_CUDNT = """
<b>Sᴏʀʀʏ

I Cᴏᴜʟᴅ Nᴏᴛ Fɪɴᴅ Aɴʏᴛʜɪɴɢ Rᴇʟᴀᴛᴇᴅ Tᴏ Tʜᴀᴛ
Pʟᴇᴀsᴇ Cʜᴇᴄᴋ Yᴏᴜʀ Sᴘᴇʟʟɪɴɢ 🤧</b>
"""

    I_CUD_NT = """I Cᴏᴜʟᴅɴ'ᴛ Fɪɴᴅ Aɴʏ Mᴏᴠɪᴇ Rᴇʟᴀᴛᴇᴅ Tᴏ {}.
Pʟᴇᴀsᴇ Cʜᴇᴄᴋ Tʜᴇ Sᴘᴇʟʟɪɴɢ Oɴ Gᴏᴏɢʟᴇ Oʀ Iᴍᴅʙ...
"""

    MVE_NT_FND = """<b>Mᴏᴠɪᴇ Nᴏᴛ Fᴏᴜɴᴅ...

Rᴇᴀsᴏɴs
𝟷) O.T.T Oʀ DVD Nᴏᴛ Rᴇʟᴇᴀsᴇᴅ

𝟸) Tʏᴘᴇ Nᴀᴍᴇ Wɪᴛʜ Yᴇᴀʀ

𝟹) Mᴏᴠɪᴇ Is Nᴏᴛ Aᴠᴀɪʟᴀʙʟᴇ Iɴ Tʜᴇ Dᴀᴛᴀʙᴀsᴇ 
Rᴇᴘᴏʀᴛ Hᴇʀᴇ @Binge_Request_Group</b>
"""

    TOP_ALRT_MSG = """Cʜᴇᴄᴋɪɴɢ Fᴏʀ Mᴏᴠɪᴇ Iɴ Dᴀᴛᴀʙᴀsᴇ...
"""
    
    OWNER_INFO = """<b>⍟───[ Oᴡɴᴇʀ Dᴇᴛᴀɪʟꜱ ]───⍟
    
• Fᴜʟʟ Nᴀᴍᴇ : Mᴀᴛʜᴇᴡ Mᴜʀᴅᴏᴄᴋ
• Uꜱᴇʀɴᴀᴍᴇ : @Mathew_Murdockk
• Pᴇʀᴍᴀɴᴇɴᴛ Dᴍ Lɪɴᴋ : <a href='t.me/Mathew_Murdockk'>Mᴀᴛʜᴇᴡ Mᴜʀᴅᴏᴄᴋ</a></b>"""

    KD_IMDB = """<b>Cᴏᴍᴍᴀɴᴅs Aɴᴅ Usᴀɢᴇ:

• /imdb  - Gᴇᴛ Tʜᴇ Fɪʟᴍ Iɴғᴏʀᴍᴀᴛɪᴏɴ Fʀᴏᴍ Iᴍᴅʙ Sᴏᴜʀᴄᴇ.
• /search  - Gᴇᴛ Tʜᴇ Fɪʟᴍ Iɴғᴏʀᴍᴀᴛɪᴏɴ Fʀᴏᴍ Vᴀʀɪᴏᴜs Sᴏᴜʀᴄᴇs.</b>"""

    KD_MISC = """<b>Cᴏᴍᴍᴀɴᴅs Aɴᴅ Usᴀɢᴇ:

• /id - Gᴇᴛ Iᴅ Oғ A Sᴘᴇᴄɪғɪᴇᴅ Usᴇʀ.</code>
• /info  - Gᴇᴛ Iɴғᴏʀᴍᴀᴛɪᴏɴ Aʙᴏᴜᴛ A Usᴇʀ.</b>"""

    KD_FILSTR = """<b>⍟ Wᴇʟᴄᴏᴍᴇ Tᴏ Fɪʟᴇ Sᴛᴏʀᴇ Mᴏᴅᴜʟᴇ ⍟

» A Mᴏᴅᴜʟᴇ Tᴏ Gᴇᴛ Sʜᴀʀᴀʙʟᴇ Lɪɴᴋ Fᴏʀ Aɴʏ Tᴇʟᴇɢʀᴀᴍ Mᴇᴅɪᴀ.

Cᴏᴍᴍᴀɴᴅs Aɴᴅ Usᴀɢᴇ:

• /link - Rᴇᴘʟʏ Tᴏ Aɴʏ Tᴇʟᴇɢʀᴀᴍ Mᴇᴅɪᴀ.
• /batch - Tᴏ Cʀᴇᴀᴛᴇ Lɪɴᴋ Fᴏʀ Mᴜʟᴛɪᴘʟᴇ Mᴇᴅɪᴀ.

Exᴀᴍᴘʟᴇ:
<code>/batch https://t.me/Binge_Pirates/1 
https://t.me/Binge_Pirates/9</code></b>"""

    KD_CNL = """<b>⍟ Cʜᴀɴɴᴇʟs & Gʀᴏᴜᴘs Mᴏᴅᴜʟᴇ ⍟</b>

<b>🎬 Cᴏᴍᴘʟᴇᴛᴇ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛɪɴɢ Gʀᴏᴜᴘ.
🚦 Aʟʟ Lᴀɴɢᴜᴀɢᴇs Mᴏᴠɪᴇs & Sᴇʀɪᴇs.
🗣️ Bᴏᴛ Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ.
📢 Bᴏᴛ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ.</b>"""

    FORCE_SUB = """
**⚠️ Pʟᴇᴀsᴇ Fᴏʟʟᴏᴡ Tʜɪs Rᴜʟᴇs ⚠️

Iɴ Oʀᴅᴇʀ Tᴏ Gᴇᴛ Tʜᴇ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛᴇᴅ Bʏ Yᴏᴜ.

Yᴏᴜ Wɪʟʟ Hᴀᴠᴇ Tᴏ Jᴏɪɴ Oᴜʀ Oғғɪᴄɪᴀʟ Cʜᴀɴɴᴇʟ Fɪʀsᴛ.

Aғᴛᴇʀ Tʜᴀᴛ Tʀʏ Aᴄᴄᴇssɪɴɢ Tʜᴀᴛ Mᴏᴠɪᴇ Tʜᴇɴ Cʟɪᴄᴋ Oɴ Tʜᴇ Tʀʏ Aɢᴀɪɴ.

I'ʟʟ Sᴇɴᴅ Yᴏᴜ Tʜᴀᴛ Mᴏᴠɪᴇ Pʀɪᴠᴀᴛᴇʟʏ.**
"""
    
    BANP_LOG_TXT = """<b>⍟ Bᴀɴɴᴇᴅ Usᴇʀ Lᴏɢs ⍟</b>

<b>Aᴅᴍɪɴ :</b> </b> <b>{}</b>

<b>Nᴀᴍᴇ :</b> <b>{}</b>

<b>Rᴇᴀsᴏɴ :</b> <code>{}</code>

<b>⍟ #BannedUser ⍟</b>
"""
    UNBANP_LOG_TXT = """<b>⍟ UɴBᴀɴɴᴇᴅ Usᴇʀ Lᴏɢs ⍟</b>

<b>Aᴅᴍɪɴ :</b> </b> <b>{}</b>

<b>Nᴀᴍᴇ :</b> <b>{}</b>

<b>⍟ #UnBannedUser ⍟</b>
"""
    BANG_LOG_TXT = """<b>⍟ Bᴀɴɴᴇᴅ Gʀᴏᴜᴘ Lᴏɢs ⍟</b>

<b>Cʜᴀᴛ ID :</b> <code>{}</code>

<b>Rᴇᴀsᴏɴ :</b> <code>{}</code>

<b>Aᴅᴍɪɴ :</b> </b> <b>{}</b>

<b>⍟ #BannedGroup ⍟</b>
"""
    UNBANG_LOG_TXT = """<b>⍟ UɴBᴀɴɴᴇᴅ Gʀᴏᴜᴘ Lᴏɢs ⍟</b>

<b>Cʜᴀᴛ ID :</b> <code>{}</code>

<b>Aᴅᴍɪɴ :</b> </b> <b>{}</b>

<b>⍟ #UnBannedGroup ⍟</b>
"""

    REQINFO2 = """⚠ Iɴғᴏʀᴍᴀᴛɪᴏɴ ⚠

Iғ Yᴏᴜ Dᴏ Nᴏᴛ Sᴇᴇ Tʜᴇ Rᴇǫᴜᴇsᴛᴇᴅ Mᴏᴠɪᴇ/Sᴇʀɪᴇs Fɪʟᴇ, Lᴏᴏᴋ Aᴛ Tʜᴇ Nᴇxᴛ Pᴀɢᴇ"""

    REQINFO = """⚠ Iɴғᴏʀᴍᴀᴛɪᴏɴ ⚠

Iғ Yᴏᴜ Dᴏ Nᴏᴛ Sᴇᴇ Tʜᴇ Rᴇǫᴜᴇsᴛᴇᴅ Mᴏᴠɪᴇ/Sᴇʀɪᴇs Fɪʟᴇ, Lᴏᴏᴋ Aᴛ Tʜᴇ Nᴇxᴛ Pᴀɢᴇ
"""

    MINFO = """
⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯
Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ Fᴏʀᴍᴀᴛ
⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯

Gᴏ Tᴏ Gᴏᴏɢʟᴇ ➠ Tʏᴘᴇ Mᴏᴠɪᴇ Nᴀᴍᴇ ➠ Cᴏᴘʏ Cᴏʀʀᴇᴄᴛ Nᴀᴍᴇ ➠ Pᴀsᴛᴇ Iɴ Tʜɪs Gʀᴏᴜᴘ

Exᴀᴍᴘʟᴇ : Black Adam 2022

🚯 Dᴏɴᴛ Uꜱᴇ ➠ ':(!,./)
"""

    SINFO = """
⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯
Sᴇʀɪᴇs Rᴇǫᴜᴇsᴛ Fᴏʀᴍᴀᴛ
⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯

Gᴏ Tᴏ Gᴏᴏɢʟᴇ ➠ Tʏᴘᴇ Sᴇʀɪᴇs Nᴀᴍᴇ ➠ Cᴏᴘʏ Cᴏʀʀᴇᴄᴛ Nᴀᴍᴇ ➠ Pᴀsᴛᴇ Iɴ Tʜɪs Gʀᴏᴜᴘ

Exᴀᴍᴘʟᴇ : Loki S01E01 Oʀ Loki S01 E01

🚯 Dᴏɴᴛ Uꜱᴇ ➠ ':(!,./)
"""

    PAGEINFO = """Pᴀɢᴇs Mᴇᴀɴs 10 Fɪʟᴇs Iɴ Oɴᴇ Pᴀɢᴇ

Iғ Yᴏᴜ Dᴏ Nᴏᴛ Sᴇᴇ Yᴏᴜʀ Fɪʟᴇs Oɴ Tʜɪs Pᴀɢᴇ Tʜᴇɴ Cʟɪᴄᴋ Oɴ Tʜᴇ Nᴇxᴛ Pᴀɢᴇ.

Pᴏᴡᴇʀᴇᴅ Bʏ :- Bɪɴɢᴇ Pɪʀᴀᴛᴇs
"""

    SPLMD = """Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ Fᴏʀᴍᴀᴛ

Exᴀᴍᴘʟᴇ : Black Adam 2022

Sᴇʀɪᴇs Rᴇǫᴜᴇsᴛ Fᴏʀᴍᴀᴛ

Exᴀᴍᴘʟᴇ : Loki S01E01 Oʀ Loki S01 E01

🚯Dᴏɴ'ᴛ Usᴇ ➠ ':(!,./)

Pᴏᴡᴇʀᴇᴅ Bʏ :- Bɪɴɢᴇ Pɪʀᴀᴛᴇs"""
    
    REQUEST_TXT = """<b>#PENDING
📫 Rᴇǫᴜᴇsᴛ Dᴇᴛᴀɪʟs :

🔖 Mᴇssᴀɢᴇ : <code>{}</code>

🕵️ Rᴇǫᴜᴇsᴛᴇᴅ Bʏ : {} [ <code>{}</code> ]</b>"""

    REQUEST2_TXT = """<b>Yᴏᴜʀ Rᴇǫᴜᴇsᴛ Hᴀs Bᴇᴇɴ Aᴅᴅᴇᴅ!
Pʟᴇᴀsᴇ Wᴀɪᴛ Fᴏʀ Sᴏᴍᴇ Tɪᴍᴇ.</b>"""

    SGROUP_TXT = """<b>Dᴇᴀʀ, {}

<code>{}</code> Rᴇsᴜʟᴛs Aʀᴇ Aʟʀᴇᴀᴅʏ Aᴠᴀɪʟᴀʙʟᴇ Fᴏʀ Yᴏᴜʀ Rᴇǫᴜᴇsᴛ <code>{}</code> Iɴ <a href=https://t.me/{}>Oᴜʀ Bᴏᴛ</a>.</b>
"""

    DONE_UPLOAD = """
Tʜᴇ Rᴇǫᴜᴇsᴛ Is Cᴏᴍᴘʟᴇᴛᴇᴅ !! Cʜᴇᴄᴋ Bᴏᴛ & Cʜᴀɴɴᴇʟ !!
"""

    REQ_REJECT = """
Tʜᴇ Rᴇǫᴜᴇsᴛ Is Rᴇᴊᴇᴄᴛᴇᴅ Mᴀʏʙᴇ Dᴜᴇ Tᴏ Sᴀᴍᴇ Rᴇǫᴜᴇsᴛ, Nᴏᴛ Iɴ Fᴏʀᴍᴀᴛ !!
"""

    REQ_NO = """
Tʜᴇ Rᴇǫᴜᴇsᴛ Is Nᴏᴛ Aᴠᴀɪʟᴀʙʟᴇ Mᴀʏʙᴇ Dᴜᴇ Tᴏ Nᴏᴛ Rᴇʟᴇᴀsᴇᴅ Oʀ Nᴏᴛ Aᴠᴀɪʟᴀʙʟᴇ !!
"""

    DONE_ALREADY = """
Tʜᴇ Rᴇǫᴜᴇsᴛ Is Aʟʀᴇᴀᴅʏ Uᴘʟᴏᴀᴅᴇᴅ !! Cʜᴇᴄᴋ Bᴏᴛ & Cʜᴀɴɴᴇʟ !!
""" 
    
    DONE_UPLOAD2 = """
<b>Yᴏᴜʀ Rᴇǫᴜᴇsᴛ Sᴜᴄᴇssғᴜʟʟʏ Uᴘʟᴏᴀᴅᴇᴅ Sᴇᴀʀᴄʜ Aɢᴀɪɴ..🙃</b>
"""

    REQ_REJECT2 = """
<b>Rᴇǫᴜᴇsᴛ Rᴇᴊᴇᴄᴛᴇᴅ 🚫 !!

Yᴏᴜʀ Rᴇǫᴜᴇsᴛ Aʟʀᴇᴀᴅʏ Mᴀʏʙᴇ Iɴ Tʜᴇ Rᴇǫᴜᴇsᴛ Lɪsᴛ Oʀ Yᴏᴜʀ Rᴇǫᴜᴇsᴛ Is Mᴀʟғᴏʀᴍᴀᴛᴛᴇᴅ. Kɪɴᴅʟʏ Rᴇǫᴜᴇsᴛ Aɢᴀɪɴ Oʀ Cᴏɴᴛᴀᴄᴛ Aᴅᴍɪɴ Fᴏʀ Hᴇʟᴘ.</b>
"""

    REQ_NO2 = """
<b>Sᴏʀʀʏ Yᴏᴜʀ Rᴇǫᴜᴇsᴛ Nᴏᴛ Aᴠᴀɪʟᴀʙʟᴇ 😔,
Kɪɴᴅʟʏ Cᴏɴᴛᴀᴄᴛ Aᴅᴍɪɴ Fᴏʀ Hᴇʟᴘ.</b>
"""

    DONE_ALREADY2 = """
<b>Rᴇǫᴜᴇsᴛ Aʟʀᴇᴀᴅʏ Uᴘʟᴏᴀᴅᴇᴅ ❗,
Kɪɴᴅʟʏ Cʜᴇᴄᴋ Tʜᴇ Bᴏᴛ Bᴇғᴏʀᴇ Rᴇǫᴜᴇsᴛɪɴɢ.</b>
"""

    CAP_DLT_TXT = """<b>Tʜᴇ Rᴇꜱᴜʟᴛꜱ Fᴏʀ ☞ <code>{}</code></b>
<b>Rᴇǫᴜᴇsᴛᴇᴅ Bʏ ☞ {}</b>"""

    CAP_TXT = """<b>Tʜᴇ Rᴇꜱᴜʟᴛꜱ Fᴏʀ ☞ <code>{}</code></b>
<b>Rᴇǫᴜᴇsᴛᴇᴅ Bʏ ☞ {}</b>
<b>Hᴇʏ Cʟɪᴄᴋ Oɴ Tʜᴇ Bᴜᴛᴛᴏɴ Bᴇʟᴏᴡ Tʜᴇ Fɪʟᴇs Yᴏᴜ Wᴀɴᴛ Aɴᴅ Sᴛᴀʀᴛ Tʜᴇ Bᴏᴛ.</b>
"""

    FILE_CHANNEL_TXT = """<b>🏷️ Tɪᴛʟᴇ :- <code>{}</code>

⚙️ Sɪᴢᴇ :- {}

🕵️‍♂️ Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :- {}

🔅 Pᴏᴡᴇʀᴇᴅ Bʏ :- Bɪɴɢᴇ Pɪʀᴀᴛᴇs</b>"""

    FILE_READY_TXT = """<b>Hᴇʏ {}
 
📫 Yᴏᴜʀ Fɪʟᴇ Is Sᴇɴᴛ Tᴏ Cʜᴀɴɴᴇʟ, 
Cʜᴇᴄᴋ Dᴏᴡɴ Tᴏ Vɪᴇᴡ.

📂 Fɪʟᴇ Nᴀᴍᴇ :- <code>{}</code>

⚙️ Fɪʟᴇ Sɪᴢᴇ :- {}</b>"""
