
import sqlite3
from config import config
from response import quarantine_file
from database import save_alert, save_incident
from entropy import calculate_entropy

def count_recent_events(window_seconds=60):
    connection = sqlite3.connect("./data/rdrs.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM events
        WHERE timestamp >= datetime('now', ?)
    """, (f"-{window_seconds} seconds",))

    count = cursor.fetchone()[0]
    connection.close()

    return count




def calculate_threat_score(event_count, entropy_value):
    score = 0

    # Score based on recent file activity
    if event_count >= 20:
        score += 70
    elif event_count >= 10:
        score += 40
    elif event_count >= 5:
        score += 10

    # Read the entropy threshold from config.yaml
    if entropy_value >= config["detection"]["entropy_threshold"]:
        score += 20

    # Keep the score within 0–100
    return min(score, 100)




def save_detection_alert(threat_score):
    connection = sqlite3.connect("./data/rdrs.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM events
        ORDER BY id DESC
        LIMIT 1
    """)

    result = cursor.fetchone()
    connection.close()

    event_id = result[0] if result else None

    # Save the alert
    save_alert(
        event_id,
        "HIGH_FILE_ACTIVITY",
        "High file activity detected in the last 60 seconds.",
        threat_score
    )

    # Find the ID of the alert we just saved
    connection = sqlite3.connect("./data/rdrs.db")
    cursor = connection.cursor()

    cursor.execute("SELECT MAX(id) FROM alerts")
    alert_id = cursor.fetchone()[0]

    connection.close()

    # Create an incident linked to that alert
    save_incident(
        alert_id,
        "OPEN",
        "Investigate the high file activity."
    )



def analyze_activity():
    event_count = count_recent_events(60)
    file_path = "./test_data/entropy_test.txt"
    entropy_value = calculate_entropy(file_path)
    threat_score = calculate_threat_score(event_count, entropy_value)
    

    print(f"Recent file events: {event_count}")
    print(f"Threat score: {threat_score}/100")
    print(f"Entropy of {file_path}: {entropy_value:.2f} bits per byte")

    if threat_score >= config["detection"]["threat_score_threshold"]:
        print("[WARNING] Suspicious activity requires investigation.")
        save_detection_alert(threat_score)
        print("Security alert saved to database.")

        if config["response"]["simulation_mode"]:
            print("[SIMULATION] Starting quarantine-copy response.")
            quarantine_file(file_path)
    else:
        print("[OK] Threat score is below the alert threshold.")



if __name__ == "__main__":
    analyze_activity()
