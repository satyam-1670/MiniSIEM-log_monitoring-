import re
from datetime import datetime, timedelta
from collections import defaultdict

LOG_FILE = "logs/auth.log"
TIME_WINDOW_MINUTES = 10
USER_THRESHOLD = 4

password_usage = defaultdict(list)

def parse_time(ts):
    return datetime.strptime(ts, "%Y-%m-%d %H:%M")

def monitor_logs():
    with open(LOG_FILE, "r") as f:
        logs = f.readlines()

    for line in logs:
        match = re.search(
            r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) (\w+) Failed login using (\S+) from ([\d.]+)",
            line
        )

        if not match:
            continue

        timestamp = parse_time(match.group(1))
        user = match.group(2)
        password = match.group(3)

        password_usage[password].append((timestamp, user))

        window_start = timestamp - timedelta(minutes=TIME_WINDOW_MINUTES)

        # keep only recent entries
        password_usage[password] = [
            (t, u) for (t, u) in password_usage[password]
            if t >= window_start
        ]

        unique_users = {u for (_, u) in password_usage[password]}

        if len(unique_users) >= USER_THRESHOLD:
            print("🚨 ALERT: Password Spraying Detected")
            print(f"Password: {password}")
            print(f"Users targeted: {unique_users}")
            password_usage[password].clear()

monitor_logs()
