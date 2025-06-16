import yfinance as yf
from fredapi import Fred
import numpy as np
from datetime import datetime, timedelta
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

class ResearchAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("FRED_API_KEY")
        self.fred = Fred(api_key=self.api_key)

    def get_price_data(self, tickers, period="3mo"):
        data = {}
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            history = stock.history(period=period)
            data[ticker] = history
        return data

    def get_fundamentals(self, tickers):
        fundamentals = {}
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            info = stock.info
            fundamentals[ticker] = {
                "marketCap": info.get("marketCap"),
                "peRatio": info.get("trailingPE"),
                "forwardPE": info.get("forwardPE"),
                "eps": info.get("trailingEps"),
                "dividendYield": info.get("dividendYield"),
                "beta": info.get("beta"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "summary": info.get("longBusinessSummary")
            }
        return fundamentals

    def get_macro_data(self):
        today = datetime.today()
        start = today - timedelta(days=365)

        cpi = self.fred.get_series("CPIAUCNS", start)
        interest_rate = self.fred.get_series("FEDFUNDS", start)
        gdp = self.fred.get_series("GDP", start)
        unemployment = self.fred.get_series("UNRATE", start)

        return {
            "CPI": cpi,
            "Interest Rate": interest_rate,
            "GDP": gdp,
            "Unemployment": unemployment
        }

    def collect(self, tickers):
        return {
            "prices": self.get_price_data(tickers),
            "fundamentals": self.get_fundamentals(tickers),
            "macro": self.get_macro_data()
        }