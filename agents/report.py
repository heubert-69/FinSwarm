import os
from datetime import datetime

class ReportAgent:
    def __init__(self, output_dir="output"):
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir

    def generate_summary(self, risk_data):
        summary = []
        for ticker, metrics in risk_data.items():
            line = f"**{ticker}**: "
            beta = metrics.get("beta")
            sharpe = metrics.get("sharpe_ratio")
            drawdown = metrics.get("max_drawdown")
            comment = metrics.get("risk_comment", "")

            if beta and beta > 1.5:
                profile = "High-risk, aggressive growth asset."
            elif beta and beta < 0.8:
                profile = "Defensive, low-beta asset."
            else:
                profile = "Moderate risk profile."

            summary.append(f"- {ticker}: {profile} {comment} Sharpe Ratio: {sharpe}, Max Drawdown: {drawdown}")
        return "\n".join(summary)

    def format_report(self, research, risk):
        today = datetime.today().strftime("%Y-%m-%d")
        tickers = list(research["prices"].keys())

        header = f"# FinSwarm Report – {', '.join(tickers)}\nGenerated: {today}\n\n"
        
        macro_section = "## 🏦 Macroeconomic Data\n"
        for key, series in research["macro"].items():
            macro_section += f"- **{key}** latest: {round(series.iloc[-1], 2)}\n"

        fundamentals_section = "## 📊 Fundamentals\n"
        for ticker, data in research["fundamentals"].items():
            fundamentals_section += f"### {ticker}\n"
            fundamentals_section += f"- Market Cap: {data.get('marketCap')}\n"
            fundamentals_section += f"- PE Ratio: {data.get('peRatio')}\n"
            fundamentals_section += f"- Forward PE: {data.get('forwardPE')}\n"
            fundamentals_section += f"- EPS: {data.get('eps')}\n"
            fundamentals_section += f"- Dividend Yield: {data.get('dividendYield')}\n"
            fundamentals_section += f"- Sector: {data.get('sector')}\n"
            fundamentals_section += f"- Industry: {data.get('industry')}\n"
            fundamentals_section += f"- Summary: {data.get('summary')[:200]}...\n\n"

        risk_section = "## ⚠️ Risk Analysis\n"
        for ticker, metrics in risk.items():
            risk_section += f"### {ticker}\n"
            risk_section += f"- Volatility: {metrics.get('volatility')}\n"
            risk_section += f"- Sharpe Ratio: {metrics.get('sharpe_ratio')}\n"
            risk_section += f"- Semi-Deviation: {metrics.get('semi_deviation')}\n"
            risk_section += f"- Max Drawdown: {metrics.get('max_drawdown')}\n"
            risk_section += f"- Beta: {metrics.get('beta')}\n"
            risk_section += f"- Risk Commentary: {metrics.get('risk_comment')}\n\n"

        summary_section = "## 🧠 Summary\n"
        summary_section += self.generate_summary(risk)

        return header + macro_section + "\n" + fundamentals_section + "\n" + risk_section + "\n" + summary_section

    def save_report(self, report_text, filename="report.pdf"):
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w") as f:
            f.write(report_text)
        print(f"✅ Report saved to: {filepath}")
        return filepath
