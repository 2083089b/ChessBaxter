import numpy as np
import cv2
from predictor import predict

img = cv2.imread("window_132.jpeg")

a, max = predict(img)
print a
print max
# cv2.imshow("img", img)
#cv2.waitKey(0)
