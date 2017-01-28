import numpy as np
import cv2
from sklearn import svm
from sklearn.externals import joblib
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation

# @staticmethod
def dense_keypoints(img, scaleLevels=1, scaleFactor=1.2, varyStepWithScale=False):
	curScale = 1.0
	curStep = 5
	curBound = 5
	featureScaleMul = 1/scaleFactor
	kp = []
	for curLevel in range(0, scaleLevels):
		for x in range(curBound, img.shape[1] - curBound, curStep):
			for y in range(curBound, img.shape[0] - curBound, curStep):
				kp.append(cv2.KeyPoint(x, y, curScale, _class_id=0))

		curScale *= featureScaleMul
		if varyStepWithScale:
			curStep = curStep * featureScaleMul + 0.5

	return kp


# Initialize an SVC classifier
clf = svm.SVC(probability=True,verbose=True)

X = joblib.load('descriptors/SIFT/dense/pawn/pawn.pkl')
num_of_positives = len(X)
print num_of_positives

X = np.concatenate((X,joblib.load('descriptors/SIFT/dense/king/king.pkl')))


num_of_negatives = len(X) - num_of_positives

y = np.ones((num_of_positives, 1))
y = np.ravel(np.concatenate((y,np.zeros((num_of_negatives, 1)))))

print clf.fit(X,y)

img = cv2.imread("white_pawn27.png")
siftdesc = cv2.xfeatures2d.SIFT_create()
kp = dense_keypoints(img)
img = cv2.drawKeypoints(img,kp,img,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
kp, des1 = siftdesc.compute(img, kp)


cv2.imshow('img', img)
cv2.waitKey(0)

# orb = cv2.ORB_create(edgeThreshold=4)
# kp1, des1 = orb.detectAndCompute(img, None)

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

joblib.dump(clf,'classifiers/SIFT/densepawnVking_classifier.pkl')
