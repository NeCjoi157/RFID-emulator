import requests
import random
import time

SERVER_URL = "http://localhost:8000/api/access"


def generate_rfid():
    return f"RFID-{random.randint(1000, 1010)}"  # Только рабочие карты


def generate_direction():
    return random.choice(["IN", "OUT"])


def generate_turnstile():
    return random.randint(1, 3)  # Турникеты 1, 2, 3


while True:
    rfid = generate_rfid()
    turnstile_id = generate_turnstile()
    direction = generate_direction()

    try:
        response = requests.post(
            SERVER_URL,
            json={
                "rfid": rfid,
                "turnstile_id": turnstile_id,
                "direction": direction
            }
        )
        print(
            f"✓ Отправлено: {rfid} | Турникет: {turnstile_id} | Направление: {direction} | Статус: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data.get("access") == "GRANTED":
                print(f"   Доступ разрешен: {data['employee']['full_name']}")
            else:
                print(f"   Доступ запрещен")
        else:
            print(f"   Ошибка: {response.text}")

    except Exception as e:
        print(f"✗ Ошибка подключения: {e}")

    time.sleep(3)  # Пауза 3 секунды между запросами
