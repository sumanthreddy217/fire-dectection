
# this is live camera + telegram alert system + snapshot alert (threaded)


from ultralytics import YOLO
import cv2
import requests
import threading
import time

# --- Telegram Configuration ---
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

last_alert_time = 0
alert_cooldown = 10  # seconds


def send_telegram_alert(message, image_path=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

    if image_path:
        photo_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        with open(image_path, "rb") as photo:
            requests.post(photo_url, files={"photo": photo}, data={"chat_id": CHAT_ID})


# Load YOLOv8 model
model = YOLO("best.pt")

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    current_time = time.time()

    for result in results:
        boxes = result.boxes
        for box in boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            confidence = float(box.conf[0])

            if class_name.lower() in ["fire", "smoke"] and confidence > 0.6:
                if current_time - last_alert_time > alert_cooldown:

                    alert_message = f"🚨 ALERT: {class_name.upper()} detected!\nConfidence: {confidence:.2f}"
                    print(alert_message)

                    image_path = "snapshot.jpg"
                    cv2.imwrite(image_path, frame)

                    # 🔥 Threaded alert (NO FREEZE)
                    threading.Thread(
                        target=send_telegram_alert,
                        args=(alert_message, image_path),
                        daemon=True
                    ).start()

                    last_alert_time = current_time

                cv2.putText(frame,
                            "FIRE/SMOKE DETECTED!",
                            (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 255),
                            3)

    annotated_frame = results[0].plot()

    cv2.imshow("Fire & Smoke Monitoring System", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
