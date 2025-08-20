import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
from config import Config

class SignalGenerator:
    def __init__(self):
        self.data_points = 100  # Number of recent data points to analyze
        
    def generate_signal(self):
        """
        Generate a trading signal for Crypto IDX using simulated market data
        Includes dynamic trade duration recommendations based on volatility and signal strength
        """
        # Generate synthetic market data for demonstration
        market_data = self._generate_market_data()
        
        # Technical analysis indicators
        rsi = self._calculate_rsi(market_data)
        macd = self._calculate_macd(market_data)
        bb_position = self._calculate_bollinger_bands(market_data)
        
        # Calculate volatility for duration recommendations
        volatility = self._calculate_volatility(market_data)
        
        # Combine indicators for signal
        signal_strength = self._calculate_signal_strength(rsi, macd, bb_position)
        
        # Determine direction and confidence
        direction = "UP" if signal_strength > 0 else "DOWN"
        confidence = min(abs(signal_strength) * 20 + 60, 95)  # Scale to 60-95%
        
        # Add some randomness for realism
        confidence += random.uniform(-5, 5)
        confidence = max(50, min(95, confidence))
        
        # Calculate optimal trade duration
        duration = self._calculate_optimal_duration(volatility, abs(signal_strength), confidence)
        
        return {
            'direction': direction,
            'confidence': round(confidence, 1),
            'duration': duration,
            'volatility': volatility,
            'timestamp': datetime.now(),
            'indicators': {
                'rsi': rsi,
                'macd': macd,
                'bb_position': bb_position
            }
        }
    
    def _generate_market_data(self):
        """Generate synthetic Crypto IDX price data for testing"""
        np.random.seed(int(datetime.now().timestamp()))
        
        # Generate price series with trend
        trend = np.random.choice([-1, 1]) * np.random.uniform(0.1, 0.3)
        noise = np.random.normal(0, 0.5, self.data_points)
        
        prices = 100 + np.cumsum(trend + noise)
        return pd.Series(prices)
    
    def _calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]
    
    def _calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD indicator"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        
        return {
            'macd': macd_line.iloc[-1],
            'signal': signal_line.iloc[-1],
            'histogram': macd_line.iloc[-1] - signal_line.iloc[-1]
        }
    
    def _calculate_bollinger_bands(self, prices, period=20, std_dev=2):
        """Calculate Bollinger Bands position"""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        current_price = prices.iloc[-1]
        
        # Calculate position within bands (-1 to 1)
        band_range = upper_band.iloc[-1] - lower_band.iloc[-1]
        position = (current_price - lower_band.iloc[-1]) / band_range
        
        return max(-1, min(1, position))
    
    def _calculate_signal_strength(self, rsi, macd, bb_position):
        """Calculate overall signal strength based on indicators"""
        # RSI signal (oversold/overbought)
        rsi_signal = 0
        if rsi < 30:
            rsi_signal = 1  # Oversold, potential up
        elif rsi > 70:
            rsi_signal = -1  # Overbought, potential down
            
        # MACD signal
        macd_signal = 0
        if macd['histogram'] > 0:
            macd_signal = 1
        elif macd['histogram'] < 0:
            macd_signal = -1
            
        # Bollinger Bands signal
        bb_signal = 0
        if bb_position > 0.8:
            bb_signal = -1  # Near upper band
        elif bb_position < 0.2:
            bb_signal = 1  # Near lower band
            
        # Weighted combination
        weights = {'rsi': 0.3, 'macd': 0.4, 'bb': 0.3}
        signal_strength = (
            weights['rsi'] * rsi_signal +
            weights['macd'] * macd_signal +
            weights['bb'] * bb_signal
        )
        
        return signal_strength

    def _calculate_volatility(self, prices, period=20):
        """Calculate market volatility using ATR (Average True Range) concept"""
        if len(prices) < period:
            return 0.5  # Default moderate volatility
        
        # Calculate daily returns
        returns = prices.pct_change().dropna()
        
        # Calculate rolling standard deviation of returns
        volatility = returns.rolling(window=period).std()
        
        # Normalize volatility to 0-1 scale
        current_volatility = volatility.iloc[-1] if not volatility.empty else 0.02
        normalized_volatility = min(current_volatility * 50, 1.0)  # Scale factor
        
        return round(normalized_volatility, 3)

    def _calculate_optimal_duration(self, volatility, signal_strength, confidence):
        """
        Calculate optimal trade duration based on market conditions
        
        Logic:
        - High volatility + strong signal = shorter duration (5 min)
        - Low volatility + strong signal = longer duration (10 min)
        - Low confidence = medium duration (5 min)
        - High confidence + low volatility = longest duration (15 min)
        """
        
        # Base durations in minutes for binary options
        durations = [5, 10, 15]
        
        # Volatility factor (0-1 scale where 1 is high volatility)
        volatility_factor = volatility
        
        # Signal strength factor (0-1 scale)
        strength_factor = min(signal_strength, 1.0)
        
        # Confidence factor (0-1 scale)
        confidence_factor = confidence / 100
        
        # Calculate duration score
        # Lower score = shorter duration for high volatility
        # Higher score = longer duration for low volatility + high confidence
        duration_score = (
            (1 - volatility_factor) * 0.4 +      # Prefer longer in low volatility
            strength_factor * 0.3 +            # Strong signals can handle longer
            confidence_factor * 0.3            # High confidence allows longer
        )
        
        # Map score to duration
        if duration_score < 0.4:
            return 5  # Short duration for volatile/uncertain conditions
        elif duration_score < 0.7:
            return 10  # Medium duration for balanced conditions
        else:
            return 15  # Long duration for stable/confident conditions