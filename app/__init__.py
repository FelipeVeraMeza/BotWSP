import os
import logging
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Cargar las configuraciones desde las variables de entorno
    app.config["ACCESS_TOKEN"] = os.getenv("ACCESS_TOKEN")
    app.config["VERSION"] = os.getenv("VERSION", "v21.0")
    app.config["PHONE_NUMBER_ID"] = os.getenv("PHONE_NUMBER_ID")
    app.config["VERIFY_TOKEN"] = os.getenv("VERIFY_TOKEN")
    app.config["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

    # Configuración de logging por defecto
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )

    # Importar y registrar el blueprint del Webhook
    from .views import webhook_blueprint
    app.register_blueprint(webhook_blueprint)

    return app