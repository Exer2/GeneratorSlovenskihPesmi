import os
import base64
import json
import requests
from google.cloud import speech
from google.oauth2 import service_account

def check_credentials():
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS ni nastavljena. "
                        "Prosim nastavite okoljsko spremenljivko z uporabo 'export'.")
    return credentials_path

def get_access_token():
    credentials_path = check_credentials()
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    
    # Pridobi JWT token
    credentials.refresh(requests.Request())
    return credentials.token

def transcribe_audio_google(audio_content):
    """Pošlje audio vsebino neposredno na Google Cloud Speech-to-Text API"""
    token = get_access_token()
    
    url = "https://speech.googleapis.com/v1/speech:recognize"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "config": {
            "encoding": "LINEAR16",
            "sampleRateHertz": 16000,
            "languageCode": "sl-SI"
        },
        "audio": {
            "content": base64.b64encode(audio_content).decode('utf-8')
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 200:
        raise Exception(f"Napaka pri klicu API-ja: {response.text}")
    
    result = response.json()
    
    if "results" in result and len(result["results"]) > 0:
        return result["results"][0]["alternatives"][0]["transcript"]
    return "Prepis ni bil uspešen."

def glasovni_vnos():
    # Tukaj bi morali implementirati zajemanje zvoka iz brskalnika
    # Za zdaj vrnemo testno sporočilo
    return "Funkcionalnost snemanja zvoka še ni implementirana."