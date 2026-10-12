
import requests

TOKEN = '2090218043:TSCLT51nocEpDadH9RNt7iUa-lyq8ntn7HY'

def send_bale_message(chat_id, text):
    url = (f"https://tapi.bale.ai/" f"bot{TOKEN}/sendMessage")

    payload = {"chat_id": chat_id, "text": text}

    response = requests.post(url, json=payload, timeout=10)
    return response.json()
