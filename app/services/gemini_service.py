import requests
import logging
from flask import current_app

def generate_gemini_response(message_body):
    # Ahora leemos la clave directamente desde la configuración de tu App
    api_key = current_app.config.get("GEMINI_API_KEY")
    
    if not api_key:
        logging.error("GEMINI_API_KEY no configurada.")
        return "Error interno de configuración."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": message_body}]
        }]
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=12)
        response.raise_for_status()
        
        data = response.json()
        
        if "candidates" in data and len(data["candidates"]) > 0:
            parts = data["candidates"][0]["content"]["parts"]
            if len(parts) > 0:
                return parts[0]["text"]
                
        return "Lo siento, no pude procesar una respuesta válida."
        
    except Exception as e:
        logging.error(f"Excepción en Gemini API: {str(e)}")
        return "Tuve un inconveniente al conectar con mi cerebro de IA. Por favor, intenta de nuevo."