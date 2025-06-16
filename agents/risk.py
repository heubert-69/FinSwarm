import pandas as pd
import numpy as np

#We follow Professor Aswath Damodaran's Principles of Risk
class RiskAgent:
	def __init__(self, risk_free_rate=0.05):
		self.risk_free_rate = risk_free_rate / 252 #daily risk free rate
	def compute_volatility(self, prices):
		returns = prices.pct_change.dropna()
		return returns.std() * np.sqrt(252)

	def compute_semi_deviation(self, prices):
		returns = prices.pct_change.dropna()
		negative_returns = returns[returns < 0]
		return negative_returns.std() * np.sqrt(252)
	def compute_max_drawdown(self, prices):
		cumulative = (1 + prices.pct_change().dropna()).cumprod()
		peak = cumulative.cummax()
		drawdown = (cumulative - peak) / peak
		return drawdown.min()
	def compute_sharpe_ratio(self, prices):
		returns = prices.pct_change.dropna()
		excess_returns = returns - self.risk_free_rate
		sharpe = excess_returns.mean() / excess_returns.std()
		return sharpe
	def analyze_fundamentals(self, fundamentals):
		financial_risk = {}
		for ticker, info in fundamentals.items():
			if not info:
				financial_risk[ticker] = "Missing Data"
				continue
			pe = info.get("peRatio")
			beta = info.get("beta")
			dividend = info.get("dividendYield", None)
			financial_risk[ticker] = {"beta": beta, "pe_ratio": pe, "dividend_yield": dividend, "risk_comment": self.risk_comment_on_fundamentals(pe, beta)}
			return financial_risk
	def risk_comment_on_fundamentals(self, pe, beta):
		if beta is None:
			return "Beta is None!"
		elif beta > 1.5:
			return "High Market Risk"
		elif 1.0 < beta <= 1.5:
			return "Moderate Risk, Cyclical Exposure To The Economy"
		else:
			return "Asset is Either Stable or Defensive"
	def analyze(self, research_data):
		result = {}
		price_data = research_data["prices"]
		fundamentals = research_data["fundamentals"]
		for ticker, df in price_data.items():
			close_prices = df["Close"]
			result["ticker"] = {
				"Volatility": round(self.compute_volatility(close_prices), 4),
				"Semi-Deviation": round(self.compute_semi_deviation(close_prices), 4),
				"Sharpe-Ratio": round(self.compute_sharpe_ratio(close_prices), 4),
				"Max-Drawdown": round(self.compute_max_drawdown(close_prices), 4)
			}

		#Adding Fundamental Risk View
		fund_risk = self.analyze_fundamentals(fundamentals)
		for ticker in result:
			result["ticker"].update(fund_risk.get(ticker, {}))
		return result
