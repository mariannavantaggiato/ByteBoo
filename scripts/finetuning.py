from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset, Dataset
import json

# Carica il modello e il tokenizer
model_id = "meta-llama/Llama-3.2-1B"
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Imposta il pad_token
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_id)

# Carica il dataset
def load_cyber_dataset(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

# Prepara il dataset per il fine-tuning
def prepare_dataset(data):
    texts = [f"{item['mode']}: {item['input']} {item['output']}" for item in data]
    dataset = Dataset.from_dict({"text": texts})
    return dataset

# Tokenizza il dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

# Carica e prepara il dataset
file_path = "../datasets/cyber_dataset.json"
data = load_cyber_dataset(file_path)
dataset = prepare_dataset(data)
tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Configura gli argomenti di training
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    weight_decay=0.01,
)

# Inizializza il Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset,
)

# Esegui il fine-tuning
trainer.train()

# Salva il modello fine-tuned
model.save_pretrained("./fine-tuned-llama")
tokenizer.save_pretrained("./fine-tuned-llama")