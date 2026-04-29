import cv2

VIDEO_PATH = "videos/test_twin.mp4"  # change if needed

points = []


def click_event(event, x, y, flags, param):
    global points, frame_copy

    if event == cv2.EVENT_LBUTTONDOWN:

        if len(points) < 4:
            points.append((x, y))
            print(f"Point {len(points)}: ({x}, {y})")

            # draw point
            cv2.circle(frame_copy, (x, y), 6, (0, 0, 255), -1)

            # draw lines between points
            if len(points) > 1:
                cv2.line(frame_copy, points[-2], points[-1], (0, 255, 0), 2)

            # close the polygon after 4 points
            if len(points) == 4:
                cv2.line(frame_copy, points[3], points[0], (0, 255, 0), 2)

            cv2.imshow("Pick Points", frame_copy)


def main():

    global frame_copy

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print("❌ Cannot open video")
        return

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("❌ Cannot read frame")
        return

    frame_copy = frame.copy()

    print("\n📌 INSTRUCTIONS:")
    print("Click 4 points in this order:")
    print("1️⃣ Bottom-left (near left lane)")
    print("2️⃣ Bottom-right (near right lane)")
    print("3️⃣ Top-right (far right)")
    print("4️⃣ Top-left (far left)\n")

    cv2.imshow("Pick Points", frame_copy)
    cv2.setMouseCallback("Pick Points", click_event)

    while True:
        key = cv2.waitKey(1)

        # press 'r' to reset
        if key == ord('r'):
            print("🔄 Resetting points...")
            points.clear()
            frame_copy = frame.copy()
            cv2.imshow("Pick Points", frame_copy)

        # press 'q' to quit
        elif key == ord('q'):
            break

    cv2.destroyAllWindows()

    if len(points) == 4:
        print("\n✅ FINAL POINTS (copy these):\n")
        print("SRC = np.float32([")
        for p in points:
            print(f"    [{p[0]}, {p[1]}],")
        print("])\n")
    else:
        print("\n❌ You must select exactly 4 points.")


if __name__ == "__main__":
    main()
