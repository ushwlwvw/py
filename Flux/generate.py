from asyncio.exceptions import TimeoutError
from Data import Data
from pyrogram import Client, filters
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)


@Client.on_message(filters.private & ~filters.forwarded & filters.command('generate'))
async def main(_, msg):
    await msg.reply(
        "الرجاء اختيار مكتبة python التي تريد إنشاء جلسة سلسلة لها",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("• بايروجرام •", callback_data="pyrogram"),
            InlineKeyboardButton("• تيليثون •", callback_data="telethon")
        ]])
    )


async def generate_session(bot, msg, telethon=False):
    await msg.reply("جارٍ بدء {} إنشاء الجلسة ...".format("Telethon" if telethon else "Pyrogram"))
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, 'الرجاء ارسال `API_ID`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply('ليس صحيحا API_ID (الذي يجب أن يكون عددًا صحيحًا). يرجى البدء في إنشاء الجلسة مرة أخرى.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    api_hash_msg = await bot.ask(user_id, 'الرجاء لرسال `API_HASH`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(user_id, 'ارسل الان  `رقم حسابك` مع رمز الدوله \nمثال : `+19876543210`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("Sending OTP.....")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    else:
        client = Client(":memory:", api_id, api_hash)
    await client.connect()
    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply('`API_ID` و `API_HASH` غير صالحين. يرجى البدء في إنشاء الجلسة مرة أخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply('`رقم حسابك `غير صالح. يرجى البدء في إنشاء الجلسة مرة أخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    try:
        phone_code_msg = await bot.ask(user_id, 'يرجى التحقق من وجود رمز في تطبيق Telegram . \n\nإذا حصلت عليه ، أرسل الرمز هنا بعد اقراء \nإذا كان الرمز هو `12345`, **من فضلك أرسلها كـ** `1 2 3 4 5`.", filters=filters.text, timeout=600)
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply('بلغ الحد الزمني 10 دقائق. يرجى البدء في إنشاء الجلسة مرة أخرى', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply('الرمز غير صالح. يرجى البدء في إنشاء الجلسة مرة أخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply('انتهت صلاحية كلمة المرور لمرة واحدة. يرجى البدء في إنشاء الجلسة مرة أخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(user_id, 'لقد مكّن حسابك التحقق بخطوتين. يرجى تقديم كلمة المرور.', filters=filters.text, timeout=300)
        except TimeoutError:
            await msg.reply('بلغ الحد الزمني 5 دقائق. يرجى البدء في إنشاء الجلسة مرة أخرى.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        try:
            password = two_step_msg.text
            if telethon:
                await client.sign_in(password=password)
            else:
                await client.check_password(password=password)
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msgInvalid Password Provided. Please start generating session again.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
.reply('أدخلت كلمة مرور غير صالحة. يرجى البدء في إنشاء الجلسة مرة أخرى.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = "**{} سلسلة جلسة** \n\n`{}` \n\n : تم إنشاؤها بواسطة @aaaalqp".format("TELETHON" if telethon else "PYROGRAM", string_session)
    try:
        await client.send_message("me", text)
    except KeyError:
        pass
    await client.disconnect()
    await phone_code_msg.reply("تم إنشاء جلسة سلسلة {} بنجاح. \n\nيرجى التحقق من رسائلك المحفوظة! \n\nبواسطة : @aaaalqp ".format("telethon" if telethon else "pyrogram"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("ألغيت العملية!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("أعادة تشغيل الروبوت!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("ألغيت العملية!", quote=True)
        return True
    else:
        return False
