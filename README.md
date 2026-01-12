# Mini-SIEM — Time-Based Correlation Engine (SOC Style)

## ⚠️ What This Is (And What It Is NOT)

This is **NOT** a toy brute-force counter.
This is **NOT** a beginner “if count > 5 then alert” script.

This project implements **time-based correlation using a sliding window** —
the exact logic real SOC teams use to detect **low-and-slow authentication attacks**
that intentionally evade naive detection rules.

---

## 🎯 Problem Statement (Real-World Failure)

Traditional SIEM logic fails because it:
- Uses simple counters
- Resets state after delays
- Relies on per-user or per-IP lockouts

Result:
> Slow attackers walk straight through detection.

This project fixes that.

---

## 🧠 Core Detection Concept — Sliding Time Window

Instead of asking:
> “How many failures happened?”

We ask:
> **“What happened in the last X minutes, regardless of pauses?”**

### Detection Rule 
- Same IP address
- ≥ 5 failed logins
- Within a rolling 10-minute window
- Even if attempts are spaced out

This defeats:
- Low-and-slow brute force
- Password spraying foundations
- Lockout-threshold bypassing

---

## 🧩 Why Timestamps, Not Counters

Counters lie.

Attackers wait.
Counters reset.
Defenders feel safe.

We store **timestamps** instead.


On every new event:
1. Append timestamp
2. Drop timestamps outside the window
3. Recalculate count
4. Decide — alert or not

This is **stateful correlation**, not log parsing.

---

---

## 📄 Log Format Requirements

Your logs **must contain timestamps**.
No timestamp = no correlation = useless detection.


---

## 🛠️ Detection Logic (High-Level)

For each failed login:
- Extract timestamp + source IP
- Store timestamp per IP
- Remove timestamps older than `TIME_WINDOW_MINUTES`
- If remaining count ≥ `THRESHOLD` → ALERT

Important:
> The window **slides**, it does not reset.

---

## 🚨 Alert Meaning (Don’t Misread This)

An alert means:
- An attacker deliberately slowed attempts
- Lockout policies were avoided
- Naive rules would miss this
- This is **pre-compromise behavior**

This is not noise.
This is early-stage intrusion.

---

## 🧪 How to Test Properly (If You Skip This, You’re Faking It)

### Valid Test
- Spread failures across 8–9 minutes
- Trigger on the 5th attempt
- Confirm alert fires only when threshold is crossed

### Invalid Test
- Spamming 5 lines at once
- Calling it “working”
- Moving on

That’s how bad analysts are born.

---

## 🧠 What You Should Understand After This

If you truly get this project, you understand:
- Time-based correlation
- Low-and-slow attack detection
- Stateful SIEM logic
- Why attackers win against naive rules
- How real SOC alerts are designed


---



