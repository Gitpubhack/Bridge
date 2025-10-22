"""
OpenAI Assistant for Bridge Exchange
"""
import openai
from typing import Dict, Any, List, Optional
from config import OPENAI_API_KEY, TEST_MODE

class OpenAIAssistant:
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.test_mode = TEST_MODE
        
        if not self.test_mode and self.api_key and not self.api_key.startswith("TODO"):
            openai.api_key = self.api_key
    
    async def analyze_portfolio(
        self, 
        user_balances: Dict[str, float],
        trade_history: List[Dict[str, Any]],
        market_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze user portfolio and provide recommendations"""
        if self.test_mode or not self.api_key or self.api_key.startswith("TODO"):
            return {
                "risk_level": "medium",
                "total_value_usd": 10000.0,
                "suggestions": [
                    {
                        "type": "diversification",
                        "title": "Diversify Your Portfolio",
                        "description": "Consider adding more altcoins to reduce Bitcoin concentration",
                        "priority": "high"
                    },
                    {
                        "type": "rebalancing", 
                        "title": "Rebalance Holdings",
                        "description": "Your portfolio is 80% Bitcoin. Consider reducing to 60%",
                        "priority": "medium"
                    },
                    {
                        "type": "staking",
                        "title": "Start Staking",
                        "description": "Consider staking your USDT for 5% APY rewards",
                        "priority": "low"
                    }
                ],
                "allocation_changes": [
                    {
                        "asset": "BTC",
                        "current_percentage": 80.0,
                        "recommended_percentage": 60.0,
                        "action": "reduce"
                    },
                    {
                        "asset": "ETH",
                        "current_percentage": 15.0,
                        "recommended_percentage": 25.0,
                        "action": "increase"
                    },
                    {
                        "asset": "USDT",
                        "current_percentage": 5.0,
                        "recommended_percentage": 15.0,
                        "action": "increase"
                    }
                ],
                "market_insights": [
                    "Bitcoin showing strong support at $45,000",
                    "Ethereum network upgrades driving adoption",
                    "DeFi tokens showing increased volatility"
                ]
            }
        
        # Prepare context for OpenAI
        portfolio_summary = f"""
        User Portfolio Analysis:
        - Total Balance: {sum(user_balances.values()):.2f} USD
        - Asset Distribution: {user_balances}
        - Recent Trades: {len(trade_history)} transactions
        - Market Conditions: {market_data.get('trend', 'neutral')}
        """
        
        system_prompt = """You are an expert crypto analyst and compliance-aware assistant for Bridge Exchange. 
        Analyze the user's portfolio and provide:
        1. Risk assessment (low/medium/high)
        2. 3 actionable recommendations with priorities
        3. Suggested allocation changes
        4. Market insights
        
        Be conservative, compliance-focused, and educational. Never provide financial advice."""
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": portfolio_summary}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            # Parse the response (in a real implementation, you'd parse the JSON response)
            return {
                "risk_level": "medium",
                "total_value_usd": sum(user_balances.values()),
                "suggestions": [
                    {
                        "type": "diversification",
                        "title": "Diversify Portfolio",
                        "description": "Consider adding more asset classes",
                        "priority": "high"
                    }
                ],
                "allocation_changes": [],
                "market_insights": ["Market analysis based on current conditions"]
            }
            
        except Exception as e:
            # Fallback to test mode response
            return await self.analyze_portfolio(user_balances, trade_history, market_data)
    
    async def chat_assistant(
        self, 
        user_message: str, 
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Chat assistant with context"""
        if self.test_mode or not self.api_key or self.api_key.startswith("TODO"):
            return {
                "response": "I'm here to help with your Bridge Exchange questions! How can I assist you today?",
                "suggestions": [
                    "How do I deposit funds?",
                    "What are the trading fees?",
                    "How does staking work?",
                    "How to withdraw to my wallet?"
                ],
                "related_actions": [
                    {
                        "type": "open_deposit",
                        "title": "Make a Deposit",
                        "description": "Start depositing funds to your account"
                    },
                    {
                        "type": "view_balances",
                        "title": "Check Balances", 
                        "description": "View your current account balances"
                    }
                ]
            }
        
        system_prompt = """You are a helpful assistant for Bridge Exchange, a crypto trading platform. 
        Help users with:
        - Trading questions
        - Deposit/withdrawal guidance
        - Platform features
        - Security best practices
        
        Be friendly, accurate, and always recommend checking official documentation."""
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return {
                "response": response.choices[0].message.content,
                "suggestions": [
                    "How do I deposit funds?",
                    "What are the trading fees?",
                    "How does staking work?"
                ],
                "related_actions": []
            }
            
        except Exception as e:
            return {
                "response": "I'm here to help with your Bridge Exchange questions! How can I assist you today?",
                "suggestions": [
                    "How do I deposit funds?",
                    "What are the trading fees?",
                    "How does staking work?"
                ],
                "related_actions": []
            }
    
    async def generate_trading_signal(
        self, 
        pair: str, 
        market_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate trading signal based on market analysis"""
        if self.test_mode or not self.api_key or self.api_key.startswith("TODO"):
            return {
                "pair": pair,
                "signal": "hold",
                "confidence": 0.6,
                "reasoning": "Market showing mixed signals, recommend holding current position",
                "price_targets": {
                    "support": 45000.0,
                    "resistance": 52000.0
                },
                "risk_level": "medium",
                "timeframe": "24h"
            }
        
        system_prompt = f"""Analyze the market data for {pair} and provide a trading signal.
        Consider technical indicators, market sentiment, and risk factors.
        Provide: signal (buy/sell/hold), confidence (0-1), reasoning, price targets, risk level."""
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Market data: {market_data}"}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            return {
                "pair": pair,
                "signal": "hold",
                "confidence": 0.6,
                "reasoning": response.choices[0].message.content,
                "price_targets": {
                    "support": 45000.0,
                    "resistance": 52000.0
                },
                "risk_level": "medium",
                "timeframe": "24h"
            }
            
        except Exception as e:
            return await self.generate_trading_signal(pair, market_data)
