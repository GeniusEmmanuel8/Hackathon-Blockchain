import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
from portfolio_analyzer import PortfolioAnalyzer
from risk_metrics import RiskCalculator
from ai_insights import AIInsightsGenerator
from correlation_analyzer import CorrelationAnalyzer

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Solana Risk Dashboard",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #9945FF, #14F195);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .risk-high { color: #ff4444; }
    .risk-medium { color: #ffaa00; }
    .risk-low { color: #44ff44; }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🔗 Solana Risk Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Analyze your Solana portfolio risk and get AI-powered insights")
    
    # Sidebar for wallet input
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Keys - Auto-configure from environment variables
        helius_api_key = os.getenv("HELIUS_API_KEY", "")
        coingecko_api_key = os.getenv("COINGECKO_API_KEY", "")
        gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        
        # Show API key status
        if helius_api_key:
            st.success("✅ Helius API Key: Configured")
        else:
            st.error("❌ Helius API Key: Not found")
            st.info("💡 Add HELIUS_API_KEY to your environment variables")
        
        if gemini_api_key:
            st.success("✅ Gemini API Key: Configured")
        else:
            st.warning("⚠️ Gemini API Key: Not found (AI insights disabled)")
        
        if coingecko_api_key:
            st.success("✅ CoinGecko API Key: Configured")
        else:
            st.info("ℹ️ CoinGecko API Key: Not needed (using Helius for prices)")
        
        # Optional: Allow manual override
        with st.expander("🔧 Manual API Key Override (Optional)"):
            helius_override = st.text_input(
                "Helius API Key Override", 
                type="password",
                help="Override the environment variable"
            )
            if helius_override:
                helius_api_key = helius_override
            
            gemini_override = st.text_input(
                "Gemini API Key Override", 
                type="password",
                help="Override the environment variable"
            )
            if gemini_override:
                gemini_api_key = gemini_override
        
        st.divider()
        
        # Wallet address input
        wallet_address = st.text_input(
            "Solana Wallet Address",
            placeholder="Enter wallet address (e.g., 9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM)",
            help="Enter a valid Solana wallet address to analyze"
        )
        
        # Analysis options
        st.subheader("📊 Analysis Options")
        include_ai_insights = st.checkbox("Include AI Insights", value=bool(gemini_api_key))
        risk_tolerance = st.selectbox(
            "Risk Tolerance",
            ["Conservative", "Moderate", "Aggressive"],
            index=1
        )
        
        # Time period for historical data
        time_period = st.selectbox(
            "Historical Data Period",
            ["7 days", "30 days", "90 days", "1 year"],
            index=1
        )
    
    # Main content area
    if not wallet_address:
        st.info("👆 Please enter a Solana wallet address in the sidebar to begin analysis")
        show_sample_data()
        return
    
    if not helius_api_key:
        st.error("❌ Helius API key is required to fetch wallet data")
        st.info("""
        **To fix this:**
        1. Set the environment variable: `export HELIUS_API_KEY="your_key_here"`
        2. Or use the manual override in the sidebar
        3. Get your free API key from: https://helius.xyz
        """)
        return
    
    # Initialize analyzers
    try:
        with st.spinner("🔄 Fetching wallet data and analyzing portfolio..."):
            portfolio_analyzer = PortfolioAnalyzer(helius_api_key, coingecko_api_key)
            risk_calculator = RiskCalculator()
            ai_generator = AIInsightsGenerator(gemini_api_key) if gemini_api_key else None
            correlation_analyzer = CorrelationAnalyzer(coingecko_api_key)
            
            # Fetch portfolio data
            portfolio_data = portfolio_analyzer.get_portfolio_data(wallet_address, time_period)
            
            if portfolio_data is None or portfolio_data.empty:
                st.error("❌ No data found for this wallet address or API error occurred")
                return
            
            # Calculate risk metrics
            risk_metrics = risk_calculator.calculate_risk_metrics(portfolio_data)
            
            # Display results
            display_portfolio_overview(portfolio_data, risk_metrics)
            display_portfolio_visualizations(portfolio_data, risk_metrics)
            display_risk_analysis(risk_metrics, risk_tolerance)
            display_correlation_analysis(portfolio_data, correlation_analyzer, time_period)
            
            if include_ai_insights and ai_generator:
                display_ai_insights(portfolio_data, risk_metrics, ai_generator)
            
            # Export options
            display_export_options(portfolio_data, risk_metrics)
            
    except Exception as e:
        st.error(f"❌ Error analyzing portfolio: {str(e)}")
        st.exception(e)

def show_sample_data():
    """Show sample data and features when no wallet is provided"""
    st.markdown("### 🚀 Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📊 Portfolio Analysis**
        - Real-time token balances
        - Portfolio concentration
        - Risk metrics calculation
        """)
    
    with col2:
        st.markdown("""
        **📈 Risk Metrics**
        - Volatility analysis
        - Sharpe ratio
        - Token correlations
        """)
    
    with col3:
        st.markdown("""
        **🤖 AI Insights**
        - Risk explanations
        - Diversification advice
        - What-if scenarios
        """)

def display_portfolio_overview(portfolio_data, risk_metrics):
    """Display portfolio overview metrics"""
    st.header("📊 Portfolio Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_value = portfolio_data['value_usd'].sum()
        st.metric("Total Portfolio Value", f"${total_value:,.2f}")
    
    with col2:
        num_tokens = len(portfolio_data)
        st.metric("Number of Tokens", num_tokens)
    
    with col3:
        volatility = risk_metrics.get('portfolio_volatility', 0)
        st.metric("Portfolio Volatility", f"{volatility:.2%}")
    
    with col4:
        sharpe_ratio = risk_metrics.get('sharpe_ratio', 0)
        st.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")

def display_portfolio_visualizations(portfolio_data, risk_metrics):
    """Display portfolio visualization charts"""
    st.header("📈 Portfolio Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Portfolio composition pie chart
        fig_pie = px.pie(
            portfolio_data, 
            values='value_usd', 
            names='symbol',
            title="Portfolio Composition",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Token value bar chart
        fig_bar = px.bar(
            portfolio_data.sort_values('value_usd', ascending=True),
            x='value_usd',
            y='symbol',
            orientation='h',
            title="Token Values (USD)",
            color='value_usd',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

def display_risk_analysis(risk_metrics, risk_tolerance):
    """Display risk analysis and metrics"""
    st.header("⚠️ Risk Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Risk Metrics")
        
        # Volatility
        volatility = risk_metrics.get('portfolio_volatility', 0)
        volatility_class = get_risk_class(volatility, 'volatility')
        st.markdown(f"""
        <div class="metric-card">
            <h4>Portfolio Volatility</h4>
            <h2 class="{volatility_class}">{volatility:.2%}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Sharpe Ratio
        sharpe_ratio = risk_metrics.get('sharpe_ratio', 0)
        sharpe_class = get_risk_class(sharpe_ratio, 'sharpe')
        st.markdown(f"""
        <div class="metric-card">
            <h4>Sharpe Ratio</h4>
            <h2 class="{sharpe_class}">{sharpe_ratio:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Risk Assessment")
        
        # Risk level based on tolerance
        risk_level = assess_risk_level(risk_metrics, risk_tolerance)
        risk_color = {"Low": "risk-low", "Medium": "risk-medium", "High": "risk-high"}[risk_level]
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>Overall Risk Level</h4>
            <h2 class="{risk_color}">{risk_level}</h2>
            <p>Based on {risk_tolerance} tolerance</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Recommendations
        recommendations = get_risk_recommendations(risk_metrics, risk_tolerance)
        st.subheader("💡 Recommendations")
        for rec in recommendations:
            st.write(f"• {rec}")

def display_ai_insights(portfolio_data, risk_metrics, ai_generator):
    """Display AI-generated insights"""
    st.header("🤖 AI Insights")
    
    with st.spinner("Generating AI insights..."):
        insights = ai_generator.generate_insights(portfolio_data, risk_metrics)
        
        st.markdown("### Portfolio Analysis")
        st.write(insights.get('analysis', 'No insights available'))
        
        st.markdown("### Risk Assessment")
        st.write(insights.get('risk_assessment', 'No risk assessment available'))
        
        st.markdown("### Recommendations")
        st.write(insights.get('recommendations', 'No recommendations available'))

def display_correlation_analysis(portfolio_data, correlation_analyzer, time_period):
    """Display correlation analysis and heatmap"""
    st.header("🔗 Token Correlation Analysis")
    
    if portfolio_data.empty or len(portfolio_data) < 2:
        st.info("⚠️ Need at least 2 tokens for correlation analysis")
        return
    
    # Get token symbols
    symbols = portfolio_data['symbol'].tolist()
    
    with st.spinner("🔄 Analyzing token correlations..."):
        # Get historical data
        historical_data = correlation_analyzer.get_historical_prices(symbols, 30)
        
        if historical_data.empty:
            st.warning("⚠️ Unable to fetch historical data for correlation analysis")
            return
        
        # Calculate correlations
        correlation_matrix = correlation_analyzer.calculate_correlations(historical_data)
        
        if correlation_matrix.empty:
            st.warning("⚠️ Unable to calculate correlations")
            return
        
        # Display correlation insights
        insights = correlation_analyzer.analyze_correlation_insights(correlation_matrix)
        
        # Show summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Average Correlation", f"{insights['avg_correlation']:.3f}")
        
        with col2:
            st.metric("Diversification Score", f"{insights['diversification_score']:.3f}")
        
        with col3:
            st.metric("High Correlations", len(insights['high_correlations']))
        
        with col4:
            risk_level = "Low" if insights['diversification_score'] > 0.7 else "Medium" if insights['diversification_score'] > 0.4 else "High"
            st.metric("Correlation Risk", risk_level)
        
        # Display correlation heatmap
        st.subheader("📊 Correlation Heatmap")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_heatmap = correlation_analyzer.create_correlation_heatmap(correlation_matrix)
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        with col2:
            fig_network = correlation_analyzer.create_correlation_network(correlation_matrix, threshold=0.5)
            st.plotly_chart(fig_network, use_container_width=True)
        
        # Display correlation summary
        st.subheader("📈 Correlation Summary")
        
        fig_summary = correlation_analyzer.create_correlation_summary_chart(insights)
        st.plotly_chart(fig_summary, use_container_width=True)
        
        # Display insights
        if insights['risk_insights']:
            st.subheader("💡 Correlation Insights")
            for insight in insights['risk_insights']:
                st.write(f"• {insight}")
        
        # Display high correlations
        if insights['high_correlations']:
            st.subheader("🔴 High Correlations")
            for corr in insights['high_correlations'][:5]:  # Show top 5
                st.write(f"**{corr['pair']}**: {corr['correlation']:.3f}")
        
        # Display low correlations
        if insights['low_correlations']:
            st.subheader("🟢 Low/Negative Correlations")
            for corr in insights['low_correlations'][:5]:  # Show top 5
                st.write(f"**{corr['pair']}**: {corr['correlation']:.3f}")

def display_export_options(portfolio_data, risk_metrics):
    """Display export options"""
    st.header("📄 Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export to CSV"):
            csv = portfolio_data.to_csv(index=False)
            st.download_button(
                label="Download Portfolio Data",
                data=csv,
                file_name=f"portfolio_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📋 Generate PDF Report"):
            # This would generate a comprehensive PDF report
            st.info("PDF report generation coming soon!")

def get_risk_class(value, metric_type):
    """Get CSS class for risk level"""
    if metric_type == 'volatility':
        if value < 0.1: return 'risk-low'
        elif value < 0.3: return 'risk-medium'
        else: return 'risk-high'
    elif metric_type == 'sharpe':
        if value > 1.0: return 'risk-low'
        elif value > 0.5: return 'risk-medium'
        else: return 'risk-high'
    return 'risk-medium'

def assess_risk_level(risk_metrics, risk_tolerance):
    """Assess overall risk level based on metrics and tolerance"""
    volatility = risk_metrics.get('portfolio_volatility', 0)
    sharpe_ratio = risk_metrics.get('sharpe_ratio', 0)
    
    # Simple risk assessment logic
    if volatility < 0.15 and sharpe_ratio > 0.8:
        return "Low"
    elif volatility < 0.3 and sharpe_ratio > 0.3:
        return "Medium"
    else:
        return "High"

def get_risk_recommendations(risk_metrics, risk_tolerance):
    """Get risk-based recommendations"""
    recommendations = []
    
    volatility = risk_metrics.get('portfolio_volatility', 0)
    sharpe_ratio = risk_metrics.get('sharpe_ratio', 0)
    
    if volatility > 0.3:
        recommendations.append("Consider diversifying your portfolio to reduce volatility")
    
    if sharpe_ratio < 0.5:
        recommendations.append("Your risk-adjusted returns could be improved")
    
    if len(risk_metrics.get('token_weights', {})) < 5:
        recommendations.append("Consider adding more tokens for better diversification")
    
    return recommendations

if __name__ == "__main__":
    main()
