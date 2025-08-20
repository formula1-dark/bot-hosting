import asyncio
import logging
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import Config
from signal_generator import SignalGenerator
from risk_manager import RiskManager
from trade_history import TradeHistory
import pytz

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class CryptoIDXBot:
    def __init__(self):
        self.signal_generator = SignalGenerator()
        self.risk_manager = RiskManager()
        self.trade_history = TradeHistory()
        self.active_batch = []
        self.batch_count = 0
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /start is issued."""
        welcome_message = """
🚀 **Crypto IDX Trading Bot**

Welcome! This bot provides AI-powered trading signals for Crypto IDX.

**Available Commands:**
/start - Show this welcome message
/signal - Get next trading signal
/batch - Start batch trading mode
/history - View trade history
/help - Show detailed help

**Important:** Trading involves risk. Only trade what you can afford to lose.
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /help is issued."""
        help_text = """
📊 **Help & Instructions**

**How to use:**
1. Use `/signal` to get individual trading signals
2. Use `/batch` to start 10-trade batch mode
3. Check `/history` to see past trades

**Enhanced Signal Features:**
- **Dynamic Duration**: 5, 10, or 15 minutes based on market volatility
- **Volatility Analysis**: Real-time market condition assessment
- **Expiry Time**: Exact trade closure time provided
- **Risk-Adjusted**: Duration optimized for current market conditions

**Risk Management:**
- Trade amounts: ₹100-₹500 per trade
- Low probability signals trigger warnings
- Automatic position sizing based on risk and volatility

**Signal Format:**
📈 **UP** or 📉 **DOWN**
⏰ **Entry & Expiry Time**: IST format
⏱️ **Trade Duration**: 5/10/15 minutes (dynamic)
💰 **Suggested Amount**: ₹100-₹500
📈 **Volatility**: Low/Medium/High
⚠️ **Risk Level**: Low/Medium/High
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def signal_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate and send a trading signal."""
        try:
            signal = await self.generate_signal()
            await update.message.reply_text(signal, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error generating signal: {e}")
            await update.message.reply_text("❌ Error generating signal. Please try again.")

    async def batch_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start batch trading mode."""
        if self.batch_count >= Config.BATCH_SIZE:
            self.batch_count = 0
            self.active_batch = []
            
        if len(self.active_batch) >= Config.BATCH_SIZE:
            await update.message.reply_text("📋 Batch complete! Use /batch to start new batch.")
            return
            
        await update.message.reply_text(f"🔄 Starting batch mode... {Config.BATCH_SIZE - len(self.active_batch)} trades remaining")
        
        for i in range(Config.BATCH_SIZE - len(self.active_batch)):
            signal = await self.generate_signal()
            await update.message.reply_text(signal, parse_mode='Markdown')
            self.active_batch.append(signal)
            
            if i < Config.BATCH_SIZE - 1:
                await asyncio.sleep(30)  # 30 second delay between signals
                
        self.batch_count += len(self.active_batch)

    async def history_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show trade history."""
        history = self.trade_history.get_recent_trades(5)
        if not history:
            await update.message.reply_text("📊 No trade history yet.")
            return
            
        history_text = "📈 **Recent Trades:**\n\n"
        for trade in history:
            history_text += f"{trade}\n\n"
            
        await update.message.reply_text(history_text, parse_mode='Markdown')

    async def generate_signal(self):
        """Generate a comprehensive trading signal with dynamic duration."""
        # Get current time in IST
        ist = pytz.timezone(Config.TIMEZONE)
        current_time = datetime.now(ist)
        
        # Generate signal data
        signal_data = self.signal_generator.generate_signal()
        risk_assessment = self.risk_manager.assess_risk(signal_data)
        
        # Determine trade amount
        suggested_amount = self.risk_manager.calculate_position_size(
            signal_data['confidence'], 
            risk_assessment['risk_level']
        )
        
        # Format signal message
        direction = "📈 UP" if signal_data['direction'] == 'UP' else "📉 DOWN"
        confidence = signal_data['confidence']
        duration = signal_data['duration']
        volatility = signal_data['volatility']
        
        # Calculate entry time (next 4 minutes)
        entry_time = current_time + timedelta(minutes=4)
        entry_str = entry_time.strftime("%H:%M IST")
        
        # Calculate expiry time
        expiry_time = entry_time + timedelta(minutes=duration)
        expiry_str = expiry_time.strftime("%H:%M IST")
        
        # Risk warning
        risk_warning = ""
        if confidence < Config.RISK_THRESHOLD:
            risk_warning = f"⚠️ **WARNING**: Low confidence signal ({confidence}%)"
        
        # Volatility indicator
        volatility_text = "Low" if volatility < 0.3 else "Medium" if volatility < 0.7 else "High"
        
        signal_message = f"""
{direction} **Crypto IDX Signal**

⏰ **Entry Time**: {entry_str}
⏱️ **Trade Duration**: {duration} minutes
🎯 **Expiry Time**: {expiry_str}
💰 **Suggested Amount**: ₹{suggested_amount}
📊 **Confidence**: {confidence}%
📈 **Volatility**: {volatility_text}
⚠️ **Risk Level**: {risk_assessment['risk_level']}

{risk_warning if risk_warning else "✅ **Risk**: Acceptable"}

**Action**: Place {duration}-minute trade before {entry_str}
        """
        
        return signal_message.strip()

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Log errors and notify user."""
        logger.error(msg="Exception while handling an update:", exc_info=context.error)
        
        if isinstance(update, Update) and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred. The bot is still running. Please try again."
            )

def main() -> None:
    """Start the bot."""
    if not Config.TELEGRAM_BOT_TOKEN:
        logger.error("No bot token provided!")
        return
        
    bot = CryptoIDXBot()
    application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("signal", bot.signal_command))
    application.add_handler(CommandHandler("batch", bot.batch_command))
    application.add_handler(CommandHandler("history", bot.history_command))
    
    # Add error handler
    application.add_error_handler(bot.error_handler)
    
    # Start the bot
    logger.info("Starting Crypto IDX Trading Bot...")
    application.run_polling()

if __name__ == '__main__':
    main()