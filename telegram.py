import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext

TOKEN = 'TOKEN BURAYA'

# API URLLERİ BURAYA DAHA DÜZENLİ YANIT İÇİN GELİŞTİRİRSİNZ SADECE APİ YANITINI ATAR
API_URLS = {
"TC": "APILERI BURAYA YAZ",
"Aile": "APILERI BURAYA YAZ",
"Sulale": "APILERI BURAYA YAZ",
"Tc GSM": "APILERI BURAYA YAZ",
"GSM TC": "APILERI BURAYA YAZ",
"TC Pro": "APILERI BURAYA YAZ",
"IBAN": "APILERI BURAYA YAZ",
"Kızlık Soyadı": "APILERI BURAYA YAZ",
"Operatör": "APILERI BURAYA YAZ",
"Serino": "APILERI BURAYA YAZ",
"Sicil": "APILERI BURAYA YAZ",
"SMS Bomber": "APILERI BURAYA YAZ",
"Ayak": "APILERI BURAYA YAZ",
"Yarrak ve Boy": "APILERI BURAYA YAZ",
"IP Sorgu": "APILERI BURAYA YAZ",
"Anne Baba": "APILERI BURAYA YAZ",
"Çocuk": "APILERI BURAYA YAZ",
"Kardeş": "APILERI BURAYA YAZ",
"Kuzen": "APILERI BURAYA YAZ",
"Yeğen": "APILERI BURAYA YAZ",
"Full": "APILERI BURAYA YAZ",
"Ad Soyad": "APILERI BURAYA YAZ",
"Ad Soyad İl": "APILERI BURAYA YAZ",
"Ad Soyad İl İlçe": "APILERI BURAYA YAZ",
"Adres": "APILERI BURAYA YAZ",
}

# Hoş geldin mesajı burada düzenlersin
WELCOME_MESSAGE = (
"Merhaba! @zeus289x 🌟\n\n"
"Benimle çeşitli sorgular yapabilirsiniz. Aşağıdaki seçeneklerden birini seçin ve gerekli bilgileri girin:\n\n"
"Başlamak için lütfen bir seçenek belirleyin! 🇹🇷"
)

async def start(update: Update, context: CallbackContext):
keyboard = [
[InlineKeyboardButton("📋 TC Sorgula", callback_data='TC')],
[InlineKeyboardButton("👪 Aile Bilgileri", callback_data='Aile')],
[InlineKeyboardButton("🌳 Sulale", callback_data='Sulale')],
[InlineKeyboardButton("📱 TC GSM", callback_data='Tc GSM')],
[InlineKeyboardButton("📞 GSM TC", callback_data='GSM TC')],
[InlineKeyboardButton("🔑 TC Pro", callback_data='TC Pro')],
[InlineKeyboardButton("🏦 IBAN", callback_data='IBAN')],
[InlineKeyboardButton("💼 Kızlık Soyadı", callback_data='Kızlık Soyadı')],
[InlineKeyboardButton("📞 Operatör", callback_data='Operatör')],
[InlineKeyboardButton("🔢 Serino", callback_data='Serino')],
[InlineKeyboardButton("📜 Sicil", callback_data='Sicil')],
[InlineKeyboardButton("📲 SMS Bomber", callback_data='SMS Bomber')],
[InlineKeyboardButton("👣 Ayak", callback_data='Ayak')],
[InlineKeyboardButton("📏 Yarrak ve Boy", callback_data='Yarrak ve Boy')],
[InlineKeyboardButton("🌐 IP Sorgu", callback_data='IP Sorgu')],
[InlineKeyboardButton("👨‍👩‍👧‍👦 Anne Baba", callback_data='Anne Baba')],
[InlineKeyboardButton("👶 Çocuk", callback_data='Çocuk')],
[InlineKeyboardButton("👫 Kardeş", callback_data='Kardeş')],
[InlineKeyboardButton("👨‍👩‍👧 Kuzen", callback_data='Kuzen')],
[InlineKeyboardButton("👦 Yeğen", callback_data='Yeğen')],
[InlineKeyboardButton("🔍 Full Sorgu", callback_data='Full')],
[InlineKeyboardButton("📝 Ad Soyad", callback_data='Ad Soyad')],
[InlineKeyboardButton("📍 Ad Soyad İl", callback_data='Ad Soyad İl')],
[InlineKeyboardButton("📍 Ad Soyad İl İlçe", callback_data='Ad Soyad İl İlçe')],
[InlineKeyboardButton("🏠 Adres", callback_data='Adres')],
]
reply_markup = InlineKeyboardMarkup(keyboard)
await update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext):
query = update.callback_query
await query.answer()
data = query.data

await query.edit_message_text(text=f"{data} sorgusu yapmak için gerekli bilgileri girin.")
context.user_data['current_query'] = data

async def handle_message(update: Update, context: CallbackContext):
text = update.message.text
query_type = context.user_data.get('current_query')

if not query_type:
await update.message.reply_text("Önce bir sorgu seçmelisiniz. /start komutunu kullanın.")
return

params = {}
if query_type == "Ad Soyad":
parts = text.split(' ')
if len(parts) &lt; 2:
await update.message.reply_text("Ad ve soyadı doğru formatta girin: Ad Soyad")
return
params = {"ad": parts[0], "soyad": parts[1]}
elif query_type == "Ad Soyad İl":
parts = text.split(' ')
if len(parts) &lt; 3:
await update.message.reply_text("Ad, soyad ve il bilgisini doğru formatta girin: Ad Soyad İl")
return
params = {"ad": parts[0], "soyad": parts[1], "il": parts[2]}
elif query_type == "Ad Soyad İl İlçe":
parts = text.split(' ')
if len(parts) &lt; 4:
await update.message.reply_text("Ad, soyad, il ve ilçe bilgisini doğru formatta girin: Ad Soyad İl İlçe")
return
params = {"ad": parts[0], "soyad": parts[1], "il": parts[2], "ilce": parts[3]}
else:
if query_type in ["GSM TC", "Operatör"]:
params = {"gsm": text}
else:
params = {"tc": text}

api_url = API_URLS.get(query_type).format(**params)
response = requests.get(api_url)
result = response.json()

await update.message.reply_text(f"API yanıtı:\n{result}")

def main():
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button))
application.add_handler(MessageHandler(filters.TEXT &amp; ~filters.COMMAND, handle_message))

application.run_polling()

if __name__ == '__main__':
main()arts) < 2:
            await update.message.reply_text("Ad ve soyadı doğru formatta girin: Ad Soyad")
            return
        params = {"ad": parts[0], "soyad": parts[1]}
    elif query_type == "Ad Soyad İl":
        parts = text.split(' ')
        if len(parts) < 3:
            await update.message.reply_text("Ad, soyad ve il bilgisini doğru formatta girin: Ad Soyad İl")
            return
        params = {"ad": parts[0], "soyad": parts[1], "il": parts[2]}
    elif query_type == "Ad Soyad İl İlçe":
        parts = text.split(' ')
        if len(parts) < 4:
            await update.message.reply_text("Ad, soyad, il ve ilçe bilgisini doğru formatta girin: Ad Soyad İl İlçe")
            return
        params = {"ad": parts[0], "soyad": parts[1], "il": parts[2], "ilce": parts[3]}
    else:
        if query_type in ["GSM TC", "Operatör"]:
            params = {"gsm": text}
        else:
            params = {"tc": text}

    api_url = API_URLS.get(query_type).format(**params)
    response = requests.get(api_url)
    result = response.json()
    
    await update.message.reply_text(f"API yanıtı:\n{result}")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()