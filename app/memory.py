import json
import os
import csv

MEMORY_FILE = "memory.json"
CSV_FILE = "sessions.csv"

def save_session(pdf, task, output):
    data = load_sessions()
    data.append({"pdf": pdf, "task": task, "output": output})
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_sessions():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def export_sessions_to_csv():
    sessions = load_sessions()
    if not sessions:
        return
    with open(CSV_FILE, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["pdf", "task", "output"])
        writer.writeheader()
        writer.writerows(sessions)