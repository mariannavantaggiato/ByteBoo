import { marked } from 'https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js';

const logExamples = {
    'failed-login': {
        name: "Tentativo di Login Fallito",
        log: `{
  "timestamp": "2025-03-28T14:32:45Z",
  "event_type": "Failed Login",
  "source_ip": "185.143.223.67",
  "username": "admin",
  "attempts": 5,
  "application": "VPN Gateway"
}`
    },
    'brute-force': {
        name: "Attacco Brute Force",
        log: `{
  "timestamp": "2025-03-28T11:42:33Z",
  "event_type": "Multiple Failed Logins",
  "source_ip": "10.0.3.12",
  "username": "admin",
  "attempts": 15,
  "time_window": "2 minutes",
  "user_agent": "Hydra"
}`
    },
    'cleared-logs': {
        name: "Log Cancellati",
        log: `{
  "timestamp": "2025-03-28T03:12:56Z",
  "event": "Log Cleared",
  "target": {
    "log_type": "Security",
    "records_deleted": 1428
  },
  "source": {
    "process": "wevtutil.exe",
    "user": "admin_audit"
  }
}`
    }
};

let conversationHistory = ""; // Mantiene internamente la cronologia (non visualizzata)

async function sendMessage() {
    const userInputElem = document.getElementById('user-input');
    const userMessage = userInputElem.value.trim();
    if (!userMessage) return;

    const messagesDiv = document.getElementById('messages');
    const typingIndicator = document.querySelector('.typing-indicator');

    // Aggiungi solo il nuovo messaggio utente alla chat
    addMessageToChat(messagesDiv, userMessage, 'user');
    userInputElem.value = '';
    typingIndicator.style.display = 'flex';

    try {
        // Invia il nuovo messaggio e la cronologia al backend
        const response = await fetch('/get_response', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: userMessage, history: conversationHistory })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        typingIndicator.style.display = 'none';

        // Aggiorna la cronologia con quella restituita dal backend
        conversationHistory = data.history;
        processBotResponse(messagesDiv, data);

    } catch (error) {
        console.error('Errore durante l\'invio:', error);
        typingIndicator.style.display = 'none';
        showErrorMessage(messagesDiv, error.message);
    }
}

function addMessageToChat(container, content, sender) {
    const messageEl = document.createElement('div');
    messageEl.classList.add('message', `${sender}-message`);

    const icon = document.createElement('img');
    icon.src = `/static/${sender}-icon.png`;
    icon.classList.add('message-icon');
    icon.alt = `${sender === 'user' ? 'Utente' : 'Bot'} Icon`;
    messageEl.appendChild(icon);

    const contentEl = document.createElement('div');
    contentEl.classList.add('message-content');
    if (sender === 'bot' && typeof content === 'object') {
        contentEl.innerHTML = marked.parse(content.formatted || content.answer);
    } else {
        const textEl = document.createElement('span');
        textEl.textContent = content;
        contentEl.appendChild(textEl);
    }
    messageEl.appendChild(contentEl);
    container.appendChild(messageEl);
    container.scrollTop = container.scrollHeight;
}

function processBotResponse(container, data) {
    if (data.error) {
        showErrorMessage(container, data.error);
        return;
    }
    let htmlContent = marked.parse(data.answer || data.formatted || 'Nessuna risposta dal server');
    // Personalizza il rendering (puoi modificare come preferisci)
    htmlContent = htmlContent
        .replace(/<h1>/g, '<h1 class="mitre-header">')
        .replace(/<h2>/g, '<h2 class="section-header">')
        .replace(/<ul>/g, '<ul class="analysis-list">')
        .replace(/<code>/g, '<code class="code-block">');
    addMessageToChat(container, { formatted: htmlContent }, 'bot');
}

function showErrorMessage(container, errorMsg) {
    const errorMessage = `⚠️ Errore nell'analisi: ${errorMsg || 'Riprova più tardi'}`;
    addMessageToChat(container, errorMessage, 'bot');
}

document.addEventListener('DOMContentLoaded', () => {
    const userInputElem = document.getElementById('user-input');
    const sendButton = document.querySelector('.send-btn');
    
    sendButton.addEventListener('click', sendMessage);
    userInputElem.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    userInputElem.focus();
});
