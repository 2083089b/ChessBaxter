#from pyimagesearch.helpers import pyramid
from pyimagesearch.helpers import sliding_window
import time
import cv2

def my_sliding_window(image,single_square_side):
    # load the image and define the window width and height
    # TEMPORARY image = cv2.imread('screenshot.png')
    (winW, winH) = (single_square_side, single_square_side*2)



    for (x, y, window) in sliding_window(image, stepSize=32, windowSize=(winW, winH)):
	    # if the window does not meet our desired window size, ignore it
	    if window.shape[0] != winH or window.shape[1] != winW:
		    continue

	    # THIS IS WHERE YOU WOULD PROCESS YOUR WINDOW, SUCH AS APPLYING A
	    # MACHINE LEARNING CLASSIFIER TO CLASSIFY THE CONTENTS OF THE
	    # WINDOW

	    # since we do not have a classifier, we'll just draw the window
	    clone = image.copy()
	    cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
	    cv2.imshow("Window", clone)
	    cv2.waitKey(1)
	    time.sleep(0.025)