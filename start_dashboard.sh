#!/bin/bash

# Solana Risk Dashboard Launcher
echo "🎯 Solana Risk Dashboard"
echo "========================"

# Set API keys
export GEMINI_API_KEY="AIzaSyAlry5jmb1qqbFgvZztYImH6BC2-eFUpKU"
export HELIUS_API_KEY="327e16d6-4cdc-46a5-8b1a-9ed373e848d4"
export COINGECKO_API_KEY=""

echo "🔑 API Keys configured:"
echo "   ✅ Gemini API: ${GEMINI_API_KEY:0:20}..."
echo "   ✅ Helius API: ${HELIUS_API_KEY:0:20}..."
echo "   ⚪ CoinGecko API: Not needed"

echo ""
echo "🚀 Launching Dashboard..."
echo "📋 Ready to analyze Solana wallets!"

# Use virtual environment's streamlit
./venv/bin/streamlit run app.py
