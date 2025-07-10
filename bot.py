import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)

# Configuration - Replace with your actual links
CHANNEL_LINK = "https://t.me/your_channel"  # Replace with your channel
GROUP_LINK = "https://t.me/your_group"  # Replace with your group
TWITTER_LINK = "https://twitter.com/your_profile"  # Replace with your Twitter

# Your Telegram bot token
BOT_TOKEN = "7672729386:AAERQa5Um_vGmh3rv-57djwxeFptOabnB9Y"

# Conversation states
JOIN, WALLET = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("👥 Group", url=GROUP_LINK)],
        [InlineKeyboardButton("🐦 Twitter", url=TWITTER_LINK)],
        [InlineKeyboardButton("✅ Done", callback_data="joined")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎉 Welcome to the SOL Airdrop Bot!\n\n"
        "To claim your 10 SOL:\n"
        "1. Join our official channel\n"
        "2. Join our community group\n"
        "3. Follow us on Twitter\n\n"
        "Click ✅ Done after completing all steps!",
        reply_markup=reply_markup
    )
    return JOIN

async def joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📥 Please send your Solana wallet address now:\n\n"
        "(Example: 7shw... or Solana domain name)"
    )
    return WALLET

async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallet_address = update.message.text
    # Fake transaction simulation
    await update.message.reply_text(
        f"🚀 Sending 10 SOL to your wallet...\n\n"
        f"✅ Transaction successful!\n"
        f"💳 Wallet: `{wallet_address}`\n"
        f"💸 Amount: 10 SOL\n\n"
        f"🎉 Congratulations! Check your wallet.\n\n"
        f"Note: This is a test transaction. No actual SOL was sent.",
        parse_mode="Markdown"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Airdrop process cancelled.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            JOIN: [CallbackQueryHandler(joined, pattern="^joined$")],
            WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, wallet)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    app.add_handler(conv_handler)
    
    # Render.com deployment setup
    if "RENDER" in os.environ:
        port = int(os.environ.get("PORT", 5000))
        webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"
        
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=BOT_TOKEN,
            webhook_url=f"{webhook_url}/{BOT_TOKEN}"
        )
    else:
        print("🤖 Bot running in polling mode...")
        app.run_polling()

if __name__ == "__main__":
    main()
