from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import torch

model_id = "meta-llama/Llama-3.2-3B-Instruct"
# Carica il tokenizer

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

# Metti il modello in modalità eval per inferenza
model.eval()

print(f"Modello caricato: {model.config._name_or_path}")
param_name, param_value = list(model.named_parameters())[0]
print(f"🔍 Primo parametro del modello: {param_name} -> Valore medio: {param_value.mean().item()}")

print("Modello Caricato correttamente")

# Caricamento del log da analizzare
log_path = "../datasets/logs/log_0001.json"

with open(log_path, "r") as file:
    log_entry = json.load(file)

def fileopen(percorso):
    with open(percorso,"r",encoding="utf-8") as f:
        return f.read()

prompt = fileopen("../datasets/prompt.txt")

def analyze_logs(log_entry):
    instruction_text = prompt
    
    input_text = f"""
    - Fase della Kill Chain: {log_entry['kill_chain_phase']}
    - Tecnica MITRE ATT&CK: {log_entry['mitre_technique']}
    - IP sorgente: {log_entry['source_ip']}
    - IP destinazione: {log_entry['destination_ip']}
    - Azione rilevata: {log_entry['action']}
    
    Quali sono i possibili rischi, come mitigare questo attacco o i passi successivi da compiere?
    """

    local_prompt = ( 
        f"### Istruzione:\n{instruction_text}\n\n"
        f"### Input:\n{input_text}\n\n"
        f"### Risposta:\n"
    )

    print("\n🔍 DEBUG: PROMPT INVIATO AL MODELLO:\n")
    print(prompt)

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids

    print(f"Numero di token nel prompt: {input_ids.shape[1]}")  # Debug: numero token del prompt

    with torch.no_grad():
        outputs = model.generate(
        input_ids=input_ids,
        max_length=1024,  # Evita generazioni troppo lunghe
        do_sample=False,   # Evita risultati casuali
        repetition_penalty=1.2,
        eos_token_id=tokenizer.eos_token_id  
    )

    print(f"Numero di token nella risposta: {outputs.shape[1]}")  # Debug: numero token della risposta

    response = tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True)

    return response

# Test tokenizzazione
testo = "Analizza questo log di sicurezza e fornisci una valutazione dettagliata."
tokens = tokenizer.encode(testo, return_tensors="pt")
print("Esempio di tokenizzazione:", tokens)

# Analisi log
response = analyze_logs(log_entry)

print(f"\nAnalisi log:\n{response}")
