from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

print(f"API Key loaded: {API_KEY[:20]}..." if API_KEY else "ERROR: API Key NO cargada")

try:
    client = OpenAI(api_key=API_KEY)
    
    print("[OK] Cliente OpenAI creado")
    
    # Prueba con Chat Completions
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente amable"},
            {"role": "user", "content": "Hola, como estas?"}
        ],
        temperature=0.7,
        max_tokens=100
    )
    
    resultado = response.choices[0].message.content
    print(f"[OK] Respuesta recibida:")
    print(f"     {resultado}")
    
except Exception as e:
    print(f"[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()
