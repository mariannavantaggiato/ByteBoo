from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import torch

model_id = "swap-uniba/LLaMAntino-2-7b-hf-dolly-ITA"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

print("Modello Caricato correttamente")

response = ""

# Caricamento dei log da analizzare
#def load_logs(file_path="../datasets/dataset_unito.json"):
  #  with open(file_path, "r") as file:
   #     return json.load(file)

#logs = load_logs()

# Percorso del file log_0001.json
log_path = "../datasets/logs/log_0001.json"

# Carica il contenuto del file JSON
with open(log_path, "r") as file:
    log_entry = json.load(file)

def analyze_logs(log_entry):
    instruction_text = (
        "Sei un esperto di cybersecurity. Analizza il log di sicurezza fornito e rispondi seguendo questa struttura:\n\n"
        "1️ **Possibili rischi**: Elenca i rischi legati alla tecnica MITRE ATT&CK rilevata.\n"
        "2️ **Passi successivi per un attacco**: Descrivi cosa potrebbe fare un attaccante per sfruttare questa vulnerabilità.\n"
        "3️ **Mitigazione**: Spiega come difendersi e prevenire questo tipo di attacco.\n\n"
        "Rispondi in modo chiaro e dettagliato."
    )
    
    input_text = f"""
    - Fase della Kill Chain: {log_entry['kill_chain_phase']}
    - Tecnica MITRE ATT&CK: {log_entry['mitre_technique']}
    - IP sorgente: {log_entry['source_ip']}
    - IP destinazione: {log_entry['destination_ip']}
    - Azione rilevata: {log_entry['action']}
    
    Quali sono i possibili rischi, come mitigare questo attacco o i passi successivi da compiere?
    """

    prompt = ( 
        f"### Istruzione:\n{instruction_text}\n\n"
        f"### Input:\n{input_text}\n\n"
        f"### Risposta:\n"    )

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    with torch.no_grad():
        outputs = model.generate(
            input_ids=input_ids,
            max_length=1000,  # Aumenta la lunghezza massima della risposta
            temperature=0.7,  # Introduce un po' di casualità per risposte più varie
            top_p=0.9,  # Filtra le probabilità più alte per evitare output generici
            repetition_penalty=1.2  # Evita che ripeta le stesse frasi
        )

    response = tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True)

 
    return response

# Carica tutti i log
#logs = load_logs()

# Seleziona il primo log da analizzare
#log_entry = logs[0]

response = analyze_logs(log_entry)

print(f"\nAnalisi log:\n{response}")  # Stampa la risposta dell'AI
