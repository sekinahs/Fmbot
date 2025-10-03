import re
from os import environ

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot information
SESSION = environ.get('SESSION', 'spidy')
API_ID = 20697817
API_HASH = "301dc2f99971593918d02c8378c7070c"
BOT_TOKEN ="7685914795:AAEVspQ92Wnbc_k_ZwTSZbOiUEYt7OMiFQI"

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))
PORT = environ.get("PORT", "8000")
TIMEZONE = environ.get("TIMEZONE", "Asia/Kolkata")

PICS = (environ.get('PICS', 'https://telegra.ph/file/72db861ea6e7ab287b81c-779b0d2731a0335110.jpg')).split()
NOR_IMG = environ.get("NOR_IMG", "")
SPELL_IMG = environ.get("SPELL_IMG", "")
NEWGRP = environ.get("NEWGRP", "")

# Admins, Channels & Users
ADMINS = [6319218715]
CHANNELS = [-1002929028097]
auth_users = []
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = -1002242030179
AUTH_GROUPS = [-1002242030179, -1002201035608]
FILDLT_CNL = [int(dch) if id_pattern.search(dch) else dch for dch in environ.get('FILDLT_CNL', '0').split()]

# MongoDB information
DATABASE_URI = "mongodb+srv://mu1820034:meow@cluster0.aqftnlw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

# Channel Button Links
GRP_LNK = environ.get('GRP_LINK' , 'https://t.me/FS_REQAIST_BOT')
CHNL_LNK = environ.get('CHNL_LNK', 'https://t.me/F5_FILMS')
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'https://t.me/FS_REQAIST_BOT')
MSG_ALRT = environ.get('MSG_ALRT', 'Share and Support Us')

# Custom Chats
SUPPORT_GROUP = -1002385998898
FILE_CHANNEL = int(environ.get('FILE_CHANNEL', 0))
FILE_CHANNEL_LINK = environ.get('FILE_CHANNEL_LINK', 'https://t.me/F5_FILMS')

# Log Channels
LOG_CHANNEL = -1002242030179
RQST_LOG_CHANNEL = -1002242030179

# Bot Options
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "True")), True)
IMDB = is_enabled((environ.get('IMDB', "False")), False)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", '''<b>Fɪʟᴇ Nᴀᴍᴇ :- {file_caption}

Fɪʟᴇ Sɪᴢᴇ :- {file_size}

🔅 Pᴏᴡᴇʀᴇᴅ Bʏ : <a href='https://t.me/Binge_Pirates'>Bɪɴɢᴇ Pɪʀᴀᴛᴇs</a></b>''')
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>{mention}'s Qᴜᴇʀʏ ☞ <code>{query}</code>\n\n<b>🏷 Tɪᴛʟᴇ</b> : <a href={url}>{title}</a>\n\n🌟 Rᴀᴛɪɴɢ : <a href={url}/ratings>{rating}</a> / 10\n\n💀 Rᴇʟᴇᴀsᴇ :  <b>{release_date}</b> <b>{countries}</b>\n\n🎭 Gᴇɴʀᴇs : <b>#{genres}</b></b>\n\n<b>🔅 Pᴏᴡᴇʀᴇᴅ Bʏ : <a href='https://t.me/Binge_Pirates'>Bɪɴɢᴇ Pɪʀᴀᴛᴇs</a></b>")
KD_IMDB_TEMPLATE = environ.get("KD_IMDB_TEMPLATE", "<b><b>🏷 Tɪᴛʟᴇ</b> : <a href={url}>{title}</a>\n\n🌟 Rᴀᴛɪɴɢ : <a href={url}/ratings>{rating}</a> / 10\n\n💀 Rᴇʟᴇᴀsᴇ :  <b>{release_date}</b> <b>{countries}</b>\n\n🎭 Gᴇɴʀᴇs : <b>{genres}</b></b>\n\n<b>📖 Sᴛᴏʀʏ Lɪɴᴇ :</b> <code>{plot}</code>\n\n<b>🔅 Pᴏᴡᴇʀᴇᴅ Bʏ : <a href='https://t.me/Binge_Pirates'>Bɪɴɢᴇ Pɪʀᴀᴛᴇs</a></b>")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "False"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "False")), True)

# Auto Delete , Filter & Auto Filter
AUTO_FFILTER = is_enabled((environ.get('AUTO_FFILTER', "True")), True)
AUTO_DELETE = is_enabled((environ.get('AUTO_DELETE', "False")), True)
MAUTO_DELETE = is_enabled((environ.get('MAUTO_DELETE', "False")), True)

# Delete Time
DELETE_TIME = int(environ.get('DELETE_TIME', 3600))
SPL_DELETE_TIME = int(environ.get('SPL_DELETE_TIME', 3600))

LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += ("SINGLE_BUTTON is Found, filename and files size will be shown in a single button instead of two separate buttons\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled , filename and file_sixe will be shown as different buttons\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled , Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode Is Enabled, bot will be suggesting related movies if movie not found\n" if SPELL_CHECK_REPLY else "SPELL_CHECK_REPLY Mode disabled\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
LOG_STR += f"Your current IMDB template is {IMDB_TEMPLATE}"
