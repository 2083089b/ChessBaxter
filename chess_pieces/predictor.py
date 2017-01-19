import numpy as np
import cv2
from sklearn import svm
from sklearn.externals import joblib


def predict(img1):
    
    ### Read image and compute keypoints and descriptors ###
    ### USED BEFORE THIS WAS CHANGED TO A FUNCTION
    #img_name = 'white_rock/white_rock1.png'
    #img1 = cv2.imread(img_name,0)

    dictionary = {0:"king", 1:"queen", 2:"bishop", 3:"knight", 4:"rock", 5:"pawn"}
    orb = cv2.ORB_create(edgeThreshold=4)

    kp1, des1 = orb.detectAndCompute(img1,None)

    if des1 != None:
        c = 0
        final = []
        for c, des in enumerate(des1):
            if c < 50:
                final.append(des)

        ### Load classifiers from a pickle file ###
        classifiers = []
        classifiers.append(joblib.load('chess_pieces/classifiers/white_king_classifier.pkl'))
        classifiers.append(joblib.load('chess_pieces/classifiers/white_queen_classifier.pkl'))
        classifiers.append(joblib.load('chess_pieces/classifiers/white_bishop_classifier.pkl'))
        classifiers.append(joblib.load('chess_pieces/classifiers/white_knight_classifier.pkl'))
        classifiers.append(joblib.load('chess_pieces/classifiers/white_rock_classifier.pkl'))
        classifiers.append(joblib.load('chess_pieces/classifiers/white_pawn_classifier.pkl'))

        #king_clf = joblib.load('classifiers/white_king_classifier.pkl')
        #queen_clf = joblib.load('classifiers/white_queen_classifier.pkl')
        #bishop_clf = joblib.load('classifiers/white_bishop_classifier.pkl')
        #knight_clf = joblib.load('classifiers/white_knight_classifier.pkl')
        #rock_clf = joblib.load('classifiers/white_rock_classifier.pkl')
        #pawn_clf = joblib.load('classifiers/white_pawn_classifier.pkl')

        max = 0
        ## 0=king, 1=queen, 2=bishop, 3=knight, 4=rock, 5=pawn
        piece_counter = 0
        piece = ""
        for classifier in classifiers:
            result = classifier.predict(final)
            it_is = 0
            it_is_not = 0
            for elem in result:
                if elem == 1:
                    it_is += 1
                else:
                    it_is_not += 1
            

            #if it_is>it_is_not:
            #    print ("It's a: White Rock")
            #else:
            #    print ("Not a white rock")

            confidence = it_is/len(result)

            if confidence > max:
                max = confidence
                piece = piece_counter
            
            piece_counter += 1
            #print result

        # If a piece was detected, return the name of that piece and the classifier's confidence
        if piece != "":
            return dictionary[piece_counter], max

    return "None", 0
