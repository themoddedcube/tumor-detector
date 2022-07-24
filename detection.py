import numpy as np
import cv2

image = cv2.imread('2.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
x,y,w,h = cv2.boundingRect(thresh)
ROI = image[y:y+h, x:x+w]

hsv = cv2.cvtColor(ROI, cv2.COLOR_BGR2HSV)
lower = np.array([0, 0, 152])
upper = np.array([179, 255, 255])
mask = cv2.inRange(hsv, lower, upper)

x, y, w, h = 0, 0, ROI.shape[1]//2, ROI.shape[0]
left = mask[y:y+h, x:x+w]
right = mask[y:y+h, x+w:x+w+w]

#Uncomment when not scan with black background
# total_pixels = cv2.countNonZero(left) + cv2.countNonZero(right)
# left_pixels = total_pixels - cv2.countNonZero(left)
# right_pixels = total_pixels - cv2.countNonZero(right)

# if left_pixels > right_pixels:
#     print('Left pixels:', left_pixels)
#     cv2.putText(image,'On Left', (7, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 180, 0), 3)
# else:
#     print('Right pixels:', right_pixels)
#     cv2.putText(image,'On Right', (7, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 180, 0), 3)

left_pixels = cv2.countNonZero(left)
right_pixels = cv2.countNonZero(right)

if left_pixels > right_pixels:
    print('Left pixels:', left_pixels)
    cv2.putText(image,'On Left', (7, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 180, 0), 3)
    
else:
    print('Right pixels:', right_pixels)
    cv2.putText(image,'On Right', (7, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 180, 0), 3)

image = cv2.resize(image, (540, 540))
cv2.imshow('img', image)
cv2.waitKey()
