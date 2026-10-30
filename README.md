Ransomware Detection and Response System (RDRS)

 Project Overview

RDRS is a Python-based educational cybersecurity project designed to monitor file-system activity, collect process metadata, calculate basic threat scores, generate security alerts, and maintain incident records.

The project uses a rule-based detection approach to demonstrate key concepts used in security monitoring and incident response.

 Features:-

File Monitoring:Records file-system events using Watchdog.
Entropy Analysis:Calculates Shannon entropy to examine file data.
Process Monitoring: Collects process IDs, names, usernames, and memory usage using psutil.
Threat Scoring: Calculates a score from 0 to 100 using recent file activity and file entropy.
Database Storage: Stores events, processes, alerts, and incidents in SQLite.
Security Alerts: Saves alerts when the configured threat-score threshold is reached.
Incident Tracking: Creates incident records associated with alerts.
Simulation Response: Copies selected files into a quarantine folder while preserving the original.
REST API: Exposes event, process, alert, and incident data.
Web Dashboard: Displays summary counts, recent events, alerts, and incidents.
Report Exports: Provides JSON and CSV event reports.
Automated Testing: Uses pytest to test threat scoring, database operations, and response functionality.

Technologies Used

- Python
- SQLite
- Flask
- Watchdog
- psutil
- PyYAML
- pytest
- HTML, CSS, and JavaScript

Project Structure

text
RDRS/
├── analyzer.py
├── api.py
├── check_records.py
├── config.py
├── config.yaml
├── database.py
├── entropy.py
├── monitor.py
├── process_monitor.py
├── response.py
├── requirements.txt
├── README.md
├── .gitignore
├── test_analyzer.py
├── test_database.py
├── test_response.py
├── templates/
│   └── dashboard.html
├── test_data/
├── data/
└── quarantine/


Setup and Installation

 1. Clone the repository

bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Ransomware-Detection-and-Response-System


2. Create a virtual environment

bash
python -m venv .venv


3. Activate the virtual environment

Windows:

powershell
.venv\Scripts\Activate.ps1


4. Install dependencies

bash
python -m pip install -r requirements.txt


5. Initialize the database

bash
python database.py


Running the Project

Start file monitoring

bash
python monitor.py


 Run threat analysis

bash
python analyzer.py


Start the Flask API and dashboard

bash
python api.py


Open the dashboard in your browser:

http://127.0.0.1:5000/dashboard

API Endpoints

| Endpoint | Purpose |

/api/events | Retrieve file events |
/api/processes` | Retrieve saved process records |
/api/alerts | Retrieve security alerts |
/api/incidents | Retrieve incident records |
/api/reports/events/json | Retrieve event reports in JSON |
/api/reports/events/csv | Retrieve event reports in CSV |

 Running the Tests

Run the automated tests using:

```bash
python -m pytest -v
```

The project test suite contains eight automated tests covering:

- Threat-score calculations.
- Database event and process operations.
- Response functionality, including evidence copying and missing-file handling.

Latest verified result: 8 tests passed.

Configuration

The config.yaml file controls:

- Monitored directory paths.
- Entropy threshold.
- Threat-score threshold.
- Simulation response mode.
- SQLite database location.

 Limitations

- Detection uses simple rules and is not a production-grade ransomware detection engine.
- High threat scores indicate suspicious activity according to configured rules; they do not prove that ransomware is present.
- Process monitoring currently performs a scan when the script is run; continuous background process monitoring has not been implemented.
- The quarantine feature creates an evidence copy. It does not isolate processes or remove the original file.
- Automated tests cover selected functionality and do not guarantee complete system security.
- Docker deployment has not been configured.

Future Improvements

- Add automated integration tests for alerts, incidents, and response behavior.
- Improve detection rules and reduce duplicate alerts.
- Add continuous process monitoring and more detailed logging.
- Improve incident management and reporting.
- Add deployment support after testing the complete application.

