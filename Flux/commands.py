from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from .database.mongo import insert, find_one

@Client.on_message(filters.private & filters.incoming & filters.command("about"))
async def about(bot, msg):
    await bot.send_message(
        msg.chat.id,
        Data.ABOUT,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons),
    )

@Client.on_message(filters.private & filters.incoming & filters.command("help"))
async def _help(bot, msg):
	id = msg.from_user.id
	ok = find_one(id)
	if ok:
		await bot.send_message(
			msg.chat.id,
			"**Here's how to use me **\n" + Data.HELP,
			reply_markup=InlineKeyboardMarkup(Data.home_buttons)
		)
	else:
		insert(id)
		await msg.reply_text(
			text=Data.HELP, 
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(Data.home_buttons)
		) 

@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def start(bot, msg):
	user = await bot.get_me()
	mention = user["mention"]
	await bot.send_message(
		msg.chat.id,
		Data.START.format(msg.from_user.mention, mention),
		reply_markup=InlineKeyboardMarkup(Data.buttons)
	)
