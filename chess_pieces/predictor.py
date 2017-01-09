import numpy as np
import cv2
from sklearn import svm
from sklearn.externals import joblib


### Read image and compute keypoints and descriptors ###

img_name = 'white_pawn/white_pawn20.png'
img1 = cv2.imread(img_name,0)

orb = cv2.ORB_create(edgeThreshold=4)

kp1, des1 = orb.detectAndCompute(img1,None)

c = 0
final = []
for c, des in enumerate(des1):
    if c < 50:
        final.append(des)

### Load classifier from a pickle file ###
clf = joblib.load('classifiers/white_rock_classifier.pkl')

result = clf.predict(final)

it_is = 0
it_is_not = 0

for elem in result:
    if elem == 1:
        it_is += 1
    else:
        it_is_not += 1

if it_is:
    print ("It's a: White Rock")
else:
    print ("Not a white rock")
