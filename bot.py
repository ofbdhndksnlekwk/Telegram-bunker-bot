import os
import logging
import random
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiohttp import web

logging.basicConfig(level=logging.INFO)

# TOKEN (To'g'ridan-to'g'ri o'zingizniki bilan almashtiring)
BOT_TOKEN = "8710879281:AAGWM-UpJ0kjB5893YfhUbPr7_G8Wpf8nxc" 
ADMIN_USERNAME = "U_Z_BxG"
NETLIFY_URL = "https://haxi-agency.netlify.app"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- BUNKER MA'LUMOTLAR BAZASI (KIBER-VARIANT) ---
PROFESSIONS = ["Shifokor", "Muhandis", "Olim", "Dasturchi", "Harbiy", "Oshpaz", "Agronom", "Psixolog", "Uchuvchi", "Ustoz"]
HEALTH_STATUS = ["100% sog'lom", "Yengil allergiya bor", "Ko'zi biroz xira", "Yuragi zaifroq", "Mutloq sog'lom, sportchi", "Surunkali charchoq"]
YOSH_RO'YXAT = [21, 25, 28, 32, 35, 40, 45, 50, 19, 30]
HOBBIES = ["Kitob o'qish", "Yovvoyi tabiatni o'rganish", "Kamon otish", "Kimyoviy tajribalar", "Bog'dorchilik", "Yugurish", "Mexanika"]
PHOBIAS = ["Qorong'ulikdan qo'rqadi", "Yolg'izlik fobiya", "Balandlikdan qo'rqadi", "Suvdan qo'rqadi", "Hech qanday fobiyasi yo'q"]
SPECIAL_ITEMS = ["Tibbiy sumka", "Qurrollar qutisi", "1 yillik urug'lar to'plami", "Filtrlangan suv moslamasi", "Dasturlash kitobi", "Aloqa ratsiyasi"]

# 1. ASOSIY MENYU TUGMALARI
def get_main_menu():
    kb = [
        [types.KeyboardButton(text="📂 Xizmatlar ko'rsatish"), types.KeyboardButton(text="📊 Statistika & Kafolat")],
        [types.KeyboardButton(text="🌐 Bizning Sayt (Web App)"), types.KeyboardButton(text="🎮 Bunker o'yinini boshlash")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_services_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤖 Telegram Bot ($140 dan)", callback_data="serv_bot")],
        [InlineKeyboardButton(text="🌐 Veb-Sayt ($200 dan)", callback_data="serv_web")],
        [InlineKeyboardButton(text="🎬 AI Video Kliplar ($100 dan)", callback_data="serv_video")],
        [InlineKeyboardButton(text="✨ Ijtimoiy Tarmoqlar ($70 dan)", callback_data="serv_smm")]
    ])

def get_order_keyboard(service_name):
    text_msg = f"Assalomu alaykum, men premium {service_name} xizmatini buyurtma qilmoqchi edim."
    encoded_text = text_msg.replace(" ", "%20")
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Buyurtma berish (Telegram)", url=f"https://t.me/{ADMIN_USERNAME}?text={encoded_text}")],
        [InlineKeyboardButton(text="⬅️ Xizmatlarga qaytish", callback_data="back_to_services")]
    ])

# 2. HANDLERS
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "⚡ **HAXI AGENCY & BUNKER Ekosistemasiga Xush Kelibsiz!**\n\n"
        "Bu yerda siz premium kiber-xizmatlar bilan tanishishingiz yoki do'stlaringiz bilan guruhda **Bunker** o'yinini o'ynashingiz mumkin!\n\n"
        "🎮 *O'yinni guruhda boshlash uchun botni guruhga qo'shing va /bunker buyrug'ini yozing!*", 
        parse_mode="Markdown", reply_markup=get_main_menu()
    )

@dp.message(F.text == "📂 Xizmatlar ko'rsatish")
async def show_services(message: types.Message):
    await message.answer("👇 **Kerakli xizmatni tanlang:**", reply_markup=get_services_keyboard())

@dp.message(F.text == "📊 Statistika & Kafolat")
async def show_stats(message: types.Message):
    stats_text = "⚡ **HAXI AGENCY:**\n\n🌐 **5+ Yil** — Tajriba\n👥 **200+** — Mijozlar\n🚀 **200+** — Loyihalar\n🏆 **100%** — Kafolat"
    await message.answer(stats_text, parse_mode="Markdown")

@dp.message(F.text == "🌐 Bizning Sayt (Web App)")
async def show_webapp(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💻 Saytni Ochish", web_app=WebAppInfo(url=NETLIFY_URL))]])
    await message.answer("Premium saytimizni bot ichida ko'ring:", reply_markup=kb)

@dp.message(F.text == "🎮 Bunker o'yinini boshlash")
async def b_game_info(message: types.Message):
    await message.answer(
        "🎮 **Bunker o'yinini o'ynash tartibi:**\n\n"
        "1. Ushbu botni do'stlaringiz bilan ochgan **Guruh (Gruppa)**ga qo'shing.\n"
        "2. Guruh ichida `/bunker` buyrug'ini yozing.\n"
        "3. Bot har bir ishtirokchiga tasodifiy xarakter taqsimlaydi va kiber-apokalipsis boshlanadi!"
    )

# --- BUNKER O'YINI LOGIKASI ---
@dp.message(Command("bunker"))
async def play_bunker(message: types.Message):
    # Guruh yoki shaxsiy chatligini tekshirish
    if message.chat.type == "private":
        await message.answer("❌ Ushbu buyruqni faqat **guruhda** yozishingiz kerak, do'stlaringizni yig'ing!")
        return

    # Tasodifiy xarakter generatsiyasi
    prof = random.choice(PROFESSIONS)
    health = random.choice(HEALTH_STATUS)
    age = random.choice(YOSH_RO'YXAT)
    hobby = random.choice(HOBBIES)
    phobia = random.choice(PHOBIAS)
    item = random.choice(SPECIAL_ITEMS)

    bunker_msg = (
        f"🚨 **BUNKER APOKALIPSISI BOSHLANDI!** 🚨\n\n"
        "Dunyo halokat yoqasida, siz bunker ostonasidasiz. Sizning xarakteringiz:\n\n"
        "👤 **Ism:** {message.from_user.full_name}\n"
        f"💼 **Kasbi:** {prof}\n"
        f"⏳ **Yoshi:** {age} yosh\n"
        f"❤️ **Sog'lig'i:** {health}\n"
        f"🎭 **Xobbi:** {hobby}\n"
        f"🧠 **Fobiya:** {phobia}\n"
        f"🎒 **Maxsus buyum:** {item}\n\n"
        f"💬 *Bunker ichida joy cheklangan! Guruhdagilarni o'zingizni foydali ekanligingizga ko'ndiring!*"
    )
    await message.reply(bunker_msg, parse_mode="Markdown")

# --- CALLBACKS ---
@dp.callback_query(F.data.startswith("serv_"))
async def process_service_click(callback: types.CallbackQuery):
    service = callback.data.split("_")[1]
    titles = {"bot": ["Telegram Bot", "$140 dan"], "web": ["Veb-Sayt", "$200 dan"], "video": ["AI Video Kliplar", "$100 dan"], "smm": ["Ijtimoiy Tarmoqlar", "$70 dan"]}
    txt = f"🤖 **{titles[service][0]} Xizmati**\n\nPremium va kiber-yechimlar.\n\n💰 **Narxi:** {titles[service][1]}"
    await callback.message.edit_text(txt, parse_mode="Markdown", reply_markup=get_order_keyboard(titles[service][0]))
    await callback.answer()

@dp.callback_query(F.data == "back_to_services")
async def back_services(callback: types.CallbackQuery):
    await callback.message.edit_text("👇 **Kerakli xizmatni tanlang:**", reply_markup=get_services_keyboard())
    await callback.answer()

# FEYK PORT WEB SERVER (Render o'chib qolmasligi uchun)
async def handle_index(request):
    return web.Response(text="Bot is live with Bunker Game!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_index)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(start_web_server())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
