
import re
import json
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Konfigurasi Bot
TOKEN = "7806675718:AAGbK98ymtpMH4cusrmuYXbHIDenvvb5zF4"
GROUP_ID = -1002350897193
TOPIC_ID = 11

SAVE_SIGNAL_URL = "https://vvip.cuanity.id/save_signal.php"
WEBHOOK_URL = f"https://cuanitasbot.onrender.com/webhook"

def parse_signal(text):
    signal = {}
    patterns = {
        'token': r'#([A-Z]+USDT)',
        'entry': r'(?i)entry[:\s]*([\d.]+)',
        'sl': r'(?i)(stop ?loss|sl)[:\s]*([\d.]+)',
        'targets': r'(?i)targets[:\s]*([\d.\s\-]+)'
    }

    token_match = re.search(patterns['token'], text)
    if token_match:
        signal['token'] = token_match.group(1)

    entry_match = re.search(patterns['entry'], text)
    if entry_match:
        signal['entry'] = entry_match.group(1)

    sl_match = re.search(patterns['sl'], text)
    if sl_match:
        signal['sl'] = sl_match.group(2)

    targets_match = re.search(patterns['targets'], text)
    if targets_match:
        targets_text = targets_match.group(1)
        targets = re.findall(r'[\d.]+', targets_text)
        for i, value in enumerate(targets[:4]):
            signal[f'tp{i+1}'] = value

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

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.bot.set_webhook(WEBHOOK_URL)
    print("Webhook diset:", WEBHOOK_URL)
    await app.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=WEBHOOK_URL
    )

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
