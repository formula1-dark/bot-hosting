from config import Config
import math

class RiskManager:
    def __init__(self):
        self.max_daily_loss = 2000  # Maximum daily loss in ₹
        self.max_consecutive_losses = 3
        self.loss_streak = 0
        self.daily_loss = 0
        
    def assess_risk(self, signal_data):
        """
        Assess risk level for a given signal
        Returns dict with risk assessment
        """
        confidence = signal_data['confidence']
        
        # Risk levels based on confidence
        if confidence >= 85:
            risk_level = "Low"
            risk_score = 1
        elif confidence >= 75:
            risk_level = "Medium"
            risk_score = 2
        elif confidence >= 65:
            risk_level = "High"
            risk_score = 3
        else:
            risk_level = "Very High"
            risk_score = 4
            
        # Adjust for loss streak
        if self.loss_streak >= 2:
            risk_score += 1
            risk_level += " (Loss Streak)"
            
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'confidence': confidence,
            'recommended': confidence >= Config.RISK_THRESHOLD
        }
    
    def calculate_position_size(self, confidence, risk_level):
        """
        Calculate appropriate position size based on risk assessment
        """
        base_amount = Config.MIN_TRADE_AMOUNT
        max_amount = Config.MAX_TRADE_AMOUNT
        
        # Risk multiplier based on confidence
        if confidence >= 90:
            multiplier = 1.0
        elif confidence >= 80:
            multiplier = 0.8
        elif confidence >= 70:
            multiplier = 0.6
        elif confidence >= 60:
            multiplier = 0.4
        else:
            multiplier = 0.2
            
        # Adjust for loss streak
        if self.loss_streak >= 2:
            multiplier *= 0.5
            
        # Calculate final amount
        amount = base_amount + (max_amount - base_amount) * multiplier
        
        # Round to nearest 50
        amount = round(amount / 50) * 50
        
        # Ensure within bounds
        return max(Config.MIN_TRADE_AMOUNT, min(Config.MAX_TRADE_AMOUNT, int(amount)))
    
    def update_loss_streak(self, trade_result):
        """
        Update loss streak tracking
        trade_result: dict with 'profit_loss' key
        """
        if trade_result['profit_loss'] < 0:
            self.loss_streak += 1
            self.daily_loss += abs(trade_result['profit_loss'])
        else:
            self.loss_streak = 0
            
    def should_stop_trading(self):
        """
        Check if trading should be stopped due to risk limits
        """
        if self.daily_loss >= self.max_daily_loss:
            return True, "Daily loss limit reached"
            
        if self.loss_streak >= self.max_consecutive_losses:
            return True, f"{self.max_consecutive_losses} consecutive losses"
            
        return False, "Trading allowed"
    
    def reset_daily_limits(self):
        """Reset daily limits (call at start of new day)"""
        self.daily_loss = 0
        self.loss_streak = 0
        
    def get_risk_summary(self):
        """Get current risk status summary"""
        return {
            'daily_loss': self.daily_loss,
            'loss_streak': self.loss_streak,
            'max_daily_loss': self.max_daily_loss,
            'max_consecutive_losses': self.max_consecutive_losses
        }