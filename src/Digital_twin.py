from ultralytics import YOLO
import cv2
import time
import traci
import numpy as np

# -----------------------------
# CONFIG
# -----------------------------
MODEL_PATH = "models/vehicle_detection.pt"
VIDEO_PATH = "videos/test_twin.mp4"
SUMO_CONFIG = "simulation/Digital_Twin/digital_twin.sumocfg"

CONF_THRESHOLD = 0.4
STEP_TIME = 1.0
MAX_PER_TYPE = 8

CLASS_MAP = {
    "car": "car",
    "motorcycle": "bike",
    "bus": "bus",
    "truck": "truck",
    "auto": "auto"
}

# -----------------------------
# HOMOGRAPHY (YOUR POINTS)
# -----------------------------
SRC = np.float32([
    [243, 477],
    [700, 476],
    [488, 116],
    [408, 115]
])

DST = np.float32([
    [0, 0],
    [10, 0],
    [10, 30],
    [0, 30]
])

H, _ = cv2.findHomography(SRC, DST)

# Polygon for entry zone
ENTRY_POLYGON = np.array(SRC, dtype=np.int32)

# -----------------------------
# TRACKER
# -----------------------------


class Tracker:
    def __init__(self, max_dist=50):
        self.objects = {}
        self.next_id = 0
        self.max_dist = max_dist

    def update(self, detections):
        new_objects = {}

        for cx, cy, cls in detections:
            best_id = None
            best_dist = 1e9

            for oid, (px, py, pcl, counted) in self.objects.items():
                dist = np.hypot(cx - px, cy - py)
                if dist < best_dist and dist < self.max_dist:
                    best_dist = dist
                    best_id = oid

            if best_id is not None:
                _, _, _, counted = self.objects[best_id]
                new_objects[best_id] = (cx, cy, cls, counted)
            else:
                new_objects[self.next_id] = (cx, cy, cls, False)
                self.next_id += 1

        self.objects = new_objects
        return self.objects


tracker = Tracker()

# -----------------------------
# UTILS
# -----------------------------


def project_point(cx, cy):
    pt = np.array([[cx, cy]], dtype='float32')
    pt = np.array([pt])
    mapped = cv2.perspectiveTransform(pt, H)
    return mapped[0][0]


def get_lane_from_world(x_world):
    return "0" if x_world < 5 else "1"


# -----------------------------
# INIT
# -----------------------------
model = YOLO(MODEL_PATH)
traci.start(["sumo-gui", "-c", SUMO_CONFIG])


# -----------------------------
# MAIN LOOP
# -----------------------------
def run():

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print("❌ Cannot open video")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    buffer_size = max(1, fps)

    step = 0

    while True:

        start_time = time.time()
        frames = []

        for _ in range(buffer_size):
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)

        if len(frames) == 0:
            print("✅ Video ended")
            break

        lane_counts = {
            "0": {"car": 0, "bike": 0, "bus": 0, "truck": 0, "auto": 0},
            "1": {"car": 0, "bike": 0, "bus": 0, "truck": 0, "auto": 0},
        }

        detections = []

        # -------------------------
        # DETECTION
        # -------------------------
        for frame in frames:
            results = model(frame, conf=CONF_THRESHOLD)[0]

            for box in results.boxes:
                cls_id = int(box.cls)
                cls_name = model.names[cls_id]

                if cls_name not in CLASS_MAP:
                    continue

                x1, y1, x2, y2 = box.xyxy[0]

                cx = float((x1 + x2) / 2)
                cy = float((y1 + y2) / 2)

                detections.append((cx, cy, cls_name))

        # -------------------------
        # TRACKING
        # -------------------------
        tracked = tracker.update(detections)

        print(f"\n[STEP {step}] Tracked:", len(tracked))

        # -------------------------
        # ENTRY POLYGON COUNTING
        # -------------------------
        for oid, (cx, cy, cls_name, counted) in tracked.items():

            if counted:
                continue

            inside = cv2.pointPolygonTest(
                ENTRY_POLYGON, (int(cx), int(cy)), False)

            if inside >= 0:

                xw, _ = project_point(cx, cy)
                lane = get_lane_from_world(xw)

                vtype = CLASS_MAP[cls_name]

                lane_counts[lane][vtype] += 1

                # mark counted
                tracker.objects[oid] = (cx, cy, cls_name, True)

        total = sum(sum(types.values()) for types in lane_counts.values())

        print("TOTAL TO ADD:", total)
        print("LANE COUNTS:", lane_counts)

        # -------------------------
        # INSERT VEHICLES
        # -------------------------
        for lane, types in lane_counts.items():

            for vtype, count in types.items():

                count = min(MAX_PER_TYPE, count)

                for i in range(count):

                    veh_id = f"{step}_{lane}_{vtype}_{i}"

                    try:
                        traci.vehicle.add(
                            vehID=veh_id,
                            routeID="r0",
                            typeID=vtype,
                            depart="now",
                            departLane=lane
                        )
                        print(f"✔ Added {veh_id}")

                    except Exception as e:
                        print(f"❌ FAILED {veh_id}: {e}")

        traci.simulationStep()

        # -------------------------
        # DISPLAY
        # -------------------------
        annotated = results.plot()

        # draw polygon instead of line
        cv2.polylines(annotated, [ENTRY_POLYGON], True, (0, 255, 255), 2)

        display = cv2.resize(annotated, (960, 540))
        cv2.imshow("Digital Twin", display)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        # -------------------------
        # REAL-TIME SYNC
        # -------------------------
        elapsed = time.time() - start_time
        if elapsed < STEP_TIME:
            time.sleep(STEP_TIME - elapsed)

        step += 1

    cap.release()
    cv2.destroyAllWindows()
    traci.close()


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    run()
