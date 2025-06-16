# 🐝 FinSwarm: AI-Powered Financial Research Assistant

**🏆 Hackathon Submission – IBM TechXchange Day – June 26, 2025**

FinSwarm is an AI-powered research agent that helps investors and analysts collect, summarize, and analyze financial market data using LLMs, stock APIs, and macroeconomic indicators. It streamlines your equity research workflow by combining company fundamentals, price histories, and macroeconomic data into actionable insights.

This project was developed as a **hackathon submission** for the **IBM TechXchange Day Hackathon 2025**, where participants were tasked with building real-world solutions using AI and data.

---

## 🔍 Features

- 📈 Fetches real-time **stock price history** and **fundamental data** via [Yahoo Finance](https://finance.yahoo.com/)
- 📊 Gathers key **macroeconomic indicators** (CPI, GDP, Unemployment, Interest Rates) from the **FRED API**
- 🧠 Uses **local LLMs** (Phi-2 via HuggingFace Transformers) for summarizing and reasoning over data
- 🔐 `.env` configuration support for API tokens (secure and extensible)
- 🐳 Docker-ready for deployment (local setup working; cloud coming soon)
- ✅ Open Source (MIT License)

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/finswarm.git
cd finswarm
```

### 2. Install dependencies
Using Python 3.10 or above:

```bash
pip install -r requirements.txt
```

### 3. Create a .env file
```bash
FRED_API_KEY=your_fred_api_key
HF_TOKEN=your_huggingface_token
```

🛠️ Running Locally
You can test the pipeline via the test script:

bash
Copy
Edit
python test_llm.py
This script will:

Fetch financial data for companies (e.g., AAPL, MSFT)

Retrieve CPI, GDP, unemployment, and interest rates from FRED

Generate insights using the local LLM (Phi-2)

Output the summary and research insights

🧠 LLM Model
Model used: microsoft/phi-1.5

Loaded via HuggingFace Transformers

Quantization support via bitsandbytes (runs CPU if CUDA unavailable)

🐳 Docker Support
🧪 Run Locally with Docker

Build the image:

```bash
docker build -t finswarm .
```

Run the container:

```bash
docker run --env-file .env -p 8501:8501 finswarm
```

🌐 Docker Cloud Support (Coming Soon)
I plan to deploy this on DockerHub / Docker Cloud before or after the hackathon ends. The system is container-ready.

🧪 Project Structure
```pgsql
finswarm/
│
├── llm/
│   ├── phi_llm.py       # Local LLM wrapper
│   └── test_llm.py      # CLI-based test script
│
├── agents/
│   ├── research.py      # Collects price, fundamentals, and macro data
│   └── risk.py          # (In progress) Risk analysis
│
├── .env                 # Secrets for HuggingFace and FRED
├── Dockerfile           # Docker container definition
├── requirements.txt     # Python dependencies
└── README.md            # This file
```
📢 CLI Usage
```bash
python test_llm.py
```

Expected Output:

Company summaries (market cap, P/E ratio, EPS, dividend, sector, etc.)

Macro data overview (GDP, CPI, etc.)

Research-grade AI summary from LLM

⚙️ Tech Stack
Python 3.10+

HuggingFace Transformers

yfinance

fredapi

dotenv

bitsandbytes (optional CUDA support)

Docker

📄 License
This project is licensed under the MIT License. See LICENSE for details.

🙋‍♂️ Author
Created by Heubert-69/Jorge Jarme
Hackathon Submission | IBM TechXchange Day 2025

🤝 Contributing
Pull requests and suggestions are welcome! Please fork this repo and open a PR.
