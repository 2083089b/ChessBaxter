import numpy as np
import cv2
from sklearn import svm
from sklearn.externals import joblib


def predict(img1):

    ### Read image and compute keypoints and descriptors ###
    ### USED BEFORE THIS WAS CHANGED TO A FUNCTION
    #img_name = 'rock/rock1.png'
    #img1 = cv2.imread(img_name,0)

    dictionary = {0:"king", 1:"queen", 2:"bishop", 3:"knight", 4:"rock", 5:"square", 6:"pawn"}
    orb = cv2.ORB_create(edgeThreshold=4)

    kp1, des1 = orb.detectAndCompute(img1, None)
    for kp in kp1:
        cv2.circle(img1, (int(kp.pt[0]),int(kp.pt[1])), 1, (255, 0, 0), 1)

    # cv2.imshow("img1", img1)
    # cv2.waitKey(0)
    if np.size(des1) != 0:
        c = 0


        ### Load classifiers from a pickle file ###
        classifiers = []
        classifiers.append(joblib.load('chess_pieces/classifiers/king_classifier.pkl'))
        classifiers.append(joblib.load('chess_pieces/classifiers/queen_classifier.pkl'))
        classifiers.append(joblib.load('chess_pieces/classifiers/bishop_classifier.pkl'))
        classifiers.append(joblib.load('chess_pieces/classifiers/knight_classifier.pkl'))
        classifiers.append(joblib.load('chess_pieces/classifiers/rock_classifier.pkl'))
        classifiers.append(joblib.load('chess_pieces/classifiers/square_classifier.pkl'))
        classifiers.append(joblib.load('chess_pieces/classifiers/pawn_classifier.pkl'))

        max = float(0.0)
        piece_counter = -1
        piece = ""
        for classifier in classifiers:
            piece_counter += 1
            confidence = classifier.predict_proba(des1)
            print "Result " + str(piece_counter) + ": " + str(confidence[0])

            a = float(confidence[0][0])
            print "a " + str(a)
            print "max " + str(max)
            if a > max:
                max = a
                piece = piece_counter

        # If a piece was detected, return the name of that piece and the classifier's confidence
        if max > 0.75:
            print piece
            print "FINAL RESULT: " + str(dictionary[piece])
            return dictionary[piece], max

    return "None", 0
