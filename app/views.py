import logging
from flask import Blueprint, request, jsonify, current_app
from app.utils.whatsapp_utils import process_whatsapp_message, is_valid_whatsapp_message
import json
import datetime
import os

webhook_blueprint = Blueprint("webhook", __name__)

@webhook_blueprint.route("/webhook", methods=["GET"])
def webhook_verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == current_app.config["VERIFY_TOKEN"]:
            logging.info("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            logging.error("VERIFICATION_FAILED")
            return jsonify({"status": "error", "message": "Verification failed"}), 403
            
    return jsonify({"status": "error", "message": "Missing parameters"}), 400

@webhook_blueprint.route("/webhook", methods=["POST"])
def webhook_handle():
    body = request.get_json()
    
    # === GUARDAR EL JSON EN UN ARCHIVO DE TEXTO ===
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Abre (o crea) un archivo llamado debug_mensajes.txt en modo "añadir" (append)
        with open("debug_mensajes.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f"\n\n=== EVENTO META: {timestamp} ===\n")
            archivo.write(json.dumps(body, indent=2))
            archivo.write("\n========================================\n")
    except Exception as e:
        pass # Ignorar errores de escritura para no interrumpir el bot
    # ==============================================

    if is_valid_whatsapp_message(body):
        try:
            process_whatsapp_message(body)
            return jsonify({"status": "success"}), 200
        except Exception as e:
            logging.error(f"Error al procesar el mensaje: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500
            
    return jsonify({"status": "ignored"}), 200