Установка
bash
git clone https://github.com/NeCjoi157/RFID-emulator.git
cd RFID-emulator
pip install -r requirements.txt
python init_db.py

Запуск системы
Сервер:

bash
python server.py
Эмулятор RFID:

bash
python rfid_emulator.py
Работа с FastAPI
После запуска сервера доступны:

Основные эндпоинты:

http://localhost:8000 - Главная страница

http://localhost:8000/api/access - API проверки доступа

Документация:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc
