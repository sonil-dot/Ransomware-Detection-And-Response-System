from flask import Flask, jsonify, render_template, send_file
import sqlite3
import csv
import io

from config import config

app = Flask(__name__)
@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")
@app.route("/api/reports/events/json", methods=["GET"])
def export_events_json():
    connection = get_db_connection()

    rows = connection.execute(
        "SELECT * FROM events ORDER BY id DESC"
    ).fetchall()

    connection.close()

    report = [dict(row) for row in rows]

    import json
    report_path = "./data/events_report.json"

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return send_file(
        report_path,
        as_attachment=True,
        download_name="events_report.json",
        mimetype="application/json"
    )

@app.route("/api/reports/events/csv", methods=["GET"])
def export_events_csv():
    connection = get_db_connection()

    rows = connection.execute(
        "SELECT * FROM events ORDER BY id DESC"
    ).fetchall()

    connection.close()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["id", "event_type", "file_path", "timestamp"])

    for row in rows:
        writer.writerow([
            row["id"],
            row["event_type"],
            row["file_path"],
            row["timestamp"]
        ])

    report_path = "./data/events_report.csv"

    with open(report_path, "w", newline="", encoding="utf-8-sig") as file:
        file.write(output.getvalue())

    return send_file(
        report_path,
        as_attachment=True,
        download_name="events_report.csv",
        mimetype="text/csv"
    )


def get_db_connection():
    """Open a connection to the RDRS database."""
    connection = sqlite3.connect(config["database"]["path"])
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "project": "Ransomware Detection and Response System",
        "status": "running",
        "endpoints": [
            "/api/events",
            "/api/processes",
            "/api/alerts",
            "/api/incidents"
        ]
    })


@app.route("/api/events", methods=["GET"])
def get_events():
    connection = get_db_connection()
    rows = connection.execute(
        "SELECT * FROM events ORDER BY id DESC LIMIT 100"
    ).fetchall()
    connection.close()

    return jsonify([dict(row) for row in rows])


@app.route("/api/processes", methods=["GET"])
def get_processes():
    connection = get_db_connection()
    rows = connection.execute(
        "SELECT * FROM processes ORDER BY rowid DESC LIMIT 100"
    ).fetchall()
    connection.close()

    return jsonify([dict(row) for row in rows])


@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    connection = get_db_connection()
    rows = connection.execute(
        "SELECT * FROM alerts ORDER BY id DESC LIMIT 100"
    ).fetchall()
    connection.close()

    return jsonify([dict(row) for row in rows])


@app.route("/api/incidents", methods=["GET"])
def get_incidents():
    connection = get_db_connection()
    rows = connection.execute(
        "SELECT * FROM incidents ORDER BY id DESC LIMIT 100"
    ).fetchall()
    connection.close()

    return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)

