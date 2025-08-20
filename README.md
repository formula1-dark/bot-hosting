# Crypto IDX Trading Signal Bot

An advanced AI-powered trading signal generator specifically designed for Crypto IDX trading on platforms like Binomo. This bot provides high-accuracy Up/Down signals with comprehensive risk management features, tailored for Indian users.

## ⚠️ Important Disclaimer

**Trading involves significant financial risk. This bot is for educational purposes only.**

- **No guaranteed profits** - All signals are predictions, not certainties
- **Risk of total capital loss** - Never trade more than you can afford to lose
- **Regulatory compliance** - Check local laws regarding binary options trading
- **Educational use** - This is not financial advice

## Features

### 🔍 Signal Generation
- **AI-powered analysis** using technical indicators (RSI, MACD, Bollinger Bands)
- **Real-time Crypto IDX data** simulation for signal generation
- **Confidence scoring** for each signal (50-95% accuracy estimation)

### 💰 Risk Management
- **Position sizing** based on confidence levels (₹100-₹500)
- **Loss streak protection** reduces position sizes after losses
- **Daily loss limits** to prevent excessive losses
- **Risk warnings** for low-confidence signals

### 📊 Trading Interface
- **Telegram bot** for easy access and notifications
- **Batch trading mode** - 10 trades per session
- **Trade history** with performance tracking
- **IST timezone** for Indian users

### 🛡️ Safety Features
- **Automated error handling** and recovery
- **No real money integration** - signals only
- **Configurable risk parameters**

## Installation

### Prerequisites
- Python 3.8 or higher
- Telegram Bot Token (provided in .env file)

### Setup

1. **Clone or download** the project files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   - Edit `.env` file with your Telegram bot token
   - Review settings in `config.py`

4. **Run the bot**:
   ```bash
   python crypto_idx_bot.py
   ```

## Usage

### Telegram Commands

- `/start` - Welcome message and bot overview
- `/help` - Detailed usage instructions
- `/signal` - Get individual trading signal
- `/batch` - Start batch trading mode (10 signals)
- `/history` - View recent trade history

### Signal Format

Each signal includes:
- **Direction**: 📈 UP or 📉 DOWN
- **Entry Time**: Precise IST timing
- **Suggested Amount**: ₹100-₹500 based on risk
- **Confidence**: Percentage accuracy estimate
- **Risk Level**: Low/Medium/High/Very High

### Example Signal
```
📈 UP Crypto IDX Signal

⏰ Entry Time: 21:06 IST
💰 Suggested Amount: ₹200
🎯 Confidence: 85%
📊 Risk Level: Low
✅ Risk: Acceptable

Action: Place trade before 21:06 IST
```

## Configuration

### Risk Settings (`config.py`)
```python
MIN_TRADE_AMOUNT = 100      # Minimum trade amount in ₹
MAX_TRADE_AMOUNT = 500      # Maximum trade amount in ₹
BATCH_SIZE = 10             # Trades per batch session
RISK_THRESHOLD = 70          # Minimum confidence for standard trades
```

### Telegram Settings
- Bot token configured in `.env` file
- No additional permissions required
- Works in private chats and groups

## File Structure

```
crypto-idx-bot/
├── crypto_idx_bot.py      # Main bot application
├── signal_generator.py    # AI signal generation
├── risk_manager.py       # Risk management system
├── trade_history.py      # Trade tracking and history
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── .env                # Environment variables
└── README.md          # This documentation
```

## Development

### Adding Real Data
To integrate real market data:
1. Replace `_generate_market_data()` in `signal_generator.py`
2. Add real API endpoints for Crypto IDX data
3. Implement proper data validation

### Custom Indicators
Add new technical indicators in `signal_generator.py`:
- Modify `_calculate_signal_strength()`
- Add new indicator calculation methods
- Update confidence weighting

## Troubleshooting

### Common Issues

**Bot not responding**:
- Check Telegram bot token in `.env`
- Ensure internet connectivity
- Verify bot is started with `/start`

**No signals generated**:
- Check system time is set to IST
- Verify all dependencies installed
- Check logs for errors

**Risk warnings**:
- Low confidence signals are normal
- Adjust RISK_THRESHOLD in config.py
- Consider market volatility

### Logs
- Check console output for detailed logs
- Error messages include timestamps
- Use DEBUG=True in .env for verbose logging

## Support

For issues or questions:
1. Check this README first
2. Review the `/help` command in Telegram
3. Check console logs for error details

## License

This project is for educational purposes. Use at your own risk.