import requests
import time
from datetime import datetime

# Тестовые данные для демонстрации
demo_scenario = [
    {"rfid": "RFID-1001", "turnstile_id": 1, "direction": "IN", "delay": 2},
    {"rfid": "RFID-1003", "turnstile_id": 1, "direction": "IN", "delay": 1},
    {"rfid": "RFID-1005", "turnstile_id": 2, "direction": "IN", "delay": 3},
    {"rfid": "RFID-1003", "turnstile_id": 1, "direction": "OUT", "delay": 2},
    {"rfid": "RFID-9999", "turnstile_id": 1, "direction": "IN", "delay": 1}  # Неизвестная карта
]


def run_demo():
    print("=== Демонстрация системы контроля доступа ===")
    for event in demo_scenario:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Карта: {event['rfid']}", end=" ")
        print(f"| Турникет: {event['turnstile_id']} | Направление: {event['direction']}")

        try:
            response = requests.post(
                "http://localhost:8000/api/access",
                json={
                    "rfid": event["rfid"],
                    "turnstile_id": event["turnstile_id"],
                    "direction": event["direction"]
                }
            )
            data = response.json()
            if data.get("access") == "GRANTED":
                print(f"Доступ разрешен: {data['employee']['full_name']} ({data['employee']['position']})")
            else:
                print(f"Ошибка: {data}")
        except Exception as e:
            print(f"⚠️ Ошибка запроса: {str(e)}")

        time.sleep(event["delay"])


if __name__ == "__main__":
    run_demo()