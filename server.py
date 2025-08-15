from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import logging

app = FastAPI()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Вывод в консоль
        logging.FileHandler('access.log')  # Запись в файл
    ]
)


class AccessRequest(BaseModel):
    rfid: str
    turnstile_id: int
    direction: str  # "IN" или "OUT"


@app.get("/")
def read_root():
    """Корневой endpoint с информацией об API"""
    return {
        "message": "Enhanced RFID Access Control API",
        "endpoints": {
            "check_access": {
                "method": "POST",
                "path": "/api/access",
                "description": "Проверка доступа по RFID с указанием турникета"
            },
            "employees": {
                "method": "GET",
                "path": "/employees",
                "description": "Список сотрудников"
            },
            "logs": {
                "method": "GET",
                "path": "/logs",
                "description": "Журнал событий доступа"
            },
            "access_history": {
                "method": "GET",
                "path": "/access-history",
                "description": "История последних входов/выходов"
            },
            "documentation": [
                {"type": "Swagger UI", "path": "/docs"},
                {"type": "ReDoc", "path": "/redoc"}
            ]
        }
    }


@app.post("/api/access")
async def handle_access(request: AccessRequest):
    """Обработка запроса на проверку доступа с турникетом"""
    conn = sqlite3.connect("access.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # Проверяем сотрудника
        cursor.execute("SELECT * FROM employees WHERE rfid=?", (request.rfid,))
        employee = cursor.fetchone()

        # Проверяем турникет
        cursor.execute("SELECT * FROM turnstiles WHERE id=?", (request.turnstile_id,))
        turnstile = cursor.fetchone()

        if not turnstile:
            raise HTTPException(status_code=400, detail="Неизвестный турникет")

        timestamp = int(datetime.now().timestamp())
        human_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        if employee:
            # Логируем успешный доступ
            cursor.execute("""
                INSERT INTO access_logs 
                (employee_id, turnstile_id, timestamp, direction, access_granted) 
                VALUES (?, ?, ?, ?, ?)
            """, (employee['id'], turnstile['id'], timestamp, request.direction, True))

            conn.commit()

            # Вывод в консоль и файл
            log_message = (
                f"Доступ разрешен: {employee['full_name']} "
                f"(Карта: {request.rfid}) | "
                f"Турникет: {turnstile['name']} | "
                f"Направление: {request.direction}"
            )
            logging.info(log_message)

            return {
                "status": "success",
                "access": "GRANTED",
                "employee": dict(employee),
                "turnstile": dict(turnstile),
                "direction": request.direction,
                "timestamp": human_time
            }
        else:
            # Логируем попытку доступа
            cursor.execute("""
                INSERT INTO access_logs 
                (turnstile_id, timestamp, direction, access_granted) 
                VALUES (?, ?, ?, ?)
            """, (turnstile['id'], timestamp, request.direction, False))

            conn.commit()

            # Вывод в консоль и файл
            log_message = f"Доступ запрещен: неизвестная карта ({request.rfid})"
            logging.warning(log_message)

            raise HTTPException(
                status_code=403,
                detail={
                    "status": "DENIED",
                    "reason": log_message,
                    "turnstile": dict(turnstile)
                }
            )
    except sqlite3.Error as e:
        error_msg = f"Ошибка базы данных: {str(e)}"
        logging.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "message": error_msg}
        )
    finally:
        conn.close()


@app.get("/employees")
def get_employees():
    """Получить список всех сотрудников"""
    conn = sqlite3.connect("access.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"employees": employees}


@app.get("/logs")
def get_access_logs(limit: int = 100):
    """Получить расширенный журнал доступа"""
    conn = sqlite3.connect("access.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT l.id, l.timestamp, l.direction, l.access_granted,
               e.full_name, e.position, e.department,
               t.name as turnstile_name, t.location
        FROM access_logs l
        LEFT JOIN employees e ON l.employee_id = e.id
        LEFT JOIN turnstiles t ON l.turnstile_id = t.id
        ORDER BY l.timestamp DESC
        LIMIT ?
    """, (limit,))

    logs = []
    for row in cursor.fetchall():
        log = dict(row)
        log['timestamp'] = datetime.fromtimestamp(log['timestamp']).isoformat()
        logs.append(log)

    conn.close()
    return {"access_logs": logs}


@app.get("/access-history")
async def get_access_history(limit: int = 10):
    """Получить форматированную историю доступа"""
    conn = sqlite3.connect("access.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.full_name, t.name as turnstile, t.location, 
               datetime(l.timestamp, 'unixepoch') as time,
               l.direction, l.access_granted
        FROM access_logs l
        LEFT JOIN employees e ON l.employee_id = e.id
        LEFT JOIN turnstiles t ON l.turnstile_id = t.id
        ORDER BY l.timestamp DESC
        LIMIT ?
    """, (limit,))

    history = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {"history": history}