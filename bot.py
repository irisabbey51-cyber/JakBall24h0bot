import os
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import sys

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get Bot Token from environment variable
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN not found in environment variables!")
    logger.error("Please add BOT_TOKEN to Railway environment variables")
    sys.exit(1)

CHANNEL_LINK = "https://t.me/CruptoDealss"
COINGECKO_API = "https://api.coingecko.com/api/v3"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when /start is issued."""
    user = update.effective_user
    welcome_message = f"""
🚀 *Welcome to JakBall24h0bot!* 🚀

Hi {user.first_name}! I'm your 24/7 crypto companion.

📊 *What I can do:*
• Real-time cryptocurrency prices
• Latest crypto news and updates
• Price tracking and alerts
• Blockchain updates

📈 *Quick Commands:*
/price - Get current crypto prices
/news - Latest crypto news
/settings - Customize your updates
/help - Show all commands

🔔 *Stay connected with our community:*
Join our channel for exclusive updates and deals!
    """
    
    keyboard = [
        [InlineKeyboardButton("📊 View Prices", callback_data='prices')],
        [InlineKeyboardButton("📰 Latest News", callback_data='news')],
        [InlineKeyboardButton("🔔 Join Our Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("⚙️ Settings", callback_data='settings')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message when /help is issued."""
    help_text = f"""
📚 *Available Commands:*

/start - Start the bot
/help - Show this help message
/price - Get current cryptocurrency prices
/news - Latest crypto news updates
/settings - Customize your preferences
/channel - Join our crypto channel

📊 *Price Commands:*
/price btc - Get Bitcoin price
/price eth - Get Ethereum price
/price all - Get top 10 cryptocurrencies

🔔 *You'll also receive:*
• Daily market summaries
• Price alerts (coming soon)
• Blockchain updates
• News notifications

*Join our channel for more:*
{CHANNEL_LINK}
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def get_crypto_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get cryptocurrency prices."""
    try:
        response = requests.get(
            f"{COINGECKO_API}/coins/markets",
            params={
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 5,
                'page': 1,
                'sparkline': False
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            price_message = "💰 *Top Cryptocurrency Prices* 💰\n\n"
            
            for coin in data:
                price_change = coin.get('price_change_percentage_24h', 0)
                price_message += f"• *{coin['name']} ({coin['symbol'].upper()})*\n"
                price_message += f"  💵 Price: ${coin['current_price']:,.2f}\n"
                price_message += f"  📈 24h Change: {price_change:.2f}%\n"
                price_message += f"  📊 Market Cap: ${coin['market_cap']:,.0f}\n\n"
            
            price_message += f"\n*Join our channel for more updates:*\n{CHANNEL_LINK}"
            
            keyboard = [
                [InlineKeyboardButton("🔄 Refresh Prices", callback_data='prices')],
                [InlineKeyboardButton("🔔 Join Channel", url=CHANNEL_LINK)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                price_message,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                "⚠️ Sorry, I couldn't fetch the prices right now. Please try again later."
            )
    except Exception as e:
        logger.error(f"Error fetching prices: {e}")
        await update.message.reply_text(
            "⚠️ An error occurred while fetching prices. Please try again later."
        )

async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get latest crypto news."""
    news_message = f"""
📰 *Latest Crypto News* 📰

*Top Headlines:*
1. Bitcoin ETF flows show positive momentum
2. Ethereum scaling solutions gaining adoption
3. DeFi protocols reach new TVL highs
4. Regulatory updates from major economies

*Market Sentiment:*
• Fear & Greed Index: 65 (Greed)
• 24h Trading Volume: $80B+
• Active Addresses: Rising

*🔔 For real-time news and updates, join our channel:*
{CHANNEL_LINK}

*Follow us for:*
• Breaking news alerts
• Price analysis
• Trading signals
• Educational content
    """
    
    keyboard = [
        [InlineKeyboardButton("📊 View Prices", callback_data='prices')],
        [InlineKeyboardButton("🔔 Join Channel", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        news_message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """User settings menu."""
    settings_text = f"""
⚙️ *Settings* ⚙️

Customize your crypto experience!

*Available Settings:*
• 📊 Price alerts
• 📰 News categories
• ⏰ Update frequency
• 🔔 Notification preferences

*Coming Soon:*
• Custom watchlists
• Portfolio tracking
• Advanced alerts

For immediate updates and support, join our channel:
{CHANNEL_LINK}
    """
    
    keyboard = [
        [InlineKeyboardButton("🔔 Set Price Alerts", callback_data='alerts')],
        [InlineKeyboardButton("📰 News Preferences", callback_data='news_pref')],
        [InlineKeyboardButton("🔗 Join Our Community", url=CHANNEL_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        settings_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Redirect to channel."""
    channel_message = f"""
🔔 *Join Our Crypto Channel!* 🔔

Get exclusive updates, deals, and insights:
{CHANNEL_LINK}

*What you'll get:*
• 💰 Daily crypto deals
• 📊 Market analysis
• 🚀 Early signals
• 🎯 Trading tips
• 📰 Breaking news

*Don't miss out on the next big opportunity!*
    """
    
    keyboard = [[InlineKeyboardButton("🚀 Join Now", url=CHANNEL_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        channel_message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'prices':
        # Create a new message with prices
        await get_crypto_price(update, context)
    elif query.data == 'news':
        await get_news(update, context)
    elif query.data == 'settings':
        await settings(update, context)
    elif query.data == 'alerts':
        await query.edit_message_text(
            f"🔔 *Price Alerts*\n\n"
            "Set up price alerts for your favorite cryptocurrencies.\n"
            "Coming soon! Stay tuned.\n\n"
            f"Join our channel for updates: {CHANNEL_LINK}",
            parse_mode='Markdown'
        )
    elif query.data == 'news_pref':
        await query.edit_message_text(
            f"📰 *News Preferences*\n\n"
            "Customize your news feed.\n"
            "Coming soon! Stay tuned.\n\n"
            f"Join our channel for updates: {CHANNEL_LINK}",
            parse_mode='Markdown'
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors."""
    logger.warning(f"Update {update} caused error {context.error}")

def main() -> None:
    """Start the bot."""
    try:
        logger.info("🤖 JakBall24h0bot is starting...")
        logger.info(f"Bot Token: {BOT_TOKEN[:10]}... (hidden for security)")
        
        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()

        # Register command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("price", get_crypto_price))
        application.add_handler(CommandHandler("news", get_news))
        application.add_handler(CommandHandler("settings", settings))
        application.add_handler(CommandHandler("channel", channel))
        
        # Register callback handler
        application.add_handler(CallbackQueryHandler(button_callback))
        
        # Register error handler
        application.add_error_handler(error_handler)

        # Get port from environment
        port = int(os.environ.get('PORT', 8080))
        
        # Start the bot using webhook for Railway
        logger.info(f"🚀 Starting bot with webhook on port {port}")
        
        # Run with webhook
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=BOT_TOKEN,
            webhook_url=None  # Let Railway handle the URL
        )
            
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
