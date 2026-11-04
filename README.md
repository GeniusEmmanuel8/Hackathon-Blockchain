# Solana Risk Dashboard
A Streamlit-powered dashboard for Solana wallets that provides portfolio insights, risk metrics, and AI-powered recommendations. Built in 48 hours for hackathon demo purposes.
Features
 Core
Real-time portfolio analysis (balances + token prices via Helius API)
Risk metrics: Volatility, Sharpe ratio, Value-at-Risk (VaR), Concentration risk
Portfolio visualization: interactive charts + token correlation heatmaps
Diversification check: Herfindahl-Hirschman Index
## Advanced
AI-powered insights with Google Gemini
“What-if” scenarios: backtest allocation strategies
Export results: CSV & PDF reports
Personalized risk tolerance assessment
## Tech Stack
Backend: Python (Pandas, NumPy, SciPy, PyPortfolioOpt)
Frontend: Streamlit + Plotly
Blockchain API: Helius (Solana) 
AI: Google Gemini Pro for portfolio insights
Export: ReportLab for PDF
## Setup
Requirements
Python 3.8+
API Keys:
HELIUS_API_KEY → Solana wallet + price data
GEMINI_API_KEY (optional) → AI insights

Quick Start
## Clone repo
git clone https://github.com/GeniusEmmanuel8/Hackathon-Blockchain.git
cd Hackathon-Blockchain

## Install dependencies
pip install -r requirements.txt

## Run app
streamlit run app.py
Config (.env file)
Copy `env_example.txt` to `.env` and fill in your own keys (the app reads them from the environment):
HELIUS_API_KEY=your_helius_api_key
GEMINI_API_KEY=your_gemini_api_key   # optional

## Security
- API keys must only live in your local `.env` file (it is git-ignored) or in environment variables. Never put them in source files.
- Earlier versions of this repository contained hard-coded keys. Those keys must be treated as compromised and are not valid for use; if you forked the repo before this change, do not reuse them.

## Usage
Enter your Solana wallet address in the sidebar.
View portfolio breakdown, risk metrics, and AI insights.
(Optional) Export results to CSV/PDF.

## Notes
due to helius api rate limits it can only be run once every minute or so.
AI was used to build this project.


## License
MIT License – see LICENSE file.
