# app.py - Backend della webapp
from flask import Flask, request, jsonify
from script.preprocessor import preprocess_log
from script.mitre_info_extractor import analyze_log
import json
import os

app = Flask(__name__)

# Percorsi delle cartelle
DATASET_DIR = "datasets"
LOGS_DIR = os.path.join(DATASET_DIR, "logs")
RESULTS_DIR = os.path.join(DATASET_DIR, "results")
PREPROCESSED_DIR = os.path.join(DATASET_DIR, "preprocessed")

# Assicurati che le cartelle results e preprocessed esistano
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(PREPROCESSED_DIR, exist_ok=True)

# Funzione per caricare i log
def carica_log():
    """Carica tutti i log dal dataset unificato."""
    dataset_path = os.path.join(DATASET_DIR, "dataset_unito.json")
    with open(dataset_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Funzione per processare e analizzare un log
def process_log(log):
    preprocessed_log = preprocess_log(log)  # Preprocessa il log
    result = analyze_log(preprocessed_log)  # Analizza il log
    return result

# Endpoint per ricevere la richiesta del log e restituire l'analisi
@app.route('/analizza_log', methods=['POST'])
def analizza_log():
    try:
        # Estrai il log dal corpo della richiesta
        data = request.get_json()
        log_id = data.get("log_id")  # E.g., id del log
        log = None
        
        # Carica il log dal dataset
        logs = carica_log()
        for scenario in logs:
            if scenario['id'] == log_id:
                log = scenario
                break

        if log is None:
            return jsonify({"error": "Log non trovato"}), 404

        # Analizza il log
        result = process_log(log)

        # Restituisci il risultato come risposta
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
