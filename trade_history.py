import json
import os
from datetime import datetime
import pytz
from config import Config

class TradeHistory:
    def __init__(self):
        self.history_file = 'trade_history.json'
        self.max_history_size = 1000
        self.trades = self._load_history()
        
    def _load_history(self):
        """Load trade history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_history(self):
        """Save trade history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.trades[-self.max_history_size:], f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def add_trade(self, trade_data):
        """
        Add a new trade to history
        trade_data: dict with trade details
        """
        ist = pytz.timezone(Config.TIMEZONE)
        trade_data['timestamp'] = datetime.now(ist).isoformat()
        trade_data['trade_id'] = len(self.trades) + 1
        
        self.trades.append(trade_data)
        self._save_history()
        
    def get_recent_trades(self, count=10):
        """Get recent trades"""
        recent = self.trades[-count:]
        formatted_trades = []
        
        for trade in recent:
            timestamp = trade.get('timestamp', 'Unknown')
            direction = trade.get('direction', 'Unknown')
            amount = trade.get('amount', 0)
            result = trade.get('result', 'Unknown')
            profit_loss = trade.get('profit_loss', 0)
            duration = trade.get('duration', 5)
            
            # Format for display
            status_emoji = "✅" if profit_loss >= 0 else "❌"
            profit_text = f"₹{abs(profit_loss)}"
            
            formatted_trade = (
                f"{status_emoji} **{direction}** - ₹{amount} - {duration}min\n"
                f"📅 {timestamp[:16]}\n"
                f"💰 **Result**: {profit_text} {'Profit' if profit_loss >= 0 else 'Loss'}"
            )
            formatted_trades.append(formatted_trade)
            
        return formatted_trades
    
    def get_statistics(self):
        """Get trading statistics"""
        if not self.trades:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'total_profit': 0,
                'average_profit': 0,
                'largest_win': 0,
                'largest_loss': 0
            }
        
        total_trades = len(self.trades)
        winning_trades = [t for t in self.trades if t.get('profit_loss', 0) >= 0]
        losing_trades = [t for t in self.trades if t.get('profit_loss', 0) < 0]
        
        win_rate = (len(winning_trades) / total_trades) * 100 if total_trades > 0 else 0
        total_profit = sum(t.get('profit_loss', 0) for t in self.trades)
        average_profit = total_profit / total_trades if total_trades > 0 else 0
        
        largest_win = max([t.get('profit_loss', 0) for t in self.trades], default=0)
        largest_loss = min([t.get('profit_loss', 0) for t in self.trades], default=0)
        
        return {
            'total_trades': total_trades,
            'win_rate': round(win_rate, 2),
            'total_profit': round(total_profit, 2),
            'average_profit': round(average_profit, 2),
            'largest_win': largest_win,
            'largest_loss': largest_loss,
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades)
        }
    
    def get_daily_summary(self, date=None):
        """Get summary for a specific date"""
        if date is None:
            ist = pytz.timezone(Config.TIMEZONE)
            date = datetime.now(ist).date()
            
        date_str = str(date)
        daily_trades = [t for t in self.trades if t.get('timestamp', '').startswith(date_str)]
        
        if not daily_trades:
            return None
            
        total_profit = sum(t.get('profit_loss', 0) for t in daily_trades)
        win_rate = (len([t for t in daily_trades if t.get('profit_loss', 0) >= 0]) / len(daily_trades)) * 100
        
        return {
            'date': date_str,
            'trades': len(daily_trades),
            'profit': total_profit,
            'win_rate': round(win_rate, 2)
        }
    
    def clear_history(self):
        """Clear all trade history"""
        self.trades = []
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
    
    def export_history(self, filename=None):
        """Export trade history to CSV"""
        if filename is None:
            filename = f'trade_history_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            
        if not self.trades:
            return None
            
        import csv
        
        with open(filename, 'w', newline='') as csvfile:
            if self.trades:
                fieldnames = self.trades[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.trades)
                
        return filename