import json
from lmm_helper import get_mitre_suggestions
from datetime import datetime

#carica dataset
with open("percorso", "r") as file:
	logs = [json.loads(line) for line in file]

results = []

for log in logs:
	phase = log['kill_chain_phase']
	description = log['description']
	real_techniques = log['real_techniques']  # lista di tecniche MITRE realmente usate

	print(f"Analizzo log - Fase: {phase}")

	#Chiamata all'AI  generativa (LMM/LLM) per suggerire le tecniche
	suggested_techniques = get_mitre_suggestions(phase, description)

	#Valutazione: confrontro tra reali e suggerite
	correct = len(set(real_techniques) & set(suggested_techniques))
	false_positives = len(set(suggested_techniques) - set(real_techniques))
	false_negatives = len(set(real_techniques) - set(suggested_techniques))

	results.append({
		"timestamp" : datetime.now().isoformat(),
		"phase" : phase,
		"real_techniques" : real_techniques,
		"suggested_techniques" : suggested_techniques,
		"correct" : correct,
		"false_positives" : false_positives,
		"false_negatives" : false_negatives
	})

#Salva risultati
with open("../results/results_summary.json", "w") as out_file:
	json.dump(results, out_file, indent=4)

print("Analisi completata. Report salvato in reports/results_summary.json")

