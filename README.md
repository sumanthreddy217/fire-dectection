# README.md  
## Automated Fire & Smoke Monitoring System using YOLOv8 + Telegram Alerts

---

# 🔥 Project Overview

This project is a real-time fire and smoke detection system using:

- YOLOv8 Object Detection
- OpenCV Webcam Streaming
- Telegram Alert System
- Snapshot Capture
- Multithreading for Non-Freezing Alerts

The system continuously monitors live camera footage and detects:

- 🔥 Fire
- 🌫 Smoke

When fire or smoke is detected:

✅ Detection box appears on screen  
✅ Alert message sent to Telegram  
✅ Snapshot image sent to Telegram  
✅ Alerts work without freezing the live camera feed

---

# 📌 Features

- Real-time webcam monitoring
- YOLOv8 object detection
- Fire and smoke classification
- Telegram instant alert notification
- Snapshot image sending
- Threaded alert system (no lag/freezing)
- Confidence threshold filtering
- Alert cooldown system

---

# 🖥 Requirements

## Software Requirements

- Python 3.9 or above
- Webcam / USB Camera
- Internet Connection (for Telegram alerts)

---

# 📦 Create Virtual Environment (Recommended)

## Step 1 — Open Terminal

Go to your project folder.

---

## Step 2 — Create Virtual Environment

### Windows

```bash
python -m venv venv
```

### Linux / Mac

```bash
python3 -m venv venv
```

---

# ▶ Activate Virtual Environment

## Windows

```bash
venv\Scripts\activate
```

## Linux / Mac

```bash
source venv/bin/activate
```

After activation you will see:

```bash
(venv)
```

before terminal path.

---

# 📥 Install Required Libraries

Run these commands inside virtual environment:

```bash
pip install ultralytics
pip install opencv-python
pip install requests
```

OR install all together:

```bash
pip install ultralytics opencv-python requests
```

---

# 📁 Project Structure

```bash
project-folder/
│
├── venv
├── best.pt
├── detection.py
└── README.md
```

---

# 📄 File Explanation

| File | Description |
|---|---|
| `best.pt` | Trained YOLOv8 model |
| `fire_detection.py` | Main Python detection code |
| `README.md` | Project documentation |

---

# 🤖 Telegram Bot Setup

## Step 1 — Open Telegram

Install Telegram application.

---

## Step 2 — Create Bot

Search for:

```text
@BotFather
```

---

## Step 3 — Create New Bot

Send:

```text
/newbot
```

BotFather will ask:

- Bot Name
- Bot Username

After creation you will get:

```text
BOT TOKEN
```

Example:

```text
123456789:ABCxyz
```

---

## Step 4 — Get Chat ID

Search:

```text
@userinfobot
```

Send:

```text
/start
```

It will show your:

```text
CHAT ID
```

---

# ⚙ Configure Telegram in Code

Replace these values:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
```

---

# ▶ Run the Project

Use command:

```bash
python fire_detection.py
```

---

# 🎥 How System Works

## Step-by-Step Workflow

1. Webcam captures live video
2. YOLOv8 processes each frame
3. Model detects fire or smoke
4. Confidence score checked
5. Snapshot image captured
6. Telegram alert sent
7. Alert image sent
8. Live detection displayed on screen

---

# 🧠 Detection Logic

The system checks:

```python
if class_name.lower() in ["fire", "smoke"] and confidence > 0.6
```

Meaning:

- Only detect:
  - Fire
  - Smoke
- Confidence must be greater than:
  - 60%

---

# ⏱ Alert Cooldown System

```python
alert_cooldown = 10
```

Purpose:

- Prevent repeated alerts
- Reduces spam messages
- Sends alerts only once every 10 seconds

---

# ⚡ Multithreading

Telegram alerts are sent using:

```python
threading.Thread()
```

Purpose:

- Prevents webcam freezing
- Improves real-time performance
- Allows smooth detection while sending alerts

---

# 🖼 Snapshot Feature

When detection occurs:

```python
cv2.imwrite(image_path, frame)
```

The current frame is saved as:

```text
snapshot.jpg
```

and sent to Telegram.

---

# 🛑 Stop the Program

Press:

```text
Q
```

on keyboard to stop the system.

---

# 📊 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| YOLOv8 | Object Detection |
| OpenCV | Video Processing |
| Telegram Bot API | Alert System |
| Requests | Sending HTTP Requests |
| Threading | Background Alert Processing |

---

# 🚨 Example Telegram Alert

```text
🚨 ALERT: FIRE detected!
Confidence: 0.87
```

along with snapshot image.

---

# 🔧 Possible Future Enhancements

- Email alert system
- Buzzer/Siren integration
- Cloud storage for snapshots
- Mobile application integration
- Multiple camera support
- CCTV/IP camera support

---

# ❗ Troubleshooting

## Webcam Not Opening

Try changing:

```python
cap = cv2.VideoCapture(0)
```

to:

```python
cap = cv2.VideoCapture(1)
```

---

## Telegram Alerts Not Working

Check:

- Internet connection
- Correct BOT_TOKEN
- Correct CHAT_ID

---

## Model Not Loading

Ensure:

```text
best.pt
```

exists in same folder.

---

# 👨‍💻 Author

## Automated Fire & Smoke Monitoring System

Developed using YOLOv8, OpenCV, and Telegram API for real-time intelligent monitoring.