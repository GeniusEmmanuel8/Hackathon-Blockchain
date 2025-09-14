#!/usr/bin/env python3
"""
Debug script to check what Helius API is actually returning
"""

import requests
import json

def debug_helius_response():
    """Check what Helius API returns for a wallet"""
    
    api_key = "327e16d6-4cdc-46a5-8b1a-9ed373e848d4"
    wallet_address = "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM"
    
    url = f"https://api.helius.xyz/v0/addresses/{wallet_address}/balances"
    params = {
        "api-key": api_key
    }
    
    print(f"🔍 Fetching data from Helius API...")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Response received")
        print(f"📊 Total tokens: {len(data.get('tokens', []))}")
        
        # Show first 5 tokens with all their data
        tokens = data.get('tokens', [])[:5]
        print(f"\n🔍 First 5 tokens:")
        for i, token in enumerate(tokens):
            print(f"\nToken {i+1}:")
            for key, value in token.items():
                print(f"  {key}: {value}")
        
        # Check if any tokens have price/value data
        print(f"\n💰 Price/Value Analysis:")
        tokens_with_price = [t for t in data.get('tokens', []) if t.get('price') and t.get('price') > 0]
        tokens_with_value = [t for t in data.get('tokens', []) if t.get('value') and t.get('value') > 0]
        
        print(f"Tokens with price > 0: {len(tokens_with_price)}")
        print(f"Tokens with value > 0: {len(tokens_with_value)}")
        
        if tokens_with_price:
            print(f"\n🏆 Tokens with prices:")
            for token in tokens_with_price[:3]:
                print(f"  {token.get('symbol', 'Unknown')}: ${token.get('price', 0):.6f}")
        
        if tokens_with_value:
            print(f"\n💎 Tokens with values:")
            for token in tokens_with_value[:3]:
                print(f"  {token.get('symbol', 'Unknown')}: ${token.get('value', 0):.2f}")
        
        # Check for known token symbols
        symbols = [t.get('symbol', 'Unknown') for t in data.get('tokens', [])]
        unique_symbols = set(symbols)
        print(f"\n📝 Unique symbols found: {len(unique_symbols)}")
        print(f"Symbols: {list(unique_symbols)[:10]}...")  # Show first 10
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_helius_response()
