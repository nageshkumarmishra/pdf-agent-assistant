import json
import os
import csv

MEMORY_FILE = "memory.json"
CSV_FILE = "sessions.csv"

def save_session(pdf, task, output):
    """Append a new session entry to the memory file."""
    # Initialize file if it doesn't exist
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w") as f:
            f.write("[]")

    data = load_sessions()
    data.append({"pdf": pdf, "task": task, "output": output})

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_sessions():
    """Load session history safely, even if the file is empty or invalid."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []  # Empty file
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return []  # Corrupt file fallback
    return []

def export_sessions_to_csv():
    """Export all saved sessions to a CSV file."""
    sessions = load_sessions()
    if not sessions:
        return

    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["pdf", "task", "output"])
        writer.writeheader()
        writer.writerows(sessions)