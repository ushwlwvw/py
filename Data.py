from pyrogram.types import InlineKeyboardButton


class Data:
    # Start Message
    START = """
مرحبًا {} مرحبًا بك في {} يمكنني
إنشاء جلسة سلسلة pyrogram و telethon. استخدم الزر أدناه
بواسطة: @aaaalqp
    """

    # Home Button
    home_buttons = [
        [InlineKeyboardButton("🔥 ابدا بانشاء الجلسة 🔥", callback_data="generate")],
        [InlineKeyboardButton(text="• ࢪجـوع •", callback_data="home")]
    ]

    generate_button = [
        [InlineKeyboardButton("🔥 ابدأ بانشاء الجلسة 🔥", callback_data="generate")]
    ]

    # Rest Buttons
    buttons = [
        [InlineKeyboardButton("🔥 ابدأ بانشاء الجلسة 🔥", callback_data="generate")],
        [InlineKeyboardButton(" • 𝗖𝗔𝗟𝗜𝗣𝗛  ›", url="https://t.me/aaaalqp")],
        [
            InlineKeyboardButton("كيفية الاستعمال ❔", callback_data="help"),
            InlineKeyboardButton("حول الـبوت 🚩", callback_data="about")
        ],
        [InlineKeyboardButton(" الحصول على مساعده↗️", url="https://t.me/aaaalqp")],
    ]

    # Help Message
    HELP = """
✨ اوامر البوت ✨

/about - حول البوت 

/help - المساعده

/start - بدء البوت

/generate - انشاء جلسة 

/cancel - الغاء العمليه 

/restart - اعادة تشغيل 
"""

    # About Message
    ABOUT = """
    ** حول هذا البوت**

روبوت تليجرام لإنشاء جلسة بيروجرام وسلسلة تيليثون بواسطة: @H_M_Dr

مقدم من : [اضغط هنا](https://t.me/aaaalqp)

نطاق : [Pyrogram](docs.pyrogram.org)

لغة : [Python](www.python.org)

المالك : @H_M_Dr
    """
