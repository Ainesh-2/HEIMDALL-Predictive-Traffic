from ultralytics import YOLO
import cv2

model = YOLO('models/vehicle_detection.pt')


def detect_density(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame, conf=0.5)
        annotated = results[0].plot()
        h, w = frame.shape[:2]
        lane_width = int(w*0.15)
        north_roi = (int(w/2-lane_width/2), 0,
                     int(w/2+lane_width/2), int(h*0.35))
        south_roi = (int(w/2-lane_width/2), int(h*0.65),
                     int(w/2+lane_width/2), h)
        west_roi = (0, int(h/2-lane_width/2),
                    int(w*0.35), int(h/2+lane_width/2))
        east_roi = (int(w*0.65), int(h/2-lane_width/2),
                    w, int(h/2+lane_width/2))

        north = south = east = west = 0
        for box in results[0].boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)
            cx, cy = int((x1+x2)/2), int((y1+y2)/2)
            if north_roi[0] < cx < north_roi[2] and north_roi[1] < cy < north_roi[3]:
                north += 1
                cv2.putText(annotated, 'N', (cx, cy), 0, 0.7, (0, 255, 0), 2)
            elif south_roi[0] < cx < south_roi[2] and south_roi[1] < cy < south_roi[3]:
                south += 1
                cv2.putText(annotated, 'S', (cx, cy), 0, 0.7, (0, 255, 0), 2)
            elif west_roi[0] < cx < west_roi[2] and west_roi[1] < cy < west_roi[3]:
                west += 1
                cv2.putText(annotated, 'W', (cx, cy), 0, 0.7, (0, 255, 0), 2)
            elif east_roi[0] < cx < east_roi[2] and east_roi[1] < cy < east_roi[3]:
                east += 1
                cv2.putText(annotated, 'E', (cx, cy), 0, 0.7, (0, 255, 0), 2)
        for roi, colour in [
            (north_roi, (255, 0, 0)),
            (south_roi, (0, 255, 0)),
            (west_roi, (0, 0, 255)),
            (east_roi, (255, 255, 0))
        ]:
            cv2.rectangle(annotated, (roi[0], roi[1]),
                          (roi[2], roi[3]), colour, 2)
        cv2.putText(annotated, f'N: {north}', (20, 40), 0, 0.7, (255, 0, 0), 2)
        cv2.putText(annotated, f'S: {south}', (20, 70), 0, 0.7, (0, 255, 0), 2)
        cv2.putText(annotated, f'W: {west}', (20, 100), 0, 0.7, (0, 0, 255), 2)
        cv2.putText(annotated, f'E: {east}',
                    (20, 130), 0, 0.7, (255, 255, 0), 2)
        resized = cv2.resize(annotated, (960, 540))
        cv2.imshow('Density Intersection', resized)
        print(f'N: {north}, S: {south}, W: {west}, E: {east}')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    video_path = 'videos/test.mp4'
    detect_density(video_path)
