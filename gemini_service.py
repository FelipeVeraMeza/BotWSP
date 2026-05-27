import os
import requests
import logging

def generate_gemini_response(message_body):
    api_key = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": message_body}]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        
        # Extraer el texto de la respuesta de Gemini
        data = response.json()
        reply_text = data['candidates'][0]['content']['parts'][0]['text']
        return reply_text
        
    except Exception as e:
        logging.error(f"Error con Gemini API: {str(e)}")
        return "Lo siento, tuve un problema al procesar tu mensaje."