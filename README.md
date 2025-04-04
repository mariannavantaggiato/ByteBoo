#Progetto: AI per lo sviluppo di progetti cyber

##Descrizione
Questo progetto analizza la capacità di un LLM/LMM di supportare attività di difesa e risposta nel contesto della Cyber Kill Chain. Il modello suggerisce tecniche MITRE ATT&CK per ogni fase e log di attacco, e i risultati vengono valutati per misurarne accuratezza e affidabilità.

## Struttura

-**dataset/**: Log simulati e mappature MITRE.
-**scripts/**: Script di analisi, interazione con LLM e valutazione.
-**reports/**: Output di ciascuna simulazione.

## Requisiti
-Python 3.10+
-Transformers, llama-cpp-python o altro framework LLM
-Dataset JSONL precompilato
-Modello opensource (es. LLaMa, Mistral , GPTQ)

## Esecuzione
1. Esegui 'analyze_logs.py' per processare i log e salvare i report.
2. Esegui 'eveluate_results.py' per calcolare precisione, recall e F1-score.
