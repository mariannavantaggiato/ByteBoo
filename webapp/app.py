from flask import Flask, request, jsonify, render_template
import re
from datetime import datetime
from chatbot_model import ChatBot
from threading import Lock
from chatbot_evaluator import ChatbotResponseEvaluator, save_evaluation_to_file

app = Flask(__name__, static_folder='static', template_folder='templates')

chatbot = ChatBot()
model_lock = Lock()
evaluator = ChatbotResponseEvaluator()

def clean_output(text):
    unwanted_patterns = [r"^Response:\s*", r"^Conversational Mode\s*", r"^Technical Mode\s*", r"^Technical Mode Activate\s*"]
    for pattern in unwanted_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.MULTILINE)
    return text.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    start_time = datetime.now()
    try:
        data = request.get_json()
        user_input = data.get("question", "").strip()

        if not user_input:
            return jsonify({"status": "error", "message": "Nessun input fornito"}), 400

        with model_lock:
            response_text, updated_history = chatbot.process_input(user_input)

        response_cleaned = clean_output(response_text)
        
        # Valutazione della risposta
        evaluation = evaluator.evaluate(user_input, response_text)
        # Salva la valutazione su file
        save_evaluation_to_file({
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "chatbot_response": response_text,
            "evaluation": evaluation["evaluation"]
        })
        
        elapsed = datetime.now() - start_time
        print(f"{datetime.now()} - Richiesta completata in {elapsed}")
        return jsonify({
            "status": "success",
            "answer": response_cleaned,
            "history": updated_history
        })
    except Exception as e:
        print(f"{datetime.now()} - Errore: {str(e)}")
        return jsonify({"status": "error", "message": f"Errore durante l'elaborazione: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=36001, debug=True)
