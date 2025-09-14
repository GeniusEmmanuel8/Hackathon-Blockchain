import google.generativeai as genai
import json
import pandas as pd
from typing import Dict, Any, Optional

class AIInsightsGenerator:
    def __init__(self, api_key: str):
        """Initialize the AI insights generator with Google Gemini API key"""
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.enabled = True
        else:
            self.enabled = False
    
    def generate_insights(self, portfolio_data, risk_metrics) -> Dict[str, str]:
        """Generate AI-powered insights for the portfolio"""
        if not self.enabled:
            return self._get_fallback_insights(portfolio_data, risk_metrics)
        
        try:
            # Prepare portfolio summary for AI analysis
            portfolio_summary = self._prepare_portfolio_summary(portfolio_data, risk_metrics)
            
            # Generate insights using Gemini
            insights = self._call_gemini_api(portfolio_summary)
            
            return insights
            
        except Exception as e:
            print(f"Error generating AI insights: {e}")
            return self._get_fallback_insights(portfolio_data, risk_metrics)
    
    def _prepare_portfolio_summary(self, portfolio_data, risk_metrics) -> str:
        """Prepare a summary of the portfolio for AI analysis"""
        total_value = portfolio_data['value_usd'].sum()
        num_tokens = len(portfolio_data)
        
        # Top holdings
        top_holdings = portfolio_data.nlargest(5, 'value_usd')[['symbol', 'value_usd', 'weight']].to_dict('records')
        
        # Risk metrics
        volatility = risk_metrics.get('portfolio_volatility', 0)
        sharpe_ratio = risk_metrics.get('sharpe_ratio', 0)
        concentration_risk = risk_metrics.get('concentration_risk', 'Unknown')
        correlation_risk = risk_metrics.get('correlation_risk', 'Unknown')
        
        summary = f"""
Portfolio Analysis Summary:
- Total Value: ${total_value:,.2f}
- Number of Tokens: {num_tokens}
- Portfolio Volatility: {volatility:.2%}
- Sharpe Ratio: {sharpe_ratio:.2f}
- Concentration Risk: {concentration_risk}
- Correlation Risk: {correlation_risk}

Top Holdings:
"""
        
        for holding in top_holdings:
            summary += f"- {holding['symbol']}: ${holding['value_usd']:,.2f} ({holding['weight']:.1%})\n"
        
        return summary
    
    def _call_gemini_api(self, portfolio_summary: str) -> Dict[str, str]:
        """Call Gemini API to generate insights"""
        try:
            prompt = f"""You are a professional cryptocurrency portfolio risk analyst. 
            Analyze the provided Solana portfolio data and provide:
            1. A clear analysis of the portfolio's risk profile
            2. Risk assessment highlighting key concerns
            3. Specific, actionable recommendations for improvement
            
            Be concise, professional, and focus on practical advice.
            
            Portfolio data:
            {portfolio_summary}
            
            Please provide your analysis in the following format:
            ANALYSIS: [Your portfolio analysis here]
            RISK ASSESSMENT: [Your risk assessment here]
            RECOMMENDATIONS: [Your recommendations here]"""
            
            response = self.model.generate_content(prompt)
            ai_response = response.text
            
            # Parse the response into structured insights
            return self._parse_ai_response(ai_response)
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._get_fallback_insights(None, None)
    
    def _parse_ai_response(self, ai_response: str) -> Dict[str, str]:
        """Parse AI response into structured insights"""
        # Simple parsing - in a real implementation, you might use more sophisticated parsing
        lines = ai_response.split('\n')
        
        analysis = []
        risk_assessment = []
        recommendations = []
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if 'analysis' in line.lower() or 'portfolio' in line.lower():
                current_section = 'analysis'
            elif 'risk' in line.lower() and 'assessment' in line.lower():
                current_section = 'risk'
            elif 'recommendation' in line.lower() or 'suggest' in line.lower():
                current_section = 'recommendations'
            elif line.startswith('-') or line.startswith('•'):
                if current_section == 'recommendations':
                    recommendations.append(line[1:].strip())
                else:
                    recommendations.append(line)
            else:
                if current_section == 'analysis':
                    analysis.append(line)
                elif current_section == 'risk':
                    risk_assessment.append(line)
                elif current_section == 'recommendations':
                    recommendations.append(line)
        
        return {
            'analysis': '\n'.join(analysis) if analysis else ai_response,
            'risk_assessment': '\n'.join(risk_assessment) if risk_assessment else "Risk assessment not available",
            'recommendations': '\n'.join(recommendations) if recommendations else "Recommendations not available"
        }
    
    def _get_fallback_insights(self, portfolio_data, risk_metrics) -> Dict[str, str]:
        """Provide fallback insights when AI is not available"""
        if portfolio_data is None or risk_metrics is None:
            return {
                'analysis': "AI insights are not available. Please provide an OpenAI API key for enhanced analysis.",
                'risk_assessment': "Risk assessment requires AI analysis.",
                'recommendations': "Recommendations require AI analysis."
            }
        
        # Generate basic insights based on risk metrics
        volatility = risk_metrics.get('portfolio_volatility', 0)
        sharpe_ratio = risk_metrics.get('sharpe_ratio', 0)
        concentration_risk = risk_metrics.get('concentration_risk', 'Unknown')
        
        analysis = f"""
Portfolio Analysis:
Your portfolio has a volatility of {volatility:.1%} and a Sharpe ratio of {sharpe_ratio:.2f}.
The concentration risk is currently {concentration_risk.lower()}.
"""
        
        risk_assessment = []
        if volatility > 0.3:
            risk_assessment.append("High volatility detected - portfolio may experience significant price swings")
        if sharpe_ratio < 0.5:
            risk_assessment.append("Low Sharpe ratio suggests poor risk-adjusted returns")
        if concentration_risk == 'High':
            risk_assessment.append("High concentration risk - portfolio is not well diversified")
        
        recommendations = []
        if volatility > 0.3:
            recommendations.append("Consider adding stablecoins or less volatile assets to reduce overall volatility")
        if sharpe_ratio < 0.5:
            recommendations.append("Review your asset allocation to improve risk-adjusted returns")
        if concentration_risk == 'High':
            recommendations.append("Diversify your portfolio by adding more different types of tokens")
        
        return {
            'analysis': analysis,
            'risk_assessment': '\n'.join(risk_assessment) if risk_assessment else "Portfolio risk appears manageable",
            'recommendations': '\n'.join(recommendations) if recommendations else "Portfolio appears well-balanced"
        }
    
    def generate_what_if_scenario(self, portfolio_data, scenario_type: str) -> Dict[str, Any]:
        """Generate what-if scenario analysis"""
        if not self.enabled:
            return self._get_fallback_scenario(portfolio_data, scenario_type)
        
        try:
            scenario_prompt = self._create_scenario_prompt(portfolio_data, scenario_type)
            
            response = self.model.generate_content(scenario_prompt)
            
            return {
                'scenario': scenario_type,
                'analysis': response.text,
                'generated_at': str(pd.Timestamp.now())
            }
            
        except Exception as e:
            print(f"Error generating scenario: {e}")
            return self._get_fallback_scenario(portfolio_data, scenario_type)
    
    def _create_scenario_prompt(self, portfolio_data, scenario_type: str) -> str:
        """Create a prompt for scenario analysis"""
        portfolio_summary = self._prepare_portfolio_summary(portfolio_data, {})
        
        scenarios = {
            'market_crash': "Analyze what would happen to this portfolio in a 50% market crash scenario",
            'bull_market': "Analyze potential performance in a 100% bull market scenario",
            'rebalancing': "Suggest optimal rebalancing strategy for this portfolio",
            'diversification': "Analyze the impact of adding 20% allocation to stablecoins"
        }
        
        scenario_description = scenarios.get(scenario_type, "Analyze this portfolio scenario")
        
        return f"""
{portfolio_summary}

Scenario: {scenario_description}

Please provide:
1. Expected impact on portfolio value
2. Risk implications
3. Recommended actions
4. Key metrics to monitor
"""
    
    def _get_fallback_scenario(self, portfolio_data, scenario_type: str) -> Dict[str, Any]:
        """Provide fallback scenario analysis"""
        return {
            'scenario': scenario_type,
            'analysis': f"Scenario analysis for {scenario_type} is not available without AI integration.",
            'generated_at': str(pd.Timestamp.now())
        } 