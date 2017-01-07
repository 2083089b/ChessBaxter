import numpy as np
import cv2


img = cv2.imread('white_pawn.png',0)

# Initiate SIFT detector
siftdesc = cv2.xfeatures2d.SIFT_create()

(kp1, des1) = siftdesc.detectAndCompute(img, None)

for kp in kp1:
    cv2.circle(img, (int(kp.pt[0]),int(kp.pt[1])), 4, (0, 0, 0), 1)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
