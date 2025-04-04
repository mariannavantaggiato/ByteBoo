## BiteBoo👻
## 🧠 Cybersecurity Chatbot WebApp

Questo progetto è una webapp basata su Flask che integra un modello LLM open-source ottimizzato via prompt engineering per assistere nella **cybersecurity**.  
È progettato per analizzare log e fornire risposte contestuali e coerenti, valutate automaticamente secondo le linee guida di **Symbiotic AI**.

---

## 🚀 Caratteristiche principali

- ✅ Webapp in Flask con interfaccia intuitiva
- 🤖 Integrazione di un LLM (`LLaMAntino-3-ANITA-8B-Inst-DPO-ITA`)
- 🧩 Prompt engineering ottimizzato per contesto cybersecurity
- 📊 Script di valutazione delle risposte secondo **Symbiotic AI Guidelines**
- ⚡ Utilizzo di quantizzazione 8-bit con **BitsAndBytes** per efficienza

---

## 🗂️ Struttura del progetto
webapp/  <br/>
├── app.py <br/>
├── chatbot_model.py #Logica di caricamento modello e gestione conversazione  <br/>
├── evaluator.py #Valutazione delle risposte (Symbiotic AI) <br/>
├── templates/ <br/>
│ └── index.html #Interfaccia HTML <br/>
├── static/ <br/>
│ ├── style.css #Stili personalizzati <br/>
│ └── chatbot.js #Logica client JS <br/>
├── datasets/ <br/>
│ └── prompt.txt #Prompt iniziale per il modello <br/>
└── README.md #Questo file<br/>


---

## 🪢Clonare la repository

```bash
git clone https://github.com/mariannavantaggiato/ByteBoo.git
cd ByteBoo
```
> Assicurati di avere [Git](https://git-scm.com/) installato.

---

## 🛠️ Requisiti

Assicurati di avere Python 3.10+ e un ambiente virtuale attivo:

```bash
pip install -r requirements.txt
```

Librerie principali:

- `transformers`
- `accelerate`
- `bitsandbytes`
- `flask`
- `torch con CUDA`
- `scikit-learn` (per valutazione)

## ▶️ Avvio della WebApp
Avvia il server Flask da terminale:
```bash
python3 app.py
```

La webapp sarà disponibile su http://127.0.0.1:36000 <br/>
*Se hai necessità di cambiare la porta, basta cambiare il valore nella riga n in `app.py`*

---

## ✅ Valutazione delle Risposte
Le risposte generate dal chatbot vengono automaticamente valutate dallo script evaluator.py, seguendo le linee guida Symbiotic AI:

- Coerenza logica (logical consistency)
- Rilevanza per la cybersecurity
- Sicurezza e responsabilità
- Stile e chiarezza
- Supporto alle decisioni umane

---

Esempio di utilizzo:

```python
from evaluator import evaluate_response

user_input = "Mostra le tecniche MITRE usate in un attacco X"
model_response = "Le tecniche T1566 e T1059 sono comuni..."
score, report = evaluate_response(user_input, model_response)

print("Score totale:", score)
print("Dettagli:", report)

```

## 📚 Fonti e Linee Guida

Questo progetto si basa su un approccio di prompt engineering e segue le linee guida per la progettazione e valutazione di AI collaborative, con un focus sulla sicurezza informatica. Di seguito le fonti principali:

- **[Techniques and Methods to Evaluate Human-Centered Symbiotic AI Systems](https://dl.acm.org/doi/full/10.1145/3708557.3716153)**  
  *Miriana Calvano.*  

- **[Building Symbiotic AI: Reviewing the AI Act for a Human-Centred, Principle-Based Framework](https://arxiv.org/abs/2501.08046)**  
  *Miriana Calvano,  Antonio Curci, Giuseppe Desolda, Andrea Esposito, Rosa Lanzilotti, Antonio Piccinno*  

- **[Design and Evaluation of High-Quality Symbiotic AI Systems through a Human-Centered Approach](https://dl.acm.org/doi/abs/10.1145/3661167.3661223)**  
  *Miriana Calvano*  

- **[LLaMAntino-3 ANITA-8B (HuggingFace)](https://huggingface.co/swap-uniba/LLaMAntino-3-ANITA-8B-Inst-DPO-ITA)**  
  Modello linguistico open-source ottimizzato per il linguaggio italiano e il dialogo istruito, usato tramite prompt engineering per fornire supporto in ambito cybersecurity.

- **[MITRE ATT&CK Framework](https://attack.mitre.org/)**  
  Fonte strutturata di conoscenza sulle tattiche e tecniche utilizzate da attori malevoli in scenari reali, usata come base per costruire prompt e valutare la pertinenza delle risposte.


## 📌 Note finali
🔒 Tutte le risposte sono generate in modo responsabile, evitando contenuti dannosi o fuorvianti. <br/>
📈 Questo progetto è parte di una tesi triennale in Informatica con focus su AI e Cybersecurity.

## 👩‍💻 Autore
Marianna Vantaggiato <br/>
Corso di Laurea in Informatica e Tecnologie per la Produzione del Software <br/>
Università degli Studi di Bari — 2025

