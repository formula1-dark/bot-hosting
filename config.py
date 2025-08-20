import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Trading parameters
    MIN_TRADE_AMOUNT = 100
    MAX_TRADE_AMOUNT = 500
    BATCH_SIZE = 10
    RISK_THRESHOLD = 70  # percentage
    
    # Crypto IDX settings
    CRYPTO_IDX_SYMBOL = "CRYPTO_IDX"
    
    # Time settings (IST)
    TIMEZONE = 'Asia/Kolkata'
    
    # Signal generation parameters
    SIGNAL_COOLDOWN = 300  # seconds between signals
    ANALYSIS_WINDOW = 60  # minutes of data to analyze