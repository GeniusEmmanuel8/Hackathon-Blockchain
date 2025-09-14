import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class CorrelationAnalyzer:
    def __init__(self, coingecko_api_key=None):
        self.coingecko_api_key = coingecko_api_key
        self.coingecko_base_url = "https://api.coingecko.com/api/v3"
        
    def get_historical_prices(self, symbols: List[str], days: int = 30) -> pd.DataFrame:
        """Get historical price data for correlation analysis"""
        if not symbols:
            return pd.DataFrame()
        
        # Map Solana tokens to CoinGecko IDs
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
            # If no CoinGecko mappings, generate mock data
            return self._generate_mock_historical_data(symbols, days)
        
        # Get historical data from CoinGecko
        url = f"{self.coingecko_base_url}/coins/market_chart"
        params = {
            'ids': ','.join(coingecko_ids),
            'vs_currency': 'usd',
            'days': days,
            'interval': 'daily'
        }
        
        if self.coingecko_api_key:
            params['x_cg_demo_api_key'] = self.coingecko_api_key
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Process the data
            price_data = {}
            for coin_id, coin_data in data.items():
                symbol = [k for k, v in token_mapping.items() if v == coin_id][0]
                prices = [point[1] for point in coin_data['prices']]
                price_data[symbol] = prices
            
            # Create DataFrame
            df = pd.DataFrame(price_data)
            df.index = pd.date_range(end=datetime.now(), periods=len(df), freq='D')
            
            return df
            
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            # Fallback to mock data
            return self._generate_mock_historical_data(symbols, days)
    
    def _generate_mock_historical_data(self, symbols: List[str], days: int) -> pd.DataFrame:
        """Generate mock historical data for correlation analysis"""
        np.random.seed(42)  # For reproducible results
        
        # Create date range
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        # Generate mock price data with realistic correlations
        price_data = {}
        
        for i, symbol in enumerate(symbols):
            # Base price
            base_price = 100 * (i + 1)
            
            # Generate correlated random walk
            if symbol == 'SOL':
                # SOL as the main token
                returns = np.random.normal(0.001, 0.05, days)  # 0.1% daily return, 5% volatility
            elif symbol in ['USDC', 'USDT']:
                # Stablecoins - very low volatility
                returns = np.random.normal(0.0001, 0.001, days)
            else:
                # Other tokens - correlated with SOL but more volatile
                sol_correlation = 0.6 + np.random.uniform(-0.2, 0.2)
                returns = sol_correlation * np.random.normal(0.001, 0.05, days) + \
                         (1 - sol_correlation) * np.random.normal(0.001, 0.08, days)
            
            # Calculate prices
            prices = [base_price]
            for ret in returns[1:]:
                prices.append(prices[-1] * (1 + ret))
            
            price_data[symbol] = prices
        
        df = pd.DataFrame(price_data, index=dates)
        return df
    
    def calculate_correlations(self, price_data: pd.DataFrame) -> pd.DataFrame:
        """Calculate correlation matrix from price data"""
        if price_data.empty:
            return pd.DataFrame()
        
        # Calculate daily returns
        returns = price_data.pct_change().dropna()
        
        # Calculate correlation matrix
        correlation_matrix = returns.corr()
        
        return correlation_matrix
    
    def create_correlation_heatmap(self, correlation_matrix: pd.DataFrame, title: str = "Token Correlation Matrix") -> go.Figure:
        """Create an interactive correlation heatmap"""
        if correlation_matrix.empty:
            # Return empty figure
            fig = go.Figure()
            fig.add_annotation(
                text="No correlation data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            colorscale='RdBu',
            zmid=0,
            text=np.round(correlation_matrix.values, 3),
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False,
            colorbar=dict(
                title="Correlation",
                tickmode="array",
                tickvals=[-1, -0.5, 0, 0.5, 1],
                ticktext=["-1", "-0.5", "0", "0.5", "1"]
            )
        ))
        
        fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                font=dict(size=16)
            ),
            xaxis=dict(title="Tokens"),
            yaxis=dict(title="Tokens"),
            width=600,
            height=500,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig
    
    def create_correlation_network(self, correlation_matrix: pd.DataFrame, threshold: float = 0.3) -> go.Figure:
        """Create a network graph showing strong correlations"""
        if correlation_matrix.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="No correlation data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Find strong correlations
        strong_correlations = []
        tokens = correlation_matrix.columns.tolist()
        
        for i in range(len(tokens)):
            for j in range(i + 1, len(tokens)):
                corr = correlation_matrix.iloc[i, j]
                if abs(corr) >= threshold:
                    strong_correlations.append({
                        'token1': tokens[i],
                        'token2': tokens[j],
                        'correlation': corr
                    })
        
        if not strong_correlations:
            fig = go.Figure()
            fig.add_annotation(
                text=f"No strong correlations found (threshold: {threshold})",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            return fig
        
        # Create network layout
        all_tokens = list(set([c['token1'] for c in strong_correlations] + 
                             [c['token2'] for c in strong_correlations]))
        
        # Simple circular layout
        n_tokens = len(all_tokens)
        angles = np.linspace(0, 2 * np.pi, n_tokens, endpoint=False)
        
        pos = {}
        for i, token in enumerate(all_tokens):
            pos[token] = (np.cos(angles[i]), np.sin(angles[i]))
        
        # Create edges
        edge_x = []
        edge_y = []
        edge_info = []
        
        for corr in strong_correlations:
            x0, y0 = pos[corr['token1']]
            x1, y1 = pos[corr['token2']]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_info.append(f"{corr['token1']} ↔ {corr['token2']}<br>Correlation: {corr['correlation']:.3f}")
        
        # Create nodes
        node_x = [pos[token][0] for token in all_tokens]
        node_y = [pos[token][1] for token in all_tokens]
        node_text = all_tokens
        
        # Create the figure
        fig = go.Figure()
        
        # Add edges
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='lightgray'),
            hoverinfo='none',
            mode='lines',
            name='Correlations'
        ))
        
        # Add nodes
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            marker=dict(size=20, color='lightblue', line=dict(width=2, color='darkblue')),
            text=node_text,
            textposition="middle center",
            textfont=dict(size=10, color='white'),
            name='Tokens',
            hovertemplate='%{text}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(
                text=f"Token Correlation Network (threshold: {threshold})",
                x=0.5,
                font=dict(size=16)
            ),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                text="Strong correlations are shown as lines between tokens",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002,
                xanchor="left", yanchor="bottom",
                font=dict(size=12, color="gray")
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            width=600,
            height=500
        )
        
        return fig
    
    def analyze_correlation_insights(self, correlation_matrix: pd.DataFrame) -> Dict[str, any]:
        """Analyze correlation matrix and provide insights"""
        if correlation_matrix.empty:
            return {
                'avg_correlation': 0,
                'max_correlation': 0,
                'min_correlation': 0,
                'high_correlations': [],
                'low_correlations': [],
                'diversification_score': 0,
                'risk_insights': []
            }
        
        # Calculate basic statistics
        correlations = correlation_matrix.values
        # Remove diagonal (self-correlations)
        mask = ~np.eye(correlations.shape[0], dtype=bool)
        off_diagonal = correlations[mask]
        
        avg_correlation = np.mean(off_diagonal)
        max_correlation = np.max(off_diagonal)
        min_correlation = np.min(off_diagonal)
        
        # Find high and low correlations
        high_correlations = []
        low_correlations = []
        
        tokens = correlation_matrix.columns.tolist()
        for i in range(len(tokens)):
            for j in range(i + 1, len(tokens)):
                corr = correlation_matrix.iloc[i, j]
                pair = f"{tokens[i]} ↔ {tokens[j]}"
                
                if corr > 0.7:
                    high_correlations.append({'pair': pair, 'correlation': corr})
                elif corr < -0.3:
                    low_correlations.append({'pair': pair, 'correlation': corr})
        
        # Calculate diversification score (lower average correlation = better diversification)
        diversification_score = max(0, 1 - abs(avg_correlation))
        
        # Generate risk insights
        risk_insights = []
        
        if avg_correlation > 0.6:
            risk_insights.append("High average correlation suggests portfolio may not be well diversified")
        elif avg_correlation < 0.2:
            risk_insights.append("Low average correlation indicates good diversification")
        
        if max_correlation > 0.8:
            risk_insights.append("Some tokens are highly correlated, increasing concentration risk")
        
        if len(high_correlations) > len(tokens) / 2:
            risk_insights.append("Many token pairs are highly correlated, reducing diversification benefits")
        
        if diversification_score < 0.3:
            risk_insights.append("Portfolio has low diversification score - consider adding uncorrelated assets")
        
        return {
            'avg_correlation': avg_correlation,
            'max_correlation': max_correlation,
            'min_correlation': min_correlation,
            'high_correlations': high_correlations,
            'low_correlations': low_correlations,
            'diversification_score': diversification_score,
            'risk_insights': risk_insights
        }
    
    def create_correlation_summary_chart(self, insights: Dict[str, any]) -> go.Figure:
        """Create a summary chart of correlation insights"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Average Correlation', 'Diversification Score', 
                          'High Correlations Count', 'Risk Level'),
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "bar"}, {"type": "indicator"}]]
        )
        
        # Average correlation gauge
        fig.add_trace(go.Indicator(
            mode = "gauge+number",
            value = insights['avg_correlation'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Avg Correlation"},
            gauge = {
                'axis': {'range': [-1, 1]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [-1, -0.5], 'color': "lightgreen"},
                    {'range': [-0.5, 0.5], 'color': "yellow"},
                    {'range': [0.5, 1], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 0.7
                }
            }
        ), row=1, col=1)
        
        # Diversification score gauge
        fig.add_trace(go.Indicator(
            mode = "gauge+number",
            value = insights['diversification_score'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Diversification Score"},
            gauge = {
                'axis': {'range': [0, 1]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 0.3], 'color': "lightcoral"},
                    {'range': [0.3, 0.7], 'color': "yellow"},
                    {'range': [0.7, 1], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 0.5
                }
            }
        ), row=1, col=2)
        
        # High correlations count
        high_corr_count = len(insights['high_correlations'])
        fig.add_trace(go.Bar(
            x=['High Correlations'],
            y=[high_corr_count],
            marker_color='lightcoral',
            text=[str(high_corr_count)],
            textposition='auto'
        ), row=2, col=1)
        
        # Risk level indicator
        risk_level = "Low" if insights['diversification_score'] > 0.7 else "Medium" if insights['diversification_score'] > 0.4 else "High"
        risk_color = "green" if risk_level == "Low" else "orange" if risk_level == "Medium" else "red"
        
        fig.add_trace(go.Indicator(
            mode = "number",
            value = 1 if risk_level == "Low" else 2 if risk_level == "Medium" else 3,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"Risk Level: {risk_level}"},
            number = {'font': {'color': risk_color, 'size': 40}}
        ), row=2, col=2)
        
        fig.update_layout(
            title="Correlation Analysis Summary",
            height=600,
            showlegend=False
        )
        
        return fig
