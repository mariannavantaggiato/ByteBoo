import json
import os

# Percorso del dataset MITRE ATT&CK
MITRE_FILE = "../datasets/mitre/enterprise-attack.json"

# Funzione per caricare il dataset MITRE ATT&CK
def load_mitre_data():
    with open(MITRE_FILE, "r", encoding="utf-8") as mitre_file:
        return json.load(mitre_file)

# Carica i dati MITRE
mitre_data = load_mitre_data()

# Funzione per trovare dettagli su una tecnica MITRE
def get_mitre_info(technique_id):
    for obj in mitre_data["objects"]:
        if obj.get("type") == "attack-pattern":
            for ref in obj.get("external_references", []):
                if ref.get("external_id") == technique_id:
                    return {
                        "name": obj.get("name"),
                        "description": obj.get("description"),
                        "tactics": obj.get("kill_chain_phases", [])
                    }
    return None  # Se la tecnica non viene trovata

# Test della funzione
if __name__ == "__main__":
    test_technique = "T1595"  # Tecnica di Reconnaissance
    info = get_mitre_info(test_technique)
    print(f"Dettagli su {test_technique}:", info)



