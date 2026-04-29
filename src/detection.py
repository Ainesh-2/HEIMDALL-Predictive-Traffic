from ultralytics import YOLO
import cv2

model = YOLO("models/vehicle_detection.pt")


def detect_vehicles(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        annotated_frame = results[0].plot()
        vehicle_count = len(results[0].boxes)
        cv2.putText(
            annotated_frame,
            f"Vehicles: {vehicle_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )
        resized_frame = cv2.resize(annotated_frame, (960, 540))
        cv2.imshow("Vehicle Detection", resized_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    video_path = "videos/test_twin.mp4"
    detect_vehicles(video_path)
