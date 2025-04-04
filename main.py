# main.py - Gestione simulazioni e invocazione AI
import json
import os
from script.preprocessor import preprocess_log
from script.mitre_info_extractor import analyze_log

# Percorsi delle cartelle
DATASET_DIR = "datasets"
LOGS_DIR = os.path.join(DATASET_DIR, "logs")
RESULTS_DIR = os.path.join(DATASET_DIR, "results")
PREPROCESSED_DIR = os.path.join(DATASET_DIR, "preprocessed")

# Assicurati che le cartelle results e preprocessed esistano
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(PREPROCESSED_DIR, exist_ok=True)

def carica_scenari():
    """Carica tutti i log dal dataset unificato."""
    dataset_path = os.path.join(DATASET_DIR, "dataset_unito.json")
    with open(dataset_path, "r", encoding="utf-8") as f:
        return json.load(f)  # Carica tutti i log

def esegui_simulazioni():
    """Esegue l'analisi sui log caricati dal dataset_unito.json."""
    scenari = carica_scenari()

    for scenario in scenari:
        log_file = f"{scenario['id']}.json"  # Identificatore del log
        log_path = os.path.join(LOGS_DIR, log_file)

        # Salva il log originale nei file singoli (opzionale se già presenti)
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(scenario, f, indent=4)

        # Preprocessa il log
        preprocessed_log = preprocess_log(scenario)

        # Salva il log preprocessato
        preprocessed_path = os.path.join(PREPROCESSED_DIR, log_file)
        with open(preprocessed_path, "w", encoding="utf-8") as f:
            json.dump(preprocessed_log, f, indent=4)

        # Analizza il log con il modello AI
        result = analyze_log(preprocessed_log)

        # Salva il risultato
        result_path = os.path.join(RESULTS_DIR, f"{scenario['id']}_result.json")
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)

        print(f"Analizzato {log_file} → Salvato in {result_path}")

if __name__ == "__main__":
    esegui_simulazioni()
    print("Simulazioni completate. Controlla la cartella datasets/results/ per i risultati.")
