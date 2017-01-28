import numpy as np
import cv2
from sklearn import svm
from sklearn.externals import joblib
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation

# Initialize an SVC classifier
clf = svm.SVC(probability=True,verbose=True)
# clf = LogisticRegression(C=1, penalty='l1')

X = joblib.load('descriptors/ORB/pawn/pawn.pkl')
XXX = np.copy(X)
num_of_positives = len(X)
print num_of_positives

X = np.concatenate((X,joblib.load('descriptors/ORB/king/king.pkl')))


num_of_negatives = len(X) - num_of_positives

y = np.ones((num_of_positives, 1))
y = np.ravel(np.concatenate((y,np.zeros((num_of_negatives, 1)))))

print clf.fit(X,y)
img = cv2.imread("white_pawn27.png")
# siftdesc = cv2.xfeatures2d.SIFT_create()
# kp1, des1 = siftdesc.detectAndCompute(img, None)

orb = cv2.ORB_create(edgeThreshold=4)
kp1, des1 = orb.detectAndCompute(img, None)

prediction = clf.predict(des1)
print prediction
print clf.predict_proba(des1)

total = 0
counter = 0
for entry in clf.predict_proba(des1):
    if prediction[counter] == 1:
        total = total + entry[0]
    else:
        total = total + entry[1]
    counter += 1

print "Mean: " + str(total/counter)

joblib.dump(clf,'classifiers/ORB/pawnVking_classifier.pkl')