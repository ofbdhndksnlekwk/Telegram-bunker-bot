import os
import logging
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

logging.basicConfig(level=logging.INFO)

# O'zingizning haqiqiy tokeningizni shu yerga yozing
BOT_TOKEN = "8710879281:AAGWM-UpJ0kjB5893YfhUbPr7_G8Wpf8nxc" 
ADMIN_USERNAME = "U_Z_BxG"
NETLIFY_URL = "https://haxi-agency.netlify.app"

if not BOT_TOKEN:
    exit("Xatolik: BOT_TOKEN topilmadi!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# --- BUNKER MA'LUMOTLAR BAZASI ---
PROFESSIONS = ["Shifokor", "Muhandis", "Olim", "Dasturchi", "Harbiy", "Oshpaz", "Agronom", "Psixolog", "Uchuvchi", "Ustoz"]
HEALTH_STATUS = ["100% sog'lom", "Yengil allergiya bor", "Ko'zi biroz xira", "Yuragi zaifroq", "Mutloq sog'lom, sportchi", "Surunkali charchoq"]
YOSH_ROYXATI = [21, 25, 28, 32, 35, 40, 45, 50, 19, 30]
HOBBIES = ["Kitob o'qish", "Yovvoyi tabiatni o'rganish", "Kamon otish", "Kimyoviy tajribalar", "Bog'dorchilik", "Yugurish", "Mexanika"]
PHOBIAS = ["Qorong'ulikdan qo'rqadi", "Yolg'izlik fobiya", "Balandlikdan qo'rqadi", "Suvdan qo'rqadi", "Hech qanday fobiyasi yo'q"]
SPECIAL_ITEMS = ["Tibbiy sumka", "Qurrollar qutisi", "1 yillik urug'lar to'plami", "Filtrlangan suv moslamasi", "Dasturlash kitobi", "Aloqa ratsiyasi"]

# TUGMALAR
def get_main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📂 Xizmatlar ko'rsatish", "📊 Statistika & Kafolat")
    kb.row("🌐 Bizning Sayt (Web App)", "🎮 Bunker o'yinini boshlash")
    return kb

def get_services_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🤖 Telegram Bot ($140 dan)", callback_data="serv_bot"),
        InlineKeyboardButton("🌐 Veb-Sayt ($200 dan)", callback_data="serv_web"),
        InlineKeyboardButton("🎬 AI Video Kliplar ($100 dan)", callback_data="serv_video"),
        InlineKeyboardButton("✨ Ijtimoiy Tarmoqlar ($70 dan)", callback_data="serv_smm")
    )
    return kb

def get_order_keyboard(service_name):
    text_msg = f"Assalomu alaykum, men premium {service_name} xizmatini buyurtma qilmoqchi edim."
    encoded_text = text_msg.replace(" ", "%20")
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🚀 Buyurtma berish (Telegram)", url=f"https://t.me/{ADMIN_USERNAME}?text={encoded_text}"),
        InlineKeyboardButton("⬅️ Xizmatlarga qaytish", callback_data="back_to_services")
    )
    return kb

# HANDLERS
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(
        "⚡ **HAXI AGENCY & BUNKER Ekosistemasiga Xush Kelibsiz!**\n\n"
        "Biznesingiz uchun premium AI yechimlarni taklif etamiz yoki do'stlaringiz bilan Bunker o'ynashingiz mumkin.\n\n"
        "🎮 *O'yinni guruhda boshlash uchun botni guruhga qo'shing va /bunker buyrug'ini yozing!*", 
        parse_mode="Markdown", reply_markup=get_main_menu()
    )

@dp.message_handler(lambda message: message.text == "📂 Xizmatlar ko'rsatish")
async def show_services(message: types.Message):
    await message.answer("👇 **Kerakli xizmatni tanlang:**", reply_markup=get_services_keyboard())

@dp.message_handler(lambda message: message.text == "📊 Statistika & Kafolat")
async def show_stats(message: types.Message):
    stats_text = "⚡ **HAXI AGENCY:**\n\n🌐 **5+ Yil** — Tajriba\n👥 **200+** — Mijozlar\n🚀 **200+** — Loyihalar\n🏆 **100%** — Kafolat"
    await message.answer(stats_text, parse_mode="Markdown")

@dp.message_handler(lambda message: message.text == "🌐 Bizning Sayt (Web App)")
async def show_webapp(message: types.Message):
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("💻 Saytni Ochish", web_app=WebAppInfo(url=NETLIFY_URL)))
    await message.answer("Premium saytimizni bot ichida ko'ring:", reply_markup=kb)

@dp.message_handler(lambda message: message.text == "🎮 Bunker o'yinini boshlash")
async def b_game_info(message: types.Message):
    await message.answer(
        "🎮 **Bunker o'yinini o'ynash tartibi:**\n\n"
        "1. Ushbu botni do'stlaringiz bilan ochgan **Guruh (Gruppa)**ga qo'shing.\n"
        "2. Guruh ichida `/bunker` buyrug'ini yozing.\n"
        "3. Bot har bir ishtirokchiga tasodifiy kiber-xarakter taqsimlaydi!"
    )

# --- BUNKER COMMAND HANDLER ---
@dp.message_handler(commands=['bunker'])
async def play_bunker(message: types.Message):
    if message.chat.type == "private":
        await message.answer("❌ Ushbu buyruqni faqat **guruhda** yozishingiz kerak, do'stlaringizni yig'ing!")
        return

    prof = random.choice(PROFESSIONS)
    health = random.choice(HEALTH_STATUS)
    age = random.choice(YOSH_ROYXATI)
    hobby = random.choice(HOBBIES)
    phobia = random.choice(PHOBIAS)
    item = random.choice(SPECIAL_ITEMS)

    bunker_msg = (
        f"🚨 **BUNKER APOKALIPSISI BOSHLANDI!** 🚨\n\n"
        f"👤 **Ism:** {message.from_user.full_name}\n"
        f"💼 **Kasbi:** {prof}\n"
        f"⏳ **Yoshi:** {age} yosh\n"
        f"❤️ **Sog'lig'i:** {health}\n"
        f"🎭 **Xobbi:** {hobby}\n"
        f"🧠 **Fobiya:** {phobia}\n"
        f"🎒 **Maxsus buyum:** {item}\n\n"
        f"💬 *Bunker ichida joy cheklangan! O'zingizni foydali ekanligingizni isbotlang!*"
    )
    await message.reply(bunker_msg, parse_mode="Markdown")

# CALLBACKS
@dp.callback_query_handler(lambda call: call.data.startswith("serv_"))
async def process_service_click(call: types.CallbackQuery):
    service = call.data.split("_")[1]
    titles = {"bot": ["Telegram Bot", "$140 dan"], "web": ["Veb-Sayt", "$200 dan"], "video": ["AI Video Kliplar", "$100 dan"], "smm": ["Ijtimoiy Tarmoqlar", "$70 dan"]}
    txt = f"🤖 **{titles[service][0]} Xizmati**\n\nPremium va kiber-yechimlar.\n\n💰 **Narxi:** {titles[service][1]}"
    await call.message.edit_text(txt, parse_mode="Markdown", reply_markup=get_order_keyboard(titles[service][0]))
    await call.answer()

@dp.callback_query_handler(lambda call: call.data == "back_to_services")
async def back_services(call: types.CallbackQuery):
    await call.message.edit_text("👇 **Kerakli xizmatni tanlang:**", reply_markup=get_services_keyboard())
    await call.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
    
