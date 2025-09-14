# 🔗 Solana Risk Dashboard

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive risk analysis dashboard for Solana wallets that provides portfolio insights, risk metrics, and AI-powered recommendations. Built for hackathons and blockchain enthusiasts.

## 🌟 Features

### ✅ **Core Features**
- **Real-time Portfolio Analysis**: Fetch live token balances and prices
- **Risk Metrics**: Calculate volatility, Sharpe ratio, VaR, and CVaR
- **Portfolio Visualization**: Interactive charts and graphs
- **Correlation Analysis**: Token correlation heatmaps
- **Concentration Risk**: Herfindahl-Hirschman Index analysis

### ✅ **Advanced Features**
- **AI-Powered Insights**: Google Gemini integration for intelligent analysis
- **What-if Scenarios**: Backtest different allocation strategies
- **Export Options**: CSV and PDF report generation
- **Risk Tolerance Assessment**: Personalized risk recommendations

## 🚀 Quick Start

### **🎯 For Hackathon Demo (Recommended)**
```bash
# Clone the repository
git clone https://github.com/GeniusEmmanuel8/Hackathon-Blockchain.git
cd solana-risk-dashboard

# Launch demo (one command)
./LAUNCH_DEMO.sh
```
This script will:
- ✅ Activate the virtual environment
- ✅ Test all components
- ✅ Launch the dashboard at http://localhost:8501

### **Option 1: Manual Setup**
```bash
# Clone the repository
git clone https://github.com/GeniusEmmanuel8/Hackathon-Blockchain.git
cd solana-risk-dashboard

# Install dependencies
python3 -m pip install -r requirements.txt

# Run the app
source venv/bin/activate && streamlit run app.py --server.headless true --server.port 8501
```

### **🎯 Demo Features Ready**
- ✅ Real-time Solana wallet analysis via Helius API
- ✅ Advanced risk metrics (volatility, Sharpe ratio, concentration)
- ✅ AI-powered insights using Google Gemini
- ✅ Robust error handling and retry logic
- ✅ Professional UI with refresh functionality
- ✅ Realistic portfolio values ($2.5B demo portfolio)

## 🔧 Configuration

### **Required API Keys**

1. **Helius API Key** (Required)
   - Get free API key from: https://helius.xyz
   - Used for fetching Solana wallet data and token prices

2. **Google Gemini API Key** (Optional)
   - Get free API key from: https://aistudio.google.com/app/apikey
   - Used for AI-powered portfolio insights

3. **CoinGecko API Key** (Optional)
   - Get from: https://www.coingecko.com/en/api
   - Used for higher rate limits (not required - Helius provides prices)

### **Environment Variables**
Create a `.env` file in the project root:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
HELIUS_API_KEY=your_helius_api_key_here
COINGECKO_API_KEY=your_coingecko_api_key_here  # Optional
```

## 🚀 Features

### Core Features
- **Real-time Portfolio Analysis**: Fetch live token balances and prices
- **Risk Metrics**: Calculate volatility, Sharpe ratio, VaR, and CVaR
- **Portfolio Visualization**: Interactive charts and graphs
- **Correlation Analysis**: Token correlation heatmaps
- **Concentration Risk**: Herfindahl-Hirschman Index analysis

### Advanced Features
- **AI-Powered Insights**: OpenAI integration for intelligent analysis
- **What-if Scenarios**: Backtest different allocation strategies
- **Export Options**: CSV and PDF report generation
- **Risk Tolerance Assessment**: Personalized risk recommendations

## 🛠️ Tech Stack

- **Backend**: Python 3.8+
- **Web Framework**: Streamlit
- **Data Analysis**: Pandas, NumPy, SciPy
- **Visualization**: Plotly, Seaborn, Matplotlib
- **Portfolio Optimization**: PyPortfolioOpt
- **APIs**: Helius (Solana), CoinGecko (Prices)
- **AI**: Google Gemini Pro
- **Export**: ReportLab (PDF generation)

## 📋 Prerequisites

- Python 3.8 or higher
- Helius API key (free at [helius.xyz](https://helius.xyz))
- CoinGecko API key (optional, for higher rate limits)
- Google Gemini API key (optional, for AI insights)

## 🚀 Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd solana-risk-dashboard
   pip install -r requirements.txt
   ```

2. **Configure API Keys**
   ```bash
   cp env_example.txt .env
   # Edit .env with your API keys
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

4. **Open in Browser**
   - Navigate to `http://localhost:8501`
   - Enter your Solana wallet address
   - View your portfolio analysis!

## 📊 Usage

### Basic Analysis
1. Enter your Solana wallet address in the sidebar
2. Provide your Helius API key
3. Select analysis options (risk tolerance, time period)
4. View comprehensive portfolio analysis

### AI Insights (Optional)
1. Add your OpenAI API key
2. Enable "Include AI Insights" checkbox
3. Get intelligent analysis and recommendations

### Export Data
1. Use the export options at the bottom
2. Download CSV data or generate PDF reports

## 🔧 Configuration

### Environment Variables
```bash
HELIUS_API_KEY=your_helius_api_key_here
COINGECKO_API_KEY=your_coingecko_api_key_here  # Optional
GEMINI_API_KEY=your_gemini_api_key_here        # Optional
```

### Risk Tolerance Levels
- **Conservative**: Lower volatility, stable returns
- **Moderate**: Balanced risk-return profile
- **Aggressive**: Higher risk, potential for higher returns

## 📈 Risk Metrics Explained

### Volatility
- Measures price fluctuation over time
- Higher volatility = higher risk
- Calculated using portfolio-weighted standard deviation

### Sharpe Ratio
- Risk-adjusted return metric
- Higher ratio = better risk-adjusted performance
- Formula: (Portfolio Return - Risk-Free Rate) / Volatility

### Value at Risk (VaR)
- Maximum expected loss over a given time period
- 95% VaR = 5% chance of losing more than this amount

### Concentration Risk
- Measures portfolio diversification
- Uses Herfindahl-Hirschman Index
- Lower values = better diversification

## 🤖 AI Features

### Portfolio Analysis
- Intelligent assessment of portfolio composition
- Risk profile identification
- Performance evaluation

### Recommendations
- Personalized diversification advice
- Risk management suggestions
- Allocation optimization tips

### What-if Scenarios
- Market crash impact analysis
- Bull market performance projections
- Rebalancing strategies

## 📁 Project Structure

```
solana-risk-dashboard/
├── app.py                 # Main Streamlit application
├── portfolio_analyzer.py  # Portfolio data fetching and analysis
├── risk_metrics.py       # Risk calculation functions
├── ai_insights.py        # AI-powered insights generation
├── requirements.txt      # Python dependencies
├── env_example.txt       # Environment variables template
└── README.md            # This file
```

## 🔍 API Integration

### Helius API
- Fetches Solana wallet token balances
- Provides real-time price data
- Handles token metadata

### CoinGecko API
- Backup price data source
- Historical price information
- Token market data

### Google Gemini API
- Gemini Pro for insights
- Natural language analysis
- Intelligent recommendations

## 🚨 Limitations

- Historical data simulation (real implementation would use actual historical data)
- Correlation analysis uses mock data
- Some risk metrics are estimated based on token characteristics
- AI insights require Google Gemini API key

## 🔮 Future Enhancements

- Real historical data integration
- Advanced backtesting capabilities
- More sophisticated risk models
- Multi-wallet portfolio analysis
- Real-time alerts and notifications
- Mobile-responsive design

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed description

## 🎯 Hackathon Notes

This project was built for a blockchain hackathon focusing on:
- Solana ecosystem integration
- Real-time data analysis
- Risk management tools
- AI-powered insights
- User-friendly interface

Perfect for demonstrating blockchain data analysis capabilities!
