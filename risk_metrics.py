import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

class RiskCalculator:
    def __init__(self):
        self.risk_free_rate = 0.05  # Assume 5% risk-free rate
        
    def calculate_risk_metrics(self, portfolio_data):
        """Calculate comprehensive risk metrics for the portfolio"""
        if portfolio_data.empty:
            return {}
        
        # Calculate portfolio weights
        total_value = portfolio_data['value_usd'].sum()
        portfolio_data = portfolio_data.copy()
        portfolio_data['weight'] = portfolio_data['value_usd'] / total_value
        
        # Basic risk metrics
        risk_metrics = {
            'portfolio_volatility': self._calculate_portfolio_volatility(portfolio_data),
            'sharpe_ratio': self._calculate_sharpe_ratio(portfolio_data),
            'max_drawdown': self._calculate_max_drawdown(portfolio_data),
            'var_95': self._calculate_var(portfolio_data, confidence=0.95),
            'cvar_95': self._calculate_cvar(portfolio_data, confidence=0.95),
            'concentration_risk': self._calculate_concentration_risk(portfolio_data),
            'diversification_ratio': self._calculate_diversification_ratio(portfolio_data),
            'token_weights': dict(zip(portfolio_data['symbol'], portfolio_data['weight']))
        }
        
        # Add correlation analysis
        correlation_metrics = self._analyze_correlations(portfolio_data)
        risk_metrics.update(correlation_metrics)
        
        return risk_metrics
    
    def _calculate_portfolio_volatility(self, portfolio_data):
        """Calculate portfolio volatility using historical data simulation"""
        # Since we don't have historical data, we'll simulate based on token characteristics
        symbols = portfolio_data['symbol'].tolist()
        weights = portfolio_data['weight'].tolist()
        
        # Simulate individual token volatilities based on token type
        token_volatilities = self._get_token_volatilities(symbols)
        
        # Calculate portfolio volatility (simplified)
        portfolio_variance = 0
        for i, (symbol, weight) in enumerate(zip(symbols, weights)):
            portfolio_variance += (weight ** 2) * (token_volatilities[i] ** 2)
        
        # Add correlation effects (simplified)
        correlation_factor = 0.3  # Assume average correlation of 0.3
        for i in range(len(symbols)):
            for j in range(i + 1, len(symbols)):
                portfolio_variance += 2 * weights[i] * weights[j] * token_volatilities[i] * token_volatilities[j] * correlation_factor
        
        return np.sqrt(portfolio_variance)
    
    def _get_token_volatilities(self, symbols):
        """Get estimated volatilities for tokens based on their characteristics"""
        # Base volatilities for different token types
        volatility_map = {
            'SOL': 0.6,      # High volatility
            'USDC': 0.01,    # Very low volatility (stablecoin)
            'USDT': 0.01,    # Very low volatility (stablecoin)
            'RAY': 0.8,      # Very high volatility (DeFi token)
            'SRM': 0.7,      # High volatility
            'ORCA': 0.75,    # High volatility
            'MNGO': 0.8,     # Very high volatility
            'STEP': 0.7,     # High volatility
            'COPE': 0.9,     # Very high volatility
            'FIDA': 0.8,     # Very high volatility
            'KIN': 0.6,      # High volatility
            'MAPS': 0.8,     # Very high volatility
            'OXY': 0.8,      # Very high volatility
            'PORT': 0.7,     # High volatility
            'ROPE': 0.8,     # Very high volatility
            'SAMO': 0.9,     # Very high volatility (meme token)
            'SLIM': 0.8,     # Very high volatility
            'SNY': 0.7,     # High volatility
            'TULIP': 0.8,    # Very high volatility
            'LIQ': 0.7       # High volatility
        }
        
        return [volatility_map.get(symbol, 0.5) for symbol in symbols]  # Default 50% volatility
    
    def _calculate_sharpe_ratio(self, portfolio_data):
        """Calculate Sharpe ratio for the portfolio"""
        # Simulate portfolio returns based on token characteristics
        symbols = portfolio_data['symbol'].tolist()
        weights = portfolio_data['weight'].tolist()
        
        # Get expected returns for each token
        expected_returns = self._get_expected_returns(symbols)
        
        # Calculate portfolio expected return
        portfolio_return = sum(weight * ret for weight, ret in zip(weights, expected_returns))
        
        # Calculate portfolio volatility
        portfolio_volatility = self._calculate_portfolio_volatility(portfolio_data)
        
        # Sharpe ratio = (Portfolio Return - Risk Free Rate) / Portfolio Volatility
        if portfolio_volatility > 0:
            return (portfolio_return - self.risk_free_rate) / portfolio_volatility
        else:
            return 0
    
    def _get_expected_returns(self, symbols):
        """Get expected returns for tokens based on their characteristics"""
        # Expected annual returns for different token types
        return_map = {
            'SOL': 0.15,     # 15% expected return
            'USDC': 0.03,    # 3% (near risk-free)
            'USDT': 0.03,    # 3% (near risk-free)
            'RAY': 0.25,     # 25% (high risk, high return)
            'SRM': 0.20,     # 20%
            'ORCA': 0.22,    # 22%
            'MNGO': 0.30,    # 30% (very high risk)
            'STEP': 0.20,    # 20%
            'COPE': 0.35,    # 35% (very high risk)
            'FIDA': 0.25,    # 25%
            'KIN': 0.15,     # 15%
            'MAPS': 0.25,    # 25%
            'OXY': 0.25,     # 25%
            'PORT': 0.20,    # 20%
            'ROPE': 0.30,    # 30%
            'SAMO': 0.40,    # 40% (meme token, very high risk)
            'SLIM': 0.25,    # 25%
            'SNY': 0.20,     # 20%
            'TULIP': 0.25,   # 25%
            'LIQ': 0.20      # 20%
        }
        
        return [return_map.get(symbol, 0.15) for symbol in symbols]  # Default 15% return
    
    def _calculate_max_drawdown(self, portfolio_data):
        """Calculate maximum drawdown (simplified)"""
        # This would typically use historical data
        # For now, estimate based on portfolio volatility
        portfolio_volatility = self._calculate_portfolio_volatility(portfolio_data)
        
        # Rough estimate: max drawdown is typically 2-3x the volatility
        return portfolio_volatility * 2.5
    
    def _calculate_var(self, portfolio_data, confidence=0.95):
        """Calculate Value at Risk (VaR)"""
        portfolio_volatility = self._calculate_portfolio_volatility(portfolio_data)
        portfolio_value = portfolio_data['value_usd'].sum()
        
        # VaR = portfolio_value * volatility * z_score
        z_score = stats.norm.ppf(1 - confidence)
        var = portfolio_value * portfolio_volatility * abs(z_score)
        
        return var
    
    def _calculate_cvar(self, portfolio_data, confidence=0.95):
        """Calculate Conditional Value at Risk (CVaR)"""
        var = self._calculate_var(portfolio_data, confidence)
        portfolio_volatility = self._calculate_portfolio_volatility(portfolio_data)
        
        # CVaR is typically 1.2-1.5x VaR for normal distributions
        cvar = var * 1.3
        
        return cvar
    
    def _calculate_concentration_risk(self, portfolio_data):
        """Calculate concentration risk using Herfindahl-Hirschman Index"""
        weights = portfolio_data['weight'].tolist()
        hhi = sum(weight ** 2 for weight in weights)
        
        if hhi > 0.25:
            return 'High'
        elif hhi > 0.15:
            return 'Medium'
        else:
            return 'Low'
    
    def _calculate_diversification_ratio(self, portfolio_data):
        """Calculate diversification ratio"""
        weights = portfolio_data['weight'].tolist()
        symbols = portfolio_data['symbol'].tolist()
        
        # Get individual volatilities
        individual_volatilities = self._get_token_volatilities(symbols)
        
        # Weighted average volatility
        weighted_avg_vol = sum(weight * vol for weight, vol in zip(weights, individual_volatilities))
        
        # Portfolio volatility
        portfolio_vol = self._calculate_portfolio_volatility(portfolio_data)
        
        # Diversification ratio = Weighted avg vol / Portfolio vol
        if portfolio_vol > 0:
            return weighted_avg_vol / portfolio_vol
        else:
            return 1.0
    
    def _analyze_correlations(self, portfolio_data):
        """Analyze token correlations and portfolio correlation risk"""
        symbols = portfolio_data['symbol'].tolist()
        n = len(symbols)
        
        if n < 2:
            return {
                'avg_correlation': 0,
                'max_correlation': 0,
                'correlation_risk': 'Low'
            }
        
        # Generate mock correlation matrix (in real implementation, use historical data)
        np.random.seed(42)
        correlation_matrix = np.random.rand(n, n)
        correlation_matrix = (correlation_matrix + correlation_matrix.T) / 2
        np.fill_diagonal(correlation_matrix, 1.0)
        
        # Calculate correlation metrics
        upper_triangle = np.triu(correlation_matrix, k=1)
        correlations = upper_triangle[upper_triangle != 0]
        
        avg_correlation = np.mean(correlations)
        max_correlation = np.max(correlations)
        
        # Assess correlation risk
        if avg_correlation > 0.7:
            correlation_risk = 'High'
        elif avg_correlation > 0.4:
            correlation_risk = 'Medium'
        else:
            correlation_risk = 'Low'
        
        return {
            'avg_correlation': avg_correlation,
            'max_correlation': max_correlation,
            'correlation_risk': correlation_risk,
            'correlation_matrix': correlation_matrix.tolist()
        }
    
    def calculate_portfolio_metrics(self, portfolio_data):
        """Calculate additional portfolio performance metrics"""
        if portfolio_data.empty:
            return {}
        
        total_value = portfolio_data['value_usd'].sum()
        portfolio_data = portfolio_data.copy()
        portfolio_data['weight'] = portfolio_data['value_usd'] / total_value
        
        # Calculate metrics
        metrics = {
            'total_value': total_value,
            'num_tokens': len(portfolio_data),
            'largest_position': portfolio_data['weight'].max(),
            'smallest_position': portfolio_data['weight'].min(),
            'position_std': portfolio_data['weight'].std(),
            'effective_number_of_positions': 1 / sum(portfolio_data['weight'] ** 2)
        }
        
        return metrics
