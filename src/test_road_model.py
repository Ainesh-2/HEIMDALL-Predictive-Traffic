from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("models/road_segmentation.pt")
frame = cv2.imread("videos/test_frame.jpg")
if frame is None:
    print("Error: Could not read the image.")
    exit()
h, w = frame.shape[:2]

result = model(frame)[0]
mask = result.masks.data[0].cpu().numpy()
mask = (mask > 0.5).astype(np.uint8) * 255
mask = cv2.resize(mask, (w, h))

contours, _ = cv2.findContours(
    mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

overlay = frame.copy()

cv2.drawContours(overlay, contours, -1, (0, 255, 0), 3)
# clean holes caused by vehicles
kernel_close = np.ones((45, 45), np.uint8)
kernel_open = np.ones((5, 5), np.uint8)
mask_clean = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)
mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_OPEN, kernel_open)

contours, _ = cv2.findContours(
    mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
largest = max(contours, key=cv2.contourArea)
final_mask = np.zeros_like(mask_clean)
cv2.drawContours(final_mask, [largest], -1, 255, thickness=cv2.FILLED)

contours, _ = cv2.findContours(
    mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

largest = max(contours, key=cv2.contourArea)

epsilon = 0.002 * cv2.arcLength(largest, True)
smooth_boundary = cv2.approxPolyDP(largest, epsilon, True)
overlay = frame.copy()
cv2.drawContours(overlay, [smooth_boundary], -1, (0, 255, 0), 3)

HD_W = 1280
HD_H = 720

display_frame = cv2.resize(overlay, (HD_W, HD_H))
display_mask = cv2.resize(mask, (HD_W, HD_H))


cv2.imshow("road border", display_frame)
cv2.imshow("mask", display_mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
