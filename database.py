
import sqlite3
import os

os.makedirs("data", exist_ok=True)


def create_database():
    connection = sqlite3.connect("./data/rdrs.db")
    cursor = connection.cursor()

    # 1. Store file-system events
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            file_path TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Store process metadata
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid INTEGER,
            process_name TEXT,
            username TEXT,
            memory_mb REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 3. Store security alerts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            alert_type TEXT NOT NULL,
            description TEXT,
            threat_score INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
    """)

    # 4. Store security incidents
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_id INTEGER,
            status TEXT DEFAULT 'OPEN',
            description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (alert_id) REFERENCES alerts(id)
        )
    """)

    connection.commit()
    connection.close()

    print("RDRS database is ready!")
    print("Tables: events, processes, alerts, incidents")

def save_event(event_type, file_path):
    connection = sqlite3.connect("./data/rdrs.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO events (event_type, file_path)
        VALUES (?, ?)
    """, (event_type, file_path))

    connection.commit()
    connection.close()

    print("Event saved successfully!")

def save_process(pid, process_name, username, memory_mb):
    connection = sqlite3.connect("./data/rdrs.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO processes
        (pid, process_name, username, memory_mb)
        VALUES (?, ?, ?, ?)
    """, (pid, process_name, username, memory_mb))

    connection.commit()
    connection.close()

    print(f"Process {process_name} saved to database.")


def show_processes():
    connection = sqlite3.connect("./data/rdrs.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT pid, process_name, username, memory_mb, timestamp
        FROM processes
        ORDER BY id DESC
        LIMIT 10
    """)

    records = cursor.fetchall()

    print("\nLatest 10 saved processes:")

    for record in records:
        print(record)

    connection.close()

def save_alert(event_id, alert_type, description, threat_score):
    connection = sqlite3.connect("./data/rdrs.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO alerts
        (event_id, alert_type, description, threat_score)
        VALUES (?, ?, ?, ?)
    """, (event_id, alert_type, description, threat_score))

    connection.commit()
    connection.close()

    print("Security alert saved successfully!")


def save_incident(alert_id, status, description):
    connection = sqlite3.connect("./data/rdrs.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO incidents
        (alert_id, status, description)
        VALUES (?, ?, ?)
    """, (alert_id, status, description))

    connection.commit()
    connection.close()

    print("Security incident saved successfully!")


if __name__ == "__main__":
    create_database()
    print("Database initialized. Existing records preserved.")
