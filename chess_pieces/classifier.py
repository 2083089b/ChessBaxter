import numpy as np
import cv2
from sklearn import svm
from sklearn.externals import joblib
import pickle

img1 = cv2.imread('white_pawn.png',0)
img2 = cv2.imread('black_knight.png',0)
img3 = cv2.imread('white_pawn20.png',0)

# Initiate ORB detector
orb = cv2.ORB_create(edgeThreshold=4)

kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)
kp3, des3 = orb.detectAndCompute(img3,None)

print "number of keypoints in img3: " + str(len(des3))
#for kp in kp1:
#    cv2.circle(img1, (int(kp.pt[0]),int(kp.pt[1])), 3, (0, 0, 0), 1)

c = 0
final = []
for c, des in enumerate(des1):
    if c < 50:
        final.append(des)

c = 0
final2 = []
for c, des in enumerate(des2):
    if c < 50:
        final2.append(des)

c = 0
final3 = []
for c, des in enumerate(des3):
    if c < 50:
        final3.append(des)

# Save to a file for future use
joblib.dump(final,'descriptors/white_pawn.pkl')
joblib.dump(final2,'descriptors/black_knight.pkl')
joblib.dump(final3,'descriptors/white_pawn20.pkl')

clf = svm.SVC()

X = np.concatenate((final,final2,final3))


y = np.ones((len(final), 1))
y = np.concatenate((y,np.zeros((len(final), 1))))


print clf.fit(X,y)

joblib.dump(clf,'classifier/clf.pkl')
#cv2.imshow('img1',img1)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
