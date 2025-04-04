import json
import random
import os
from datetime import datetime

# Definiamo le fasi della MITRE ATT&CK Kill Chain con tecniche di esempio
kill_chain = {
    "Reconnaissance": ["T1595", "T1598", "T1592"],
    "Resource Development": ["T1583", "T1584", "T1585"],
    "Initial Access": ["T1078", "T1190", "T1133"],
    "Execution": ["T1059", "T1203", "T1047"],
    "Persistence": ["T1098", "T1547", "T1505"],
    "Privilege Escalation": ["T1068", "T1548", "T1134"],
    "Defense Evasion": ["T1070", "T1027", "T1211"],
    "Credential Access": ["T1003", "T1555", "T1552"],
    "Discovery": ["T1012", "T1046", "T1482"],
    "Lateral Movement": ["T1570", "T1550", "T1021"],
    "Collection": ["T1114", "T1005", "T1056"],
    "Command and Control": ["T1071", "T1095", "T1105"],
    "Exfiltration": ["T1567", "T1020", "T1041"],
    "Impact": ["T1486", "T1490", "T1529"]
}

# Percorso per salvare i log
log_dir = "../datasets/logs"
os.makedirs(log_dir, exist_ok=True)

dataset_path = "../datasets/dataset_unito.json"
dataset_unito = []

# Carica il dataset esistente per evitare duplicati
if os.path.exists(dataset_path):
    with open(dataset_path, "r") as dataset_file:
        try:
            dataset_unito = json.load(dataset_file)
        except json.JSONDecodeError:
            dataset_unito = []

existing_log_ids = {entry["log_id"] for entry in dataset_unito}

# Trova l'ultimo numero di log per continuare in ordine decrescente
existing_logs = [int(file.split("_")[1].split(".")[0]) for file in os.listdir(log_dir) if file.startswith("log_") and file.endswith(".json")]
next_log_number = max(existing_logs) + 1 if existing_logs else 1

# Generazione di 50 log con timestamp sempre diversi
for i in range(50):
    phase = random.choice(list(kill_chain.keys()))
    technique = random.choice(kill_chain[phase])
    timestamp = datetime.now().isoformat()
    log_id = f"log_{next_log_number:04d}"
    
    if log_id in existing_log_ids:
        continue  # Evita duplicati

    log_entry = {
        "timestamp": timestamp,
        "log_id": log_id,
        "kill_chain_phase": phase,
        "mitre_technique": technique,
        "source_ip": f"192.168.{random.randint(1,255)}.{random.randint(1,255)}",
        "destination_ip": f"10.0.{random.randint(1,255)}.{random.randint(1,255)}",
        "action": random.choice(["Allowed", "Blocked", "Detected", "Quarantined"])
    }
    
    # Salva ogni log in un file JSON separato con un nome ordinato decrescente
    log_filename = os.path.join(log_dir, f"{log_id}.json")
    with open(log_filename, "w") as log_file:
        json.dump(log_entry, log_file, indent=4)
    
    # Aggiunge il log al dataset unito
    dataset_unito.append(log_entry)
    existing_log_ids.add(log_id)
    next_log_number += 1

# Salva il dataset unito aggiornato senza sovrascrivere i dati esistenti
with open(dataset_path, "w") as dataset_file:
    json.dump(dataset_unito, dataset_file, indent=4)

print("Generazione completata! 50 log creati con numerazione decrescente, dataset unito aggiornato.")
