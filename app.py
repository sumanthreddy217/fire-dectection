from flask import Flask, render_template, Response, jsonify
from ultralytics import YOLO
import cv2
import numpy as np

app = Flask(__name__)

# Load your trained YOLO model
model = YOLO("best.pt")

# Store latest detection information
latest_detection = {
    "detected": False,
    "type": "None",
    "confidence": 0
}


def process_frame(frame):
    global latest_detection

    # Run YOLO detection
    results = model(frame, conf=0.60, verbose=False)

    detected = False
    detection_type = "None"
    confidence = 0

    # Draw detections
    for result in results:

        boxes = result.boxes

        for box in boxes:

            conf = float(box.conf[0])
            cls = int(box.cls[0])

            # Get class name
            class_name = model.names[cls]

            detected = True
            detection_type = class_name
            confidence = conf

            # Coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Draw bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Label
            label = f"{class_name} {conf * 100:.1f}%"

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    # Update latest detection
    latest_detection = {
        "detected": detected,
        "type": detection_type,
        "confidence": round(confidence * 100, 2)
    }

    return frame


def generate_frames():

    # Open webcam
    camera = cv2.VideoCapture(0)

    while True:

        success, frame = camera.read()

        if not success:
            break

        # Process frame with YOLO
        frame = process_frame(frame)

        # Convert frame to JPEG
        ret, buffer = cv2.imencode(".jpg", frame)

        frame_bytes = buffer.tobytes()

        # Send frame to browser
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes
            + b"\r\n"
        )

    camera.release()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/detection")
def detection():
    return jsonify(latest_detection)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
