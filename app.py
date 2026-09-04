from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
import base64

app = Flask(__name__)

# Load YOLO model
model = YOLO("best.pt")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect():

    try:
        # Get image from browser
        data = request.get_json()

        if not data or "image" not in data:
            return jsonify({
                "success": False,
                "error": "No image received"
            })

        # Remove base64 header
        image_data = data["image"].split(",")[1]

        # Decode image
        image_bytes = base64.b64decode(image_data)

        # Convert to numpy array
        np_array = np.frombuffer(image_bytes, np.uint8)

        # Convert to OpenCV image
        frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({
                "success": False,
                "error": "Could not decode image"
            })

        # Run YOLO
        results = model(
            frame,
            conf=0.60,
            verbose=False
        )

        detections = []

        # Process detections
        for result in results:

            for box in result.boxes:

                confidence = float(box.conf[0])
                class_id = int(box.cls[0])

                class_name = model.names[class_id]

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                detections.append({
                    "type": class_name,
                    "confidence": round(
                        confidence * 100,
                        2
                    )
                })

                # Draw bounding box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                # Draw label
                label = (
                    f"{class_name} "
                    f"{confidence * 100:.1f}%"
                )

                cv2.putText(
                    frame,
                    label,
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

        # Encode annotated image
        _, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        annotated_image = base64.b64encode(
            buffer
        ).decode("utf-8")

        return jsonify({
            "success": True,
            "detections": detections,
            "image": (
                "data:image/jpeg;base64,"
                + annotated_image
            )
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "success": False,
            "error": str(e)
        })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )