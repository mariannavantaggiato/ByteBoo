import json
import os
from mitre_info_extractor import get_mitre_info  # Importiamo la funzione da ai_module.py

LOG_DIR = "../datasets/logs"
OUTPUT_FILE = "../datasets/dataset_unito.json"

# Funzione per unire i log con il dataset MITRE
def process_logs():
    dataset_unito = []

    for log_file in os.listdir(LOG_DIR):
        if log_file.endswith(".json"):
            log_path = os.path.join(LOG_DIR, log_file)
            with open(log_path, "r") as file:
                log_data = json.load(file)
                
                # Arricchire il log con info MITRE
                mitre_info = get_mitre_info(log_data["mitre_technique"])
                if mitre_info:
                    log_data.update(mitre_info)

                dataset_unito.append(log_data)

    # Scrivi il dataset unito
    with open(OUTPUT_FILE, "w") as dataset_file:
        json.dump(dataset_unito, dataset_file, indent=4)

    print(f"Dataset unito aggiornato con {len(dataset_unito)} log.")

if __name__ == "__main__":
    process_logs()



