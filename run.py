import logging

from app import create_app

# Configurar el sistema de logging para que también guarde en un archivo
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("bot_errores.log", encoding="utf-8"),
        logging.StreamHandler() # Para que siga apareciendo en consola
    ]
)

app = create_app()

if __name__ == "__main__":
    logging.info("Flask app started")
    app.run(host="0.0.0.0", port=5050)
