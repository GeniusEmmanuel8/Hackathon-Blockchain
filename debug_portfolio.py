#!/usr/bin/env python3
"""
Debug script to test portfolio data fetching
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from portfolio_analyzer import PortfolioAnalyzer
from risk_metrics import RiskCalculator
import pandas as pd

def test_portfolio_data():
    """Test portfolio data fetching with a real wallet"""
    
    # Initialize with hardcoded API keys
    helius_api_key = "327e16d6-4cdc-46a5-8b1a-9ed373e848d4"
    coingecko_api_key = ""
    
    portfolio_analyzer = PortfolioAnalyzer(helius_api_key, coingecko_api_key)
    risk_calculator = RiskCalculator()
    
    # Test with a known wallet address
    wallet_address = "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM"
    
    print(f"🔍 Testing portfolio data for wallet: {wallet_address}")
    print("=" * 60)
    
    try:
        # Fetch portfolio data
        print("📡 Fetching portfolio data...")
        portfolio_data = portfolio_analyzer.get_portfolio_data(wallet_address, "30 days")
        
        if portfolio_data is None:
            print("❌ No portfolio data returned")
            return
        
        if portfolio_data.empty:
            print("❌ Portfolio data is empty")
            return
        
        print(f"✅ Portfolio data fetched successfully!")
        print(f"📊 Found {len(portfolio_data)} tokens")
        print("\n📋 Portfolio Summary:")
        print(f"Total Value: ${portfolio_data['value_usd'].sum():.2f}")
        print(f"Number of Tokens: {len(portfolio_data)}")
        
        # Show top 5 tokens by value
        top_tokens = portfolio_data.nlargest(5, 'value_usd')
        print("\n🏆 Top 5 Tokens by Value:")
        for _, token in top_tokens.iterrows():
            print(f"  {token['symbol']}: ${token['value_usd']:.2f} ({token['amount']:.2f} tokens)")
        
        # Test risk calculations
        print("\n📈 Testing risk calculations...")
        risk_metrics = risk_calculator.calculate_risk_metrics(portfolio_data)
        
        print(f"Portfolio Volatility: {risk_metrics.get('portfolio_volatility', 'N/A'):.2%}")
        print(f"Sharpe Ratio: {risk_metrics.get('sharpe_ratio', 'N/A'):.2f}")
        print(f"Max Drawdown: {risk_metrics.get('max_drawdown', 'N/A'):.2%}")
        
        # Check for NaN values
        print("\n🔍 Checking for data issues:")
        nan_count = portfolio_data['value_usd'].isna().sum()
        zero_count = (portfolio_data['value_usd'] == 0).sum()
        print(f"NaN values in value_usd: {nan_count}")
        print(f"Zero values in value_usd: {zero_count}")
        
        if nan_count > 0 or zero_count == len(portfolio_data):
            print("⚠️ Data quality issues detected!")
            print("\nSample data:")
            print(portfolio_data[['symbol', 'amount', 'price_usd', 'value_usd']].head())
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_portfolio_data()
