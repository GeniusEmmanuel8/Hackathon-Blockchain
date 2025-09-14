import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json

class PortfolioAnalyzer:
    def __init__(self, helius_api_key, coingecko_api_key=None):
        self.helius_api_key = helius_api_key
        self.coingecko_api_key = coingecko_api_key
        self.helius_base_url = "https://api.helius.xyz/v0"
        self.coingecko_base_url = "https://api.coingecko.com/api/v3"
        
    def get_portfolio_data(self, wallet_address, time_period="30 days"):
        """Fetch portfolio data from Helius API and enrich with price data"""
        try:
            # Get token accounts
            token_accounts = self._get_token_accounts(wallet_address)
            if not token_accounts:
                return None
            
            # Get token metadata and prices
            portfolio_data = self._enrich_with_prices(token_accounts)
            
            # Get historical data for risk analysis
            historical_data = self._get_historical_data(portfolio_data, time_period)
            
            return portfolio_data
            
        except Exception as e:
            print(f"Error fetching portfolio data: {e}")
            return None
    
    def _get_token_accounts(self, wallet_address):
        """Get token accounts for a wallet using Helius API"""
        url = f"{self.helius_base_url}/addresses/{wallet_address}/balances"
        params = {
            "api-key": self.helius_api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            token_accounts = []
            for token in data.get('tokens', []):
                if token.get('amount', 0) > 0:  # Only include tokens with balance
                    token_accounts.append({
                        'mint': token.get('mint'),
                        'amount': token.get('amount', 0),
                        'decimals': token.get('decimals', 9),
                        'symbol': token.get('symbol', 'Unknown'),
                        'name': token.get('name', 'Unknown Token'),
                        'price_usd': token.get('price', 0),
                        'value_usd': token.get('value', 0)
                    })
            
            return token_accounts
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching token accounts: {e}")
            return []
    
    def _enrich_with_prices(self, token_accounts):
        """Enrich token data with current prices from CoinGecko"""
        if not token_accounts:
            return pd.DataFrame()
        
        # Get unique token symbols for price lookup
        symbols = [token['symbol'] for token in token_accounts if token['symbol'] != 'Unknown']
        
        # Fetch prices from CoinGecko
        price_data = self._get_coingecko_prices(symbols)
        
        # Create portfolio DataFrame
        portfolio_data = []
        for token in token_accounts:
            symbol = token['symbol']
            price_usd = price_data.get(symbol, token.get('price_usd', 0))
            
            # Calculate actual token amount (considering decimals)
            actual_amount = token['amount'] / (10 ** token['decimals'])
            value_usd = actual_amount * price_usd
            
            portfolio_data.append({
                'mint': token['mint'],
                'symbol': symbol,
                'name': token['name'],
                'amount': actual_amount,
                'price_usd': price_usd,
                'value_usd': value_usd,
                'decimals': token['decimals']
            })
        
        return pd.DataFrame(portfolio_data)
    
    def _get_coingecko_prices(self, symbols):
        """Get current prices from CoinGecko API"""
        if not symbols:
            return {}
        
        # Map common Solana tokens to CoinGecko IDs
        token_mapping = {
            'SOL': 'solana',
            'USDC': 'usd-coin',
            'USDT': 'tether',
            'RAY': 'raydium',
            'SRM': 'serum',
            'ORCA': 'orca',
            'MNGO': 'mango-markets',
            'STEP': 'step-finance',
            'COPE': 'cope',
            'FIDA': 'bonfida',
            'KIN': 'kin',
            'MAPS': 'maps',
            'OXY': 'oxygen',
            'PORT': 'port-finance',
            'ROPE': 'rope',
            'SAMO': 'samoyedcoin',
            'SLIM': 'solanium',
            'SNY': 'synthetify-token',
            'TULIP': 'tulip-protocol',
            'LIQ': 'liq-protocol'
        }
        
        # Filter symbols that have CoinGecko mappings
        coingecko_ids = [token_mapping.get(symbol) for symbol in symbols if symbol in token_mapping]
        
        if not coingecko_ids:
            return {}
        
        url = f"{self.coingecko_base_url}/simple/price"
        params = {
            'ids': ','.join(coingecko_ids),
            'vs_currencies': 'usd',
            'include_24hr_change': 'true'
        }
        
        if self.coingecko_api_key:
            params['x_cg_demo_api_key'] = self.coingecko_api_key
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Map back to original symbols
            price_data = {}
            for symbol, coingecko_id in token_mapping.items():
                if coingecko_id in data:
                    price_data[symbol] = data[coingecko_id]['usd']
            
            return price_data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching prices from CoinGecko: {e}")
            return {}
    
    def _get_historical_data(self, portfolio_data, time_period):
        """Get historical price data for risk analysis"""
        # This would fetch historical data for backtesting
        # For now, we'll return mock data
        return {}
    
    def get_token_correlations(self, portfolio_data, time_period="30 days"):
        """Calculate token correlations for risk analysis"""
        if portfolio_data.empty:
            return pd.DataFrame()
        
        # This would calculate actual correlations using historical data
        # For now, return mock correlation matrix
        symbols = portfolio_data['symbol'].tolist()
        n = len(symbols)
        
        # Generate mock correlation matrix
        np.random.seed(42)  # For reproducible results
        correlation_matrix = np.random.rand(n, n)
        correlation_matrix = (correlation_matrix + correlation_matrix.T) / 2  # Make symmetric
        np.fill_diagonal(correlation_matrix, 1.0)  # Diagonal should be 1
        
        return pd.DataFrame(correlation_matrix, index=symbols, columns=symbols)
    
    def calculate_portfolio_concentration(self, portfolio_data):
        """Calculate portfolio concentration metrics"""
        if portfolio_data.empty:
            return {}
        
        total_value = portfolio_data['value_usd'].sum()
        portfolio_data['weight'] = portfolio_data['value_usd'] / total_value
        
        # Herfindahl-Hirschman Index (HHI) - measure of concentration
        hhi = (portfolio_data['weight'] ** 2).sum()
        
        # Largest position weight
        max_weight = portfolio_data['weight'].max()
        
        # Number of positions
        num_positions = len(portfolio_data)
        
        # Effective number of positions (inverse of HHI)
        effective_positions = 1 / hhi if hhi > 0 else 0
        
        return {
            'hhi': hhi,
            'max_weight': max_weight,
            'num_positions': num_positions,
            'effective_positions': effective_positions,
            'concentration_risk': 'High' if hhi > 0.25 else 'Medium' if hhi > 0.15 else 'Low'
        }
