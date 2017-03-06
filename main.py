import numpy as np
import cv2
import math
from chessboard_detector import chessboard_homography
from sliding_windows import my_sliding_window		# Could be deleted
from final_sliding_window import final_sliding_window
import chess
import chess.uci
import glob
from label_image import label_image
import re
import tensorflow as tf, sys

def atoi(text):
	return int(text) if text.isdigit() else text

def natural_keys(text):
	return [ atoi(c) for c in re.split('(\d+)', text) ]


img_with_matches, img_with_homography, points = chessboard_homography()

corner1 = points[0]
corner2 = points[1]
corner3 = points[16]
corner4 = points[-1]

# print "Corners' coordinates: "
# print corner1           # TOP RIGHT
# print corner2           # TOP LEFT
# print corner3           # BOTTOM RIGHT
# print corner4           # BOTTOM LEFT       for 'camera_image3.jpeg'

# cv2.circle(img_with_homography, (corner1), 10, (255, 0, 0), 10)
# cv2.circle(img_with_homography, (corner2), 10, (255, 0, 0), 10)
# cv2.circle(img_with_homography, (corner3), 10, (255, 0, 0), 10)
# cv2.circle(img_with_homography, (corner4), 10, (255, 0, 0), 10)

# cv2.imshow('homography',img_with_homography)
# cv2.waitKey(0)

## Calculate the area of the trapezoid, which is more or less the shape
## of the chessboard in the image:
## A = (a+b)/2*h        being 'a' and 'b' the bases of the trapezoid and 'h' its height
## Very approximate as the height is simply one of the two sides
a = math.sqrt((corner1[1]-corner3[1])**2+(corner1[0]-corner3[0])**2)
# print "a: " + str(a)
b = math.sqrt((corner2[1]-corner4[1])**2+(corner2[0]-corner4[0])**2)
# print "b: " + str(b)
h = math.sqrt((corner1[1]-corner2[1])**2+(corner1[0]-corner2[0])**2)
# print "h: " + str(h)
area = (a+b)/2*h
# print "Area: " + str(area)

single_square = area/64
single_square_side = int(math.sqrt(single_square))
# print "One square has an average area that is equal to: " + str(single_square) + " and each side is: " + str(single_square_side) + "\n\n"


cropped_image = img_with_homography[int(corner4[1]-single_square_side):int(corner3[1]),int(corner3[0]):int(corner1[0])]

# If the width or the height of the cropped image equal zero, invert the order of the corners
if(np.shape(cropped_image)[0] == 0 or np.shape(cropped_image)[1] == 0):
	cropped_image = img_with_homography[int(corner2[1]-single_square_side):int(corner3[1]),int(corner4[0]):int(corner3[0])]

# cv2.imshow("Window", cropped_image)
# cv2.waitKey(0)
#my_sliding_window(cropped_image, single_square_side, corner1, corner2, corner3, corner4)
final_sliding_window(img_with_homography, points)
actual_list_of_points = [(1548, 135),(839, 154)]
c = 0
while(c<len(actual_list_of_points)-1):
	pt1 = actual_list_of_points[c]
	pt2 = actual_list_of_points[c+1]
	cv2.line(img_with_homography,pt1,pt2,0,3)
	c += 2

cv2.imshow("Window", img_with_homography)
cv2.waitKey(0)


########## UNCOMMENT FROM HERE
# results = []
# filenames = []
# for filename in glob.glob('sliding_windows/*.jpg'):
# 	filenames.append(filename)
#
# # Sort by natural keys
# filenames = sorted(filenames,key=natural_keys)
# print filenames
#
# # Unpersists graph from file
# with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
# 	graph_def = tf.GraphDef()
# 	graph_def.ParseFromString(f.read())
# 	_ = tf.import_graph_def(graph_def, name='')
#
# counter = 0
# for filename in filenames:
# 	results.append(label_image(filename))
# 	print results[-1], counter
# 	counter += 1
# 	# cv2.imshow("Sliding window", cv2.imread(filename))
# 	# cv2.waitKey(0)

########### TILL HERE

# INTO THE CHESS GAME
#board = chess.Board(current_state_of_the_board)
