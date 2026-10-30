
import sqlite3

connection = sqlite3.connect("./data/rdrs.db")
cursor = connection.cursor()

print("\n--- Latest Alerts ---")
cursor.execute("""
    SELECT id, alert_type, description, threat_score, timestamp
    FROM alerts
    ORDER BY id DESC
    LIMIT 5
""")

for row in cursor.fetchall():
    print(row)

print("\n--- Latest Incidents ---")
cursor.execute("""
    SELECT id, alert_id, status, description, timestamp
    FROM incidents
    ORDER BY id DESC
    LIMIT 5
""")

for row in cursor.fetchall():
    print(row)

connection.close()
