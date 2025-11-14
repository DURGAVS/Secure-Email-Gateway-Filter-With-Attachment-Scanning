import json
import os
from config import REPORT_FILE

def append_scan_summary(user_email, filename, is_clean, path_used):
    summary = {
        "user_email": user_email,
        "filename": filename,
        "is_clean": is_clean,
        "path_used": path_used
    }

    report_dir = os.path.dirname(REPORT_FILE)
    os.makedirs(report_dir, exist_ok=True)  # Ensure directory exists

    if not os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, 'w') as f:
            json.dump([summary], f, indent=4)
    else:
        with open(REPORT_FILE, 'r+') as f:
            data = json.load(f)
            data.append(summary)
            f.seek(0)
            json.dump(data, f, indent=4)
    print(f"✅ Report updated: {REPORT_FILE}")
