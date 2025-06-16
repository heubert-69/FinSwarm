from phi_llm import PhiLLM
phi = PhiLLM()

prompt = "Summarize The Risk profile of TSLA given High beta and sharp drawdowns:"

print(phi.generate(prompt))
