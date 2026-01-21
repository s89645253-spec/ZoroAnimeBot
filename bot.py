import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Read token & admin ID from environment variables
BOT_TOKEN = os.environ.get("8407418440:AAEwSap53TUSP8Hy5kcbV9XjupLsTnOkLeQ")
ADMIN_ID = os.environ.get("6131989115")
if ADMIN_ID:
    ADMIN_ID = int(ADMIN_ID)  # convert to integer

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        file_id = context.args[0]
        try:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file_id
            )
        except:
            await update.message.reply_text("❌ File not found or expired.")
    else:
        await update.message.reply_text(
            "📦 Zoro Anime File Bot\n\n"
            "Send me anime episodes or files.\n"
            "I will generate a shareable link."
        )

# Handle files sent to bot
async def store_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if ADMIN_ID and update.effective_user.id != ADMIN_ID:
        return  # restrict uploads if ADMIN_ID set

    msg = update.message
    file_id = None

    # Check if user sent a document, video, or animation
    if msg.document:
        file_id = msg.document.file_id
    elif msg.video:
        file_id = msg.video.file_id
    elif msg.animation:
        file_id = msg.animation.file_id

    if file_id:
        # Generate shareable link
        link = f"https://t.me/{context.bot.username}?start={file_id}"
        await msg.reply_text(
            f"✅ File Stored Successfully!\n\n"
            f"📎 File ID:\n{file_id}\n\n"
            f"🔗 Share Link:\n{link}"
        )

# Main function
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, store_file))

    print("🤖 Zoro Anime File Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()