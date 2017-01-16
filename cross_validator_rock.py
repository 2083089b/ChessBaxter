import numpy as np
from sklearn.cross_validation import cross_val_score        # In some other versions of scikit-learn the package is called sklearn.model_selection
from sklearn import svm
from sklearn.externals import joblib

clf = svm.SVC(kernel='linear', C=1)

X = joblib.load('chess_pieces/descriptors/white_knight/white_knight.pkl')
num_of_positives = len(X)

folders_names = ['white_rock','white_king','white_bishop','white_queen','white_pawn','white_knight']

boo = True
for folder_name in folders_names:
    X = np.concatenate((X,joblib.load('chess_pieces/descriptors/'+folder_name+'/'+folder_name+'.pkl')))
    if boo:
        num_of_positives = len(X)
        boo = False


num_of_negatives = len(X) - num_of_positives

y = np.ones((num_of_positives, 1))

y = np.ravel(np.concatenate((y,np.zeros((num_of_negatives, 1)))))
print y

# y = np.ones((num_of_positives, 1))
# y = np.ravel(np.concatenate((y,np.zeros((num_of_negatives, 1)))))

scores = cross_val_score(clf, X, y, cv=2)

print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
