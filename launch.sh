#!/bin/bash

# Set API keys
export GEMINI_API_KEY="AIzaSyAlry5jmb1qqbFgvZztYImH6BC2-eFUpKU"
export HELIUS_API_KEY="327e16d6-4cdc-46a5-8b1a-9ed373e848d4"
export COINGECKO_API_KEY=""

echo "🚀 Starting Solana Risk Dashboard..."
echo "🔑 API Keys configured automatically"
echo "📱 Open http://localhost:8501 in your browser"
echo "=================================================="

# Change to the script directory
cd "$(dirname "$0")"

# Activate virtual environment and run streamlit
source venv/bin/activate
streamlit run app.py --server.headless true
