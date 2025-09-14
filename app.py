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
    # Bigger, more prominent title
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 4rem; font-weight: bold; background: linear-gradient(90deg, #8B5CF6, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;">
            🔗 Solana Risk Dashboard
        </h1>
        <h2 style="font-size: 1.5rem; color: #94A3B8; font-weight: 300; margin-top: 0;">
            Analyze your Solana portfolio risk and get AI-powered insights
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # API Keys - Hardcoded for hackathon demo
    helius_api_key = "327e16d6-4cdc-46a5-8b1a-9ed373e848d4"
    coingecko_api_key = ""
    gemini_api_key = "AIzaSyAlry5jmb1qqbFgvZztYImH6BC2-eFUpKU"
    
    # Main page layout
    st.header("🔍 Portfolio Analysis")
    
    # Wallet address input
    wallet_address = st.text_input(
        "Solana Wallet Address",
        value="9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
        placeholder="Enter wallet address (e.g., 9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM)",
        help="Enter a valid Solana wallet address to analyze"
    )
    
    # Analysis options in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        include_ai_insights = st.checkbox(
            "🤖 AI Insights", 
            value=bool(gemini_api_key),
            help="Generate AI-powered insights and recommendations"
        )
    
    with col2:
        risk_tolerance = st.selectbox(
            "⚖️ Risk Tolerance",
            ["Conservative", "Moderate", "Aggressive"],
            index=1
        )
    
    with col3:
        time_period = st.selectbox(
            "📅 Historical Period",
            ["7 days", "30 days", "90 days", "1 year"],
            index=1
        )
    
    with col4:
        if st.button("🔄 Refresh Data", help="Click to refresh portfolio data"):
            st.cache_data.clear()
            st.rerun()
    
    # Main content area
    if not wallet_address:
        st.info("👆 Please enter a Solana wallet address above to begin analysis")
        show_sample_data()
        return
    
    # API keys are now hardcoded, so no need to check
    
    # Initialize analyzers
    try:
        with st.spinner("🔄 Fetching wallet data and analyzing portfolio..."):
            portfolio_analyzer = PortfolioAnalyzer(helius_api_key, coingecko_api_key)
            risk_calculator = RiskCalculator()
            ai_generator = AIInsightsGenerator(gemini_api_key) if gemini_api_key else None
            
            # Fetch portfolio data with better error handling
            portfolio_data = portfolio_analyzer.get_portfolio_data(wallet_address, time_period)
            
            if portfolio_data is None:
                st.error("❌ Failed to fetch portfolio data. Please check your wallet address and try again.")
                st.info("💡 Try clicking the 'Refresh Data' button above")
                return
            
            if portfolio_data.empty:
                st.error("❌ No tokens found in this wallet address")
                st.info("💡 Try a different wallet address or click 'Refresh Data'")
                return
            
            # Calculate risk metrics
            risk_metrics = risk_calculator.calculate_risk_metrics(portfolio_data)
            
            # Show debug info
            with st.expander("🔍 Debug Info", expanded=False):
                st.write(f"**Wallet Address**: {wallet_address}")
                st.write(f"**Portfolio Data Shape**: {portfolio_data.shape}")
                st.write(f"**Total Value**: ${portfolio_data['value_usd'].sum():,.2f}")
                st.write(f"**Token Count**: {len(portfolio_data)}")
            
            # Display results
            display_portfolio_overview(portfolio_data, risk_metrics)
            display_portfolio_explanation(portfolio_data, risk_metrics)
            display_risk_analysis(risk_metrics, risk_tolerance)
            
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

def display_portfolio_explanation(portfolio_data, risk_metrics):
    """Display explanation of what the user is seeing"""
    st.header("📚 Understanding Your Portfolio")
    
    # Create expandable sections for different concepts
    with st.expander("🔍 What is Portfolio Volatility?", expanded=True):
        volatility = risk_metrics.get('portfolio_volatility', 0)
        st.write(f"""
        **Volatility ({volatility:.1%})** measures how much your portfolio's value fluctuates over time.
        
        • **Low volatility (< 20%)**: Your portfolio value stays relatively stable
        • **Medium volatility (20-50%)**: Moderate price swings, typical for crypto portfolios  
        • **High volatility (> 50%)**: Large price swings, higher risk but potentially higher returns
        
        Your portfolio shows {'low' if volatility < 0.2 else 'medium' if volatility < 0.5 else 'high'} volatility.
        """)
    
    with st.expander("📊 What is the Sharpe Ratio?"):
        sharpe = risk_metrics.get('sharpe_ratio', 0)
        st.write(f"""
        **Sharpe Ratio ({sharpe:.2f})** measures risk-adjusted returns - how much return you get per unit of risk.
        
        • **Good (> 1.0)**: Strong risk-adjusted performance
        • **Average (0.5-1.0)**: Decent risk-adjusted performance
        • **Poor (< 0.5)**: High risk for relatively low returns
        
        Your portfolio shows {'excellent' if sharpe > 1.0 else 'good' if sharpe > 0.5 else 'needs improvement'} risk-adjusted performance.
        """)
    
    with st.expander("🎯 What is Concentration Risk?"):
        concentration = risk_metrics.get('concentration_risk', 0)
        # Ensure concentration is a number
        if isinstance(concentration, str):
            try:
                concentration = float(concentration)
            except (ValueError, TypeError):
                concentration = 0.0
        
        st.write(f"""
        **Concentration Risk ({concentration:.1%})** measures how much of your portfolio is in your largest position.
        
        • **Low (< 20%)**: Well diversified across many tokens
        • **Medium (20-40%)**: Some concentration, consider diversifying
        • **High (> 40%)**: Highly concentrated, significant risk
        
        Your largest position represents {concentration:.1%} of your portfolio, indicating {'good' if concentration < 0.2 else 'moderate' if concentration < 0.4 else 'high'} concentration risk.
        """)

def display_ai_insights(portfolio_data, risk_metrics, ai_generator):
    """Display AI-generated insights"""
    st.header("🤖 AI-Powered Portfolio Analysis")
    
    with st.spinner("🔄 Generating comprehensive AI analysis..."):
        insights = ai_generator.generate_insights(portfolio_data, risk_metrics)
        
        # Detailed Gemini Summary Section
        st.subheader("📊 AI Portfolio Summary")
        
        # Get portfolio metrics for context with proper type handling
        total_value = portfolio_data['value_usd'].sum()
        num_tokens = len(portfolio_data)
        volatility = risk_metrics.get('portfolio_volatility', 0)
        sharpe = risk_metrics.get('sharpe_ratio', 0)
        concentration = risk_metrics.get('concentration_risk', 0)
        
        # Ensure all values are numeric
        if isinstance(volatility, str):
            try:
                volatility = float(volatility)
            except (ValueError, TypeError):
                volatility = 0.0
        
        if isinstance(sharpe, str):
            try:
                sharpe = float(sharpe)
            except (ValueError, TypeError):
                sharpe = 0.0
                
        if isinstance(concentration, str):
            try:
                concentration = float(concentration)
            except (ValueError, TypeError):
                concentration = 0.0
        
        # Create a comprehensive summary card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; margin: 20px 0;">
            <h3 style="margin-top: 0; color: white;">🎯 Portfolio Overview</h3>
            <p><strong>Total Value:</strong> ${total_value:,.2f} | <strong>Tokens:</strong> {num_tokens:,} | <strong>Volatility:</strong> {volatility:.1%}</p>
            <p><strong>Risk-Adjusted Return (Sharpe):</strong> {sharpe:.2f} | <strong>Concentration:</strong> {concentration:.1%}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # AI Analysis in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🧠 AI Analysis")
            st.write(insights.get('analysis', 'No analysis available'))
            
        with col2:
            st.subheader("⚠️ Risk Assessment")
            st.write(insights.get('risk_assessment', 'No risk assessment available'))
        
        # Recommendations section
        st.subheader("💡 AI Recommendations")
        recommendations = insights.get('recommendations', 'No recommendations available')
        st.write(recommendations)
        
        # How metrics affect risk scores
        st.subheader("📈 How Your Metrics Affect Risk Scores")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Volatility Impact", 
                     f"{volatility:.1%}",
                     help="Higher volatility = Higher risk score")
            if volatility > 0.5:
                st.warning("High volatility increases your risk score significantly")
            elif volatility > 0.2:
                st.info("Moderate volatility contributes to medium risk")
            else:
                st.success("Low volatility keeps risk score low")
        
        with col2:
            st.metric("Sharpe Ratio Impact",
                     f"{sharpe:.2f}",
                     help="Higher Sharpe = Better risk-adjusted returns")
            if sharpe > 1.0:
                st.success("Excellent risk-adjusted performance")
            elif sharpe > 0.5:
                st.info("Good risk-adjusted performance")
            else:
                st.warning("Poor risk-adjusted performance - high risk for low returns")
        
        with col3:
            st.metric("Concentration Impact",
                     f"{concentration:.1%}",
                     help="Higher concentration = Higher diversification risk")
            if concentration > 0.4:
                st.error("High concentration - major risk factor")
            elif concentration > 0.2:
                st.warning("Moderate concentration - consider diversifying")
            else:
                st.success("Well diversified - low concentration risk")
        
        # Actionable insights
        st.subheader("🎯 Recommended Actions")
        st.write("Based on your AI analysis:")
        st.write("• **Portfolio Size**: With " + str(num_tokens) + " tokens, you have " + ("excellent" if num_tokens > 100 else "good" if num_tokens > 50 else "limited") + " diversification")
        st.write("• **Risk Management**: " + ("Consider reducing position sizes" if concentration > 0.3 else "Your diversification is well-balanced"))
        st.write("• **Performance**: " + ("Focus on risk management" if sharpe < 0.5 else "Your risk-adjusted returns are solid"))

# Correlation analysis removed as requested

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
