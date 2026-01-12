import re
from datetime import datetime,timedelta
from collections import defaultdict

LOG_FILE=r"E:\defensive project 2026\logmonitor(mini siem)\logs\auth.log"
Thresold=3
TIME_WINDOW_MINUTES = 10

failed_logins = defaultdict(list)

def parse_time(ts):
    return datetime.strptime(ts, "%Y-%m-%d %H:%M")

def monitor_logs():
    with open(LOG_FILE, "r") as f:
        logs = f.readlines()

    for line in logs:
        match = re.search(
            r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}).*Failed password.*from ([\d.]+)",
            line
        )

        if match:
            timestamp = parse_time(match.group(1))
            ip = match.group(2)

            failed_logins[ip].append(timestamp)

            # sliding window
            window_start = timestamp - timedelta(minutes=TIME_WINDOW_MINUTES)
            failed_logins[ip] = [
                t for t in failed_logins[ip] if t >= window_start
            ]

            if len(failed_logins[ip]) >= Thresold:
                print(f"🚨 ALERT: Slow brute-force detected from {ip}")
                failed_logins[ip].clear()

monitor_logs()


