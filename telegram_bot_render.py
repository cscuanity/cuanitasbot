
import re
import json
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Bot Configuration
TOKEN = "7806675718:AAGbK98ymtpMH4cusrmuYXbHIDenvvb5zF4"
GROUP_ID = -1002350897193
TOPIC_ID = 11  # Optional

# Webhook target (save_signal.php endpoint)
SAVE_SIGNAL_URL = "https://vvip.cuanity.id/save_signal.php"

def parse_signal(text):
    signal = {}
    patterns = {
        'token': r'#([A-Z]+USDT)',
        'entry': r'(?i)entry[:\s]*([\d.]+)',
        'sl': r'(?i)sl[:\s]*([\d.]+)',
        'tp1': r'(?i)tp ?1[:\s]*([\d.]+)',
        'tp2': r'(?i)tp ?2[:\s]*([\d.]+)',
        'tp3': r'(?i)tp ?3[:\s]*([\d.]+)',
        'tp4': r'(?i)tp ?4[:\s]*([\d.]+)'
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            signal[key] = match.group(1)
    return signal if 'entry' in signal and 'sl' in signal and 'token' in signal else None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != GROUP_ID:
        return
    if TOPIC_ID and update.message.message_thread_id != TOPIC_ID:
        return

    text = update.message.text
    if not text:
        return

    signal = parse_signal(text)
    if signal:
        try:
            response = requests.post(SAVE_SIGNAL_URL, data=signal)
            print("Sinyal dikirim:", signal)
            print("Response:", response.text)
        except Exception as e:
            print("Gagal mengirim sinyal:", e)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot Telegram berjalan...")
    app.run_polling()
