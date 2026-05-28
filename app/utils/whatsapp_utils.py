import logging
from flask import current_app, jsonify
import json
import requests
import re
import datetime

def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")

def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )

def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        
        # SI META DEVUELVE ERROR, ESTO LO IMPRIMIRÁ EN TU CONSOLA
        if response.status_code != 200:
            logging.error(f"❌ ERROR DE META API: {response.status_code}")
            logging.error(f"❌ DETALLE DEL ERROR: {response.text}")
            
            # Guardar en archivo de alertas críticas
            with open("alertas_error.txt", "a", encoding="utf-8") as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] ❌ ERROR META {response.status_code}: {response.text}\n")
            
        response.raise_for_status()
    except Exception as e:
        logging.error(f"❌ Fallo crítico al enviar mensaje: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        log_http_response(response)
        return response
def process_text_for_whatsapp(text):
    # Eliminar metadatos o anotaciones raras que devuelven los modelos de IA del tipo 【...】
    pattern = r"\【.*?\】"
    text = re.sub(pattern, "", text).strip()

    # Convertir las negritas de Markdown estándar (**) al formato nativo de WhatsApp (*)
    pattern = r"\*\*(.*?)\*\*"
    replacement = r"*\1*"
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text

def process_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"]

    # INDICADOR 1: ¿Llega el mensaje?
    print(f"\n📩 [1/3] Mensaje recibido de {name} ({wa_id}): {message_body}")

    from app.services.gemini_service import generate_gemini_response

    ai_response = generate_gemini_response(message_body)
    
    # INDICADOR 2: ¿Gemini generó el texto?
    print(f"🧠 [2/3] Gemini respondió: {ai_response[:50]}...") # Imprime solo los primeros 50 caracteres

    final_response = process_text_for_whatsapp(ai_response)
    data = get_text_message_input(wa_id, final_response)
    
    # INDICADOR 3: ¿Se intentó enviar a Meta?
    print("🚀 [3/3] Enviando petición a Meta...")
    send_message(data)
def is_valid_whatsapp_message(body):
    """
    Valida minuciosamente si el JSON entrante de Meta contiene la estructura obligatoria de un mensaje.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )