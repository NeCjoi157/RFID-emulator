import requests
import random
import time

SERVER_URL = "http://localhost:8000/api/access"

def generate_rfid():
    return f"RFID-{random.randint(1000, 9999)}"

while True:
    rfid = generate_rfid()
    response = requests.post(SERVER_URL, json={"rfid": rfid, "timestamp": int(time.time())})
    print(f"Sent: {rfid}, Status: {response.status_code}")
    time.sleep(5)

