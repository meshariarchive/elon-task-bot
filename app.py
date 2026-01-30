import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("bot")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Alive. Use /new <task>.")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("pong")

def main():
    log.info("BOOT: starting…")
    log.info("BOOT: TOKEN_SET=%s LEN=%s", bool(TELEGRAM_BOT_TOKEN), len(TELEGRAM_BOT_TOKEN))

    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN env var on server")

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))

    log.info("BOOT: polling…")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

