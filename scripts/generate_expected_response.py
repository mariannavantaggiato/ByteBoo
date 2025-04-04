import json
import pandas as pd

# Carica il dataset di log (assumiamo che sia in formato JSON)
def load_logs(file_path="../datasets/dataset_unito.json"):
    with open(file_path, "r") as file:
        return json.load(file)

# Crea il dataset di valutazione
def create_evaluation_dataset(logs):
    evaluation_data = []
    
    for log in logs:
        # Estrai i dati pertinenti dal log
        log_id = log["log_id"]
        kill_chain_phase = log["kill_chain_phase"]
        mitre_technique = log["mitre_technique"]
        source_ip = log["source_ip"]
        destination_ip = log["destination_ip"]
        action = log["action"]
        name = log["name"]
        description = log["description"]
        
        # Crea la domanda con la parte di analisi dei passi successivi e mitigazione
        question = f"""
        Analizza il log con ID {log_id}.
        Fase della Kill Chain: {kill_chain_phase}.
        Tecnica MITRE: {mitre_technique}.
        IP sorgente: {source_ip}.
        IP destinazione: {destination_ip}.
        Azione: {action}.
        Nome: {name}.
        Descrizione della tecnica: {description[:200]}...
        Quali sono i prossimi passi da fare per proseguire l'attacco e come mitigarli?
        """
        
        # La risposta attesa è la 'description'
        evaluation_data.append({
            "log_id": log_id,
            "question": question,
            "expected_response": description
        })

    # Converte il dataset in un DataFrame di Pandas
    df = pd.DataFrame(evaluation_data)
    return df

# Salva il dataset di valutazione in un file JSON
def save_evaluation_dataset(df, output_path="../datasets/evaluation_dataset.json"):
    # Convertiamo il DataFrame in formato JSON e lo salviamo
    df.to_json(output_path, orient="records", lines=True, force_ascii=False)

# Carica i log
logs = load_logs()

# Crea il dataset di valutazione
evaluation_df = create_evaluation_dataset(logs)

# Salva il dataset di valutazione su file
save_evaluation_dataset(evaluation_df)

# Stampa alcune righe per verifica
print(evaluation_df.head())
