#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

print(f"API Key: {API_KEY[:20]}..." if API_KEY else "ERROR: No API key")

try:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    # Test 1
    print("\n=== TEST 1: Me ayudas? ===")
    payload = {
        "contents": [{
            "parts": [{"text": "Me ayudas?"}]
        }]
    }
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    response.raise_for_status()
    print(f"Respuesta: {response.json()['candidates'][0]['content']['parts'][0]['text']}")
    
    # Test 2
    print("\n=== TEST 2: Como estas? ===")
    payload = {
        "contents": [{
            "parts": [{"text": "Como estas?"}]
        }]
    }
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    response.raise_for_status()
    print(f"Respuesta: {response.json()['candidates'][0]['content']['parts'][0]['text']}")
    
    # Test 3
    print("\n=== TEST 3: Cual es tu nombre? ===")
    payload = {
        "contents": [{
            "parts": [{"text": "Cual es tu nombre?"}]
        }]
    }
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    response.raise_for_status()
    print(f"Respuesta: {response.json()['candidates'][0]['content']['parts'][0]['text']}")
    
    print("\n[OK] Todas las pruebas pasaron!")
    
except Exception as e:
    print(f"[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()
