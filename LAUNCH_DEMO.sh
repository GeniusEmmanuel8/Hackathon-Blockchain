#!/bin/bash

# 🚀 Solana Risk Dashboard - Demo Launch Script
# Run this script to start your hackathon demo

echo "🎯 Starting Solana Risk Dashboard Demo..."
echo "========================================"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the solana-risk-dashboard directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Test components
echo "🧪 Testing all components..."
python test_components.py

if [ $? -eq 0 ]; then
    echo "✅ All components working!"
else
    echo "❌ Component test failed. Please check the errors above."
    exit 1
fi

# Start the dashboard
echo "🚀 Launching Solana Risk Dashboard..."
echo "📱 Dashboard will be available at: http://localhost:8501"
echo "🔄 Press Ctrl+C to stop the dashboard"
echo "========================================"

streamlit run app.py --server.headless true --server.port 8501
