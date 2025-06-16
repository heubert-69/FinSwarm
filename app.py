import streamlit as st
import os
from datetime import datetime
from agents.research import ResearchAgent
from agents.risk import RiskAgent
from agents.report import ReportAgent
from llm.phi_llm import PhiLLM
from fpdf import FPDF
import matplotlib.pyplot as plt
from textblob import TextBlob
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

#using my api keys
load_dotenv()


st.set_page_config(page_title="FinSwarm AI", layout="wide")

st.title("🚀 FinSwarm: Autonomous Finance Agents")
tickers = st.text_input("Enter comma-separated tickers", "TSLA,SPY")
period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y"], index=1)

st.sidebar.markdown("📬 **Get Report via Email**")
user_email = st.sidebar.text_input("Your Email", placeholder="you@example.com")


# --- Save Report as PDF ---
def save_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)

#email
def send_email_with_report(recipient_email, report_path):
    try:
        msg = EmailMessage()
        msg["Subject"] = "📊 Your FinSwarm Financial Report"
        msg["From"] = os.getenv("EMAIL_ADDRESS")
        msg["To"] = recipient_email
        msg.set_content("Hi! Your FinSwarm report is attached as a PDF.\n\nThanks for using FinSwarm 🚀")

        # Attach PDF
        with open(report_path, "rb") as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=os.path.basename(report_path))

        # SMTP Send
        with smtplib.SMTP(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT"))) as smtp:
            smtp.starttls()
            smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
            smtp.send_message(msg)
        return True

    except Exception as e:
        print("Error sending email:", e)
        return False


# --- Plot price history ---
def plot_price_history(prices_dict):
    fig, ax = plt.subplots(figsize=(10, 4))
    for ticker, df in prices_dict.items():
        ax.plot(df.index, df["Close"], label=ticker)
    ax.set_title("Price History")
    ax.set_xlabel("Date")
    ax.set_ylabel("Close Price")
    ax.legend()
    st.pyplot(fig)

# --- Plot volatility ---
def plot_volatility(risk_data):
    fig, ax = plt.subplots()
    tickers = list(risk_data.keys())
    volatilities = [risk_data[t]["volatility"] for t in tickers]
    ax.bar(tickers, volatilities, color='orange')
    ax.set_title("Volatility")
    ax.set_ylabel("Standard Deviation")
    st.pyplot(fig)

# --- Show sentiment gauge ---
def plot_sentiment_gauge(fundamentals):
    st.subheader("🧠 Sentiment Score (Summary Text)")

    for ticker, info in fundamentals.items():
        summary = info.get("summary", "")
        polarity = TextBlob(summary).sentiment.polarity
        sentiment = "Neutral"
        if polarity > 0.1:
            sentiment = "Positive"
        elif polarity < -0.1:
            sentiment = "Negative"

        st.markdown(f"**{ticker}** – {sentiment} (score: {round(polarity, 2)})")
        st.progress((polarity + 1) / 2)

if st.button("Run Analysis"):
    tickers_list = [t.strip().upper() for t in tickers.split(",")]

    with st.spinner("🔍 Collecting data..."):
        research = ResearchAgent(os.getenv("FRED_API_KEY"))
        research_data = research.collect(tickers_list)

    with st.spinner("📊 Analyzing risk..."):
        risk = RiskAgent()
        risk_data = risk.analyze(research_data)

    with st.spinner("🧠 Generating report..."):
        llm = PhiLLM()
        report = ReportAgent(llm)
        markdown_report = report.generate_markdown(research_data, risk_data, tickers_list)

        # Save markdown and PDF
        date = datetime.today().strftime("%Y%m%d")
        md_path = f"output/report_{date}.md"
        pdf_path = f"output/report_{date}.pdf"

        with open(md_path, "w") as f:
            f.write(markdown_report)
        save_pdf(markdown_report, pdf_path)

    st.success("✅ Report generated!")
    st.markdown(markdown_report)
    st.download_button("📄 Download PDF", data=open(pdf_path, "rb"), file_name=f"FinSwarm_Report_{date}.pdf")

    # Charts
    st.subheader("📈 Price History")
    plot_price_history(research_data["prices"])

    st.subheader("📉 Volatility Chart")
    plot_volatility(risk_data)

    # Sentiment
    plot_sentiment_gauge(research_data["fundamentals"])

if user_email and st.sidebar.button("📤 Send Me the Report"):
    success = send_email_with_report(user_email, pdf_path)
    if success:
        st.sidebar.success(f"✅ Sent to {user_email}")
    else:
        st.sidebar.error("❌ Failed to send email. Check server logs.")
