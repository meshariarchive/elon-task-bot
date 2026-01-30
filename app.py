import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import db as dbmod
import roadmap as roadmapmod

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
DB_PATH = os.getenv("DB_PATH", "bot.db").strip()

if not TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN in .env")

# Database setup
_conn = dbmod.connect(DB_PATH)
dbmod.init_db(_conn)

def _safe_int(s: str):
    try:
        return int(s)
    except Exception:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ TaskBot is running.\n\n"
        "Commands:\n"
        "/new <task>  — create task + roadmap + Elon review\n"
        "/list        — list open tasks\n"
        "/task <id>   — view task details\n"
        "/done <id>   — mark task done"
    )

async def new_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = " ".join(context.args).strip()

    if not text:
        await update.message.reply_text(
            "Usage: /new <task text>\n"
        )
        return

    roadmap_v1 = roadmapmod.roadmap_v1(text)
    elon = roadmapmod.elon_review(text)

    task_id = dbmod.create_task(_conn, chat_id, text, roadmap_v1, elon)

    await update.message.reply_text(
        f"🧾 Created Task #{task_id}\n\n"
        f"{roadmap_v1}\n"
        f"{elon}\n\n"
        f"Next: /list or /done {task_id}"
    )

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    rows = dbmod.list_open_tasks(_conn, chat_id)

    if not rows:
        await update.message.reply_text("No open tasks ✅\nCreate one with: /new <task>")
        return

    lines = ["📌 Open tasks:"]
    for r in rows[:20]:
        lines.append(f"- #{r['id']} — {r['task_text']} (created {r['created_at']})")

    await update.message.reply_text("\n".join(lines))

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if not context.args:
        await update.message.reply_text("Usage: /done <id>")
        return

    task_id = _safe_int(context.args[0])
    if not task_id:
        await update.message.reply_text("Please provide a numeric id. Example: /done 3")
        return

    ok = dbmod.close_task(_conn, chat_id, task_id)
    if ok:
        await update.message.reply_text(f"✅ Task #{task_id} marked DONE.")
    else:
        await update.message.reply_text(
            f"Couldn’t close Task #{task_id}. (Not found or already done.)"
        )

async def task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if not context.args:
        await update.message.reply_text("Usage: /task <id>")
        return

    task_id = _safe_int(context.args[0])
    if not task_id:
        await update.message.reply_text("Please provide a numeric id. Example: /task 3")
        return

    t = dbmod.get_task(_conn, chat_id, task_id)
    if not t:
        await update.message.reply_text("Task not found.")
        return

    await update.message.reply_text(
        f"🧾 Task #{t['id']} ({t['status']})\n"
        f"Created: {t['created_at']}\n"
        f"Text: {t['task_text']}\n\n"
        f"{t['roadmap_v1']}\n"
        f"{t['elon_review']}"
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("new", new_task))
    app.add_handler(CommandHandler("list", list_tasks))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CommandHandler("task", task))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

