import cv2

cap = cv2.VideoCapture("videos/test.mp4")
ret, frame = cap.read()
cv2.imwrite("videos/test_frame.jpg", frame)
cap.release()
