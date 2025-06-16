import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import warnings
warnings.filterwarnings("ignore") #to make the warnings cheat on you like your ex girlfriend

class PhiLLM:
	def __init__(self, model_name="microsoft/phi-1", device=None):
		self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
		self.tokenizer = AutoTokenizer.from_pretrained(model_name)
		self.model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True).to(self.device)
		self.model.eval()
	def generate(self, prompt, max_tokens=200):
		inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
		with torch.no_grad():
			outputs =  self.model.generate(
				**inputs,
				max_new_tokens=max_tokens,
				temperature=0.7,
				top_k=50,
				top_p=0.95,
				do_sample=True,
				pad_token_id=self.tokenizer.eos_token_id
			)
		return self.tokenizer.decode(outputs[0], skip_special_tokens=True).replace(prompt, "").strip()



