#!/usr/bin/env python3
"""
Demo script to test Crypto IDX Trading Bot functionality
This script demonstrates the core features without requiring Telegram
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from signal_generator import SignalGenerator
from risk_manager import RiskManager
from trade_history import TradeHistory
from datetime import datetime
import pytz

def test_signal_generation():
    """Test signal generation"""
    print("🔄 Testing Signal Generation...")
    
    generator = SignalGenerator()
    signal = generator.generate_signal()
    
    print(f"✅ Signal Generated:")
    print(f"   Direction: {signal['direction']}")
    print(f"   Confidence: {signal['confidence']}%")
    print(f"   Duration: {signal['duration']} minutes")
    print(f"   Volatility: {signal['volatility']}")
    print(f"   Indicators: {signal['indicators']}")
    print()

def test_risk_management():
    """Test risk management"""
    print("🔄 Testing Risk Management...")
    
    risk_manager = RiskManager()
    
    # Test with high confidence signal
    signal_data = {'confidence': 85}
    risk_assessment = risk_manager.assess_risk(signal_data)
    position_size = risk_manager.calculate_position_size(85, "Low")
    
    print(f"✅ Risk Assessment:")
    print(f"   Risk Level: {risk_assessment['risk_level']}")
    print(f"   Position Size: ₹{position_size}")
    print()

def test_trade_history():
    """Test trade history"""
    print("🔄 Testing Trade History...")
    
    history = TradeHistory()
    
    # Add some sample trades
    sample_trades = [
        {'direction': 'UP', 'amount': 200, 'result': 'WIN', 'profit_loss': 180},
        {'direction': 'DOWN', 'amount': 150, 'result': 'LOSS', 'profit_loss': -150},
        {'direction': 'UP', 'amount': 300, 'result': 'WIN', 'profit_loss': 270}
    ]
    
    for trade in sample_trades:
        history.add_trade(trade)
    
    print("✅ Trade History:")
    recent_trades = history.get_recent_trades(3)
    for trade in recent_trades:
        print(f"   {trade}")
    
    stats = history.get_statistics()
    print(f"\n📊 Statistics:")
    print(f"   Total Trades: {stats['total_trades']}")
    print(f"   Win Rate: {stats['win_rate']}%")
    print(f"   Total Profit: ₹{stats['total_profit']}")
    print()

def test_ist_timezone():
    """Test IST timezone handling"""
    print("🔄 Testing IST Timezone...")
    
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    
    print(f"✅ Current IST Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def main():
    """Run all tests"""
    print("🚀 Crypto IDX Trading Bot - Demo Test")
    print("=" * 50)
    print()
    
    try:
        test_ist_timezone()
        test_signal_generation()
        test_risk_management()
        test_trade_history()
        
        print("✅ All tests completed successfully!")
        print("\n📱 To start the Telegram bot:")
        print("   python crypto_idx_bot.py")
        print("\n⚠️  Remember: This is for educational purposes only!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())