import re
from datetime import datetime, timedelta
from collections import defaultdict

LOG_FILE = "logs/auth.log"
TIME_WINDOW_MINUTES = 10
USER_THRESHOLD = 5

events = defaultdict(list)

def parse_time(ts):
    return datetime.strptime(ts, "%Y-%m-%d %H:%M")

def monitor_logs():
    with open(LOG_FILE, "r") as f:
        logs = f.readlines()

    for line in logs:
        match = re.search(
            r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) (\w+) (\w+) Failed authentication from ([\d.]+)",
            line
        )

        if not match:
            continue

        timestamp = parse_time(match.group(1))
        user = match.group(2)
        service = match.group(3)

        key = (service, "Failed authentication")
        events[key].append((timestamp, user))

        window_start = timestamp - timedelta(minutes=TIME_WINDOW_MINUTES)

        events[key] = [
            (t, u) for (t, u) in events[key]
            if t >= window_start
        ]

        unique_users = {u for (_, u) in events[key]}

        if len(unique_users) >= USER_THRESHOLD:
            print("🚨 ALERT: Password Spraying Detected")
            print(f"Service: {service}")
            print(f"Users targeted: {unique_users}")
            events[key].clear()

monitor_logs()
