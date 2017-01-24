import numpy as np
import cv2
from predictor import predict

img = cv2.imread("chess_pieces/window_13.jpeg")

a, max = predict(img)
print "\n\nPiece: " + str(a)
print "Max: " + str(max)
cv2.imshow("img", img)
cv2.waitKey(0)
