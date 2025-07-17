import os
import random
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    CallbackQueryHandler,
    filters
)

# Use environment variable for token in production, fallback to your test token
TOKEN = os.getenv('TELEGRAM_TOKEN', '7939794711:AAFBWBWSGCyVm6T0UJo9LVcmM1Gwm4VBsv0')

# Solana address validation pattern (basic format check)
SOLANA_PATTERN = re.compile(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$')

# Fake transaction IDs for Solscan
SOLSCAN_TXS = [
    "5vCf6VbM7dQ6Rj5qRhL3c2Tn2qL7iZ9nHcR8yW1aB3dE4xY5zX6wV7uJ8kK9oL0pI",
    "7dQ6Rj5qRhL3c2Tn2qL7iZ9nHcR8yW1aB3dE4xY5zX6wV7uJ8kK9oL0pI5vCf6VbM",
    "3c2Tn2qL7iZ9nHcR8yW1aB3dE4xY5zX6wV7uJ8kK9oL0pI5vCf6VbM7dQ6Rj5qRhL",
    "9nHcR8yW1aB3dE4xY5zX6wV7uJ8kK9oL0pI5vCf6VbM7dQ6Rj5qRhL3c2Tn2qL7iZ",
    "2qL7iZ9nHcR8yW1aB3dE4xY5zX6wV7uJ8kK9oL0pI5vCf6VbM7dQ6Rj5qRhL3c2Tn"
]

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/your_channel")],
        [InlineKeyboardButton("👥 Join Group", url="https://t.me/your_group")],
        [InlineKeyboardButton("🐦 Follow Twitter", url="https://twitter.com/your_twitter")],
        [InlineKeyboardButton("✅ Verify Tasks", callback_data="verify")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "🚀 Welcome to Airdrop Bot!\n\n"
        "Complete these tasks to participate:\n"
        "1. Join our Telegram channel\n"
        "2. Join our discussion group\n"
        "3. Follow us on Twitter\n\n"
        "Click VERIFY after completion:",
        reply_markup=reply_markup
    )

def handle_verification(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text("📝 Please send your Solana wallet address:")

def handle_solana_address(update: Update, context: CallbackContext) -> None:
    solana_address = update.message.text.strip()
    
    # Validate Solana address format
    if not SOLANA_PATTERN.match(solana_address):
        update.message.reply_text(
            "⚠️ Invalid Solana address format!\n"
            "• Should be 32-44 characters\n"
            "• Only contain these characters: 1-9A-HJ-NP-Za-km-z\n\n"
            "Please send a valid address:"
        )
        return

    # Select random transaction ID
    random_tx = random.choice(SOLSCAN_TXS)
    solscan_link = f"https://solscan.io/tx/{random_tx}"
    
    # Send fake success message
    update.message.reply_text(
        f"🎉 Congratulations! 1000 SOL is on its way to your wallet!\n\n"
        f"🔗 Transaction: {solscan_link}\n\n"
        f"Note: This is a test transaction. No actual SOL has been sent."
    )

def error_handler(update: Update, context: CallbackContext) -> None:
    """Log errors and send user-friendly message"""
    print(f"Update {update} caused error {context.error}")
    if update.message:
        update.message.reply_text("❌ An error occurred. Please try again or contact support.")

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(handle_verification, pattern="^verify$"))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_solana_address))
    
    # Error handler
    dispatcher.add_error_handler(error_handler)

    # Deployment configuration
    PORT = int(os.environ.get('PORT', 5000))
    RENDER_APP_NAME = os.environ.get('RENDER_APP_NAME')
    
    if RENDER_APP_NAME:  # Production (Webhook)
        print("Starting webhook mode...")
        updater.start_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            webhook_url=f"https://{RENDER_APP_NAME}.onrender.com/{TOKEN}"
        )
    else:  # Local development (Polling)
        print("Starting polling mode...")
        updater.start_polling()
        
    print("Bot is now running...")
    updater.idle()

if __name__ == '__main__':
    main()
