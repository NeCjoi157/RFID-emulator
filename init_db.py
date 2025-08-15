import sqlite3
from datetime import datetime


def init_database():
    conn = sqlite3.connect("access.db")
    cursor = conn.cursor()

    # Создание таблиц
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        rfid TEXT UNIQUE,
        full_name TEXT NOT NULL,
        position TEXT NOT NULL,
        department TEXT,
        phone TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS turnstiles (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        location TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS access_logs (
        id INTEGER PRIMARY KEY,
        employee_id INTEGER,
        turnstile_id INTEGER,
        timestamp INTEGER,
        direction TEXT CHECK(direction IN ('IN', 'OUT')),
        access_granted BOOLEAN,
        FOREIGN KEY (employee_id) REFERENCES employees (id),
        FOREIGN KEY (turnstile_id) REFERENCES turnstiles (id)
    )""")

    # Добавляем 10 тестовых сотрудников
    employees = [
        ("RFID-1001", "Иванов Иван Иванович", "Директор", "Администрация", "+79161000101"),
        ("RFID-1002", "Петрова Анна Сергеевна", "Бухгалтер", "Финансы", "+79161000202"),
        ("RFID-1003", "Сидоров Алексей Петрович", "Инженер", "IT", "+79161000303"),
        ("RFID-1004", "Смирнова Елена Владимировна", "Менеджер", "Продажи", "+79161000404"),
        ("RFID-1005", "Кузнецов Дмитрий Анатольевич", "Охранник", "Безопасность", "+79161000505"),
        ("RFID-1006", "Васильева Ольга Игоревна", "Аналитик", "Маркетинг", "+79161000606"),
        ("RFID-1007", "Николаев Артем Викторович", "Разработчик", "IT", "+79161000707"),
        ("RFID-1008", "Павлова Виктория Дмитриевна", "Дизайнер", "Маркетинг", "+79161000808"),
        ("RFID-1009", "Федоров Михаил Олегович", "Логист", "Склад", "+79161000909"),
        ("RFID-1010", "Григорьева Анастасия Андреевна", "HR", "Персонал", "+79161001010")
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO employees 
    (rfid, full_name, position, department, phone) 
    VALUES (?, ?, ?, ?, ?)""", employees)

    # Турникеты
    cursor.executemany("""
    INSERT OR IGNORE INTO turnstiles 
    (id, name, location) 
    VALUES (?, ?, ?)""", [
        (1, "Главный вход", "Центральный холл"),
        (2, "Складской вход", "Корпус B, 1 этаж"),
        (3, "Парковка", "Подземный уровень")
    ])

    conn.commit()
    conn.close()
    print("База данных создана с 10 сотрудниками")


if __name__ == "__main__":
    init_database()