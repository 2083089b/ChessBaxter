import numpy as np
import cv2
from sklearn import svm
from sklearn.externals import joblib
from test_dense import myPredict


img = cv2.imread('white_pawn27.png')
print myPredict(img)



# cv2.imshow('img', img)
# cv2.waitKey(0)
