from ultralytics import YOLO
import cv2

model = YOLO("models/vehicle_detection.pt")


def calculate_density(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        annotated_frame = results[0].plot()
        height, width = frame.shape[:2]
        north = south = east = west = 0
        for box in results[0].boxes.xyxy:
            x1, y1, x2, y2 = box
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            if cy < height/2:
                north += 1
            else:
                south += 1
            if cx < width/2:
                west += 1
            else:
                east += 1
            cv2.circle(annotated_frame, (cx, cy), 4, (0, 255, 0), -1)
        cv2.putText(annotated_frame, f"N: {north}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"S: {south}", (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"W: {west}", (20, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"E: {east}", (20, 130),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.line(annotated_frame, (0, height//2),
                 (width, height//2), (255, 0, 0), 2)
        cv2.line(annotated_frame, (width//2, 0),
                 (width//2, height), (255, 0, 0), 2)
        resized_frame = cv2.resize(annotated_frame, (960, 540))
        cv2.imshow("Vehicle Density", resized_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    video_path = "videos/test.mp4"
    calculate_density(video_path)
