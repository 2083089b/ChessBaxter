import numpy as np
import cv2
import pickle
import glob
from sklearn.externals import joblib


# Initiate ORB detector
orb = cv2.ORB_create(edgeThreshold=4)


folders_names = ['white_bishop','white_king','white_knight','white_pawn','white_queen','white_rock'] # Missing the square

# Go through each folder containing pictures of the chess pieces
for folder_name in folders_names:
    # Read all images in the current folder
    images = []
    for filename in glob.glob(folder_name+'/*.png'):
        images.append(cv2.imread(filename,0))
        #images.append(np.array(Image.open(filename)))

    descriptors = []

    for image in images:
        # Detect and compute key points and descriptors for the image
        kp1, des1 = orb.detectAndCompute(image,None)

        for c, des in enumerate(des1):
            if c < 50:
                descriptors.append(des)

    joblib.dump(descriptors,'descriptors/'+folder_name+'/'+folder_name+'.pkl')
