import json
from transformers import pipeline #O llama-cpp-python con modelli GGUF

def get_mitre_suggestions(phase, description):
	prompt = f"""
	You are a cybersecurity expert. Based on the MITRE ATT&CK framework, analyze this log:
	Kill Chain Phase: {phase}
	Log Description: {description}
	List all MITRE techniques (use IDs like T1566) that may apply, separated by commas.
	Response (only list techniques):
	"""

	
	generator = pipeline("text-generation", model="openlm-research/open_llama_3b")
	response = generator(prompt, max_length=200, do_sample=True)[0]['generated_text']
	
	#Estrazione delle tecniche della risposta
	techniques = [t.strip() for t in response.split(",") if t.startswith("T")]
	return techniques
