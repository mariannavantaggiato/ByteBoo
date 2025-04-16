import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PROMPT_PATH = "../datasets/prompt.txt"

def log_gpu_memory():
    if torch.cuda.is_available():
        total_memory = torch.cuda.get_device_properties(0).total_memory
        allocated_memory = torch.cuda.memory_allocated(0)
        free_memory = total_memory - allocated_memory
        logger.info(f"Memoria totale: {total_memory / 1e9:.2f} GB")
        logger.info(f"Memoria allocata: {allocated_memory / 1e9:.2f} GB")
        logger.info(f"Memoria libera: {free_memory / 1e9:.2f} GB")
    else:
        logger.info("CUDA non disponibile.")

def load_prompt():
    if os.path.exists(PROMPT_PATH):
        with open(PROMPT_PATH, "r", encoding="utf-8") as file:
            return file.read().strip()
    else:
        logger.warning(f"⚠️ File prompt.txt non trovato in {PROMPT_PATH}. Verrà usato un prompt di default.")
        return "Sei un assistente AI esperto di cybersecurity."

def load_pipeline():
    try:
        quantization_config = BitsAndBytesConfig(
            load_in_8bit=True,
            llm_int8_threshold=6.0
        )
        
        # Carica prima il modello con la quantizzazione
        model = AutoModelForCausalLM.from_pretrained(
            "swap-uniba/LLaMAntino-3-ANITA-8B-Inst-DPO-ITA",
            device_map="auto",
            torch_dtype=torch.float16,
            quantization_config=quantization_config
        )
        
        tokenizer = AutoTokenizer.from_pretrained("swap-uniba/LLaMAntino-3-ANITA-8B-Inst-DPO-ITA")

        # Passa il modello già caricato alla pipeline
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer
        )
        
        logger.info("✅ Pipeline caricata con successo")
        log_gpu_memory()
        return pipe
    except Exception as e:
        logger.error(f"❌ Errore durante il caricamento della pipeline: {str(e)}")
        raise e

class ChatBot:
    def __init__(self):
        self._pipeline = None
        self.system_prompt = load_prompt()
        self.conversation_history = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

    def _ensure_pipeline_loaded(self):
        if self._pipeline is None:
            self._pipeline = load_pipeline()

    def process_input(self, user_input):
        self._ensure_pipeline_loaded()
        self.conversation_history.append({"role": "user", "content": user_input})
        
        output = self._pipeline(self.conversation_history, max_new_tokens=300, do_sample=True, temperature=0.7, top_p=0.9)
        new_response = output[0]['generated_text'][-1]['content']

        self.conversation_history = output[0]['generated_text']

        return new_response, self.conversation_history
