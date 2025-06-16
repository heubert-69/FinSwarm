import os
from agents.research import ResearchAgent
from agents.risk import RiskAgent
from agents.report import ReportAgent
from llm.phi_llm import PhiLLM


class FinSwarm:
	def __init__(self):
		self.research_agent = ResearchAgent()
		self.risk_agent = RiskAgent()
		self.report_agent = ReportAgent()
		self.model = PhiLLM()
		self.output_dir = "output"
		os.makedirs(self.output_dir, exist=True)
	def run(self, tickers):
		print("Starting FinSwarm Automation...")

		#running my research agent to collect information
		info = self.research_agent.collect(tickers)
		print(f"Information on {tickers} collected!")

		#using risk analysis to perform on tickers
		risk = self.risk_agent.analyze(tickers)
		print(f"Performing Risk Analysis...")

		#Summarizing reports and using The Phi model to improve better understanding
		print(f"Writing Reports on {tickers}....")
		report_path = os.path.join(self.output_dir, "Analysis Result.pdf")

		self.report_agent.generate_report(
            		tickers=self.tickers,
            		research_data=info,
            		risk_data=risk,
            		llm=self.model,
            		output_path=report_path
        	)
		print(f"Done! Report saved to: {report_path}")



if __name__ == "__main__":
	#Testing
	tickers = ["TSLA", "AAPL"]

	app = FinSwarm(tickers)
	app.run()
