from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import torch

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Nome del modello base su Hugging Face
base_model_path = "swap-uniba/LLaMAntino-2-7b-hf-dolly-ITA"

# Carica il modello base da Hugging Face
model = AutoModelForCausalLM.from_pretrained(base_model_path)

# Applica il fine-tuning (pesato su LoRA)
fine_tuned_model_path = "../scripts/modello_finetunato"
model = PeftModel.from_pretrained(model, fine_tuned_model_path)

# Carica anche il tokenizer
tokenizer = AutoTokenizer.from_pretrained(base_model_path)

model = model.merge_and_unload()
model.save_pretrained("../modello_finetunato_merged", safe_serialization=True)


print("Modello Caricato correttamente")

