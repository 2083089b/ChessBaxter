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
from label_colour import label_colour
import re
import tensorflow as tf, sys
from chess_move import my_next_move
import time

def atoi(text):
	return int(text) if text.isdigit() else text

def natural_keys(text):
	return [ atoi(c) for c in re.split('(\d+)', text) ]

pieces = ["rook","knight","bishop","queen","king","pawn"]

returned_state_of_the_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"
result = ""
# START THE CHESS GAME
while result == "":

	###########
	####### UNCOMMENT FROM HERE
	##############


	colour_img, img_with_matches, img_with_homography, points = chessboard_homography()

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

	# cv2.imshow('homography',colour_img)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

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
	final_sliding_window(img_with_homography, points, colour_img)


	# cv2.imshow("Window", img_with_homography)
	# cv2.waitKey(0)


	########## UNCOMMENT FROM HERE
	results = []
	filenames = []
	for filename in glob.glob('sliding_windows/*.jpg'):
		filenames.append(filename)

	# Sort by natural keys
	filenames = sorted(filenames,key=natural_keys)

	# Unpersists graph from file for chess piece
	with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())
		_ = tf.import_graph_def(graph_def, name='hi')

	colours = []
	counter = 0
	for filename in filenames:
		prediction, score = label_image(filename)

		# filename_colour = 'sliding_windows/with_colours/sliding_window'+str(counter)+'.jpg'
		# colour_prediction, colour_score = label_colour(filename_colour)
		print score
		if score > 0.50:
			results.append(prediction)

			if prediction != "square":
				print "",
				# colours.append(colour_prediction)
				print prediction,
			else:
				print prediction
		else:
			results.append("empty")
			colours.append("noCol")
		# print results[-1], counter
		counter += 1
		# cv2.imshow("Sliding window", cv2.imread(filename))
		# cv2.waitKey(0)

	# Unpersists graph from file for colour
	with tf.gfile.FastGFile("retrained_graph_for_black_and_white.pb", 'rb') as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())
		_ = tf.import_graph_def(graph_def, name='yo')

	colours = []
	for c in range(0,64):
		filename_colour = 'sliding_windows/with_colours/sliding_window'+str(c)+'.jpg'
		colour_prediction, colour_score = label_colour(filename_colour)
		colours.append(colour_prediction)
		print results[c], colour_prediction
		c += 1

	for c in range(0,64):
		if c%8==0:
			print "\n"
		if results[c] in pieces and colours[c] == "blacks":
			results[c] = results[c].upper()
		print results[c], colours[c]

	###########
	######## UNTIL HEREEEE
	##########

	# results = ["rook","knight","bishop","queen","king","bishop","knight","rook",
	# 	   "pawn","pawn","pawn","pawn","pawn","pawn","pawn","pawn",
	# 	   "square","square","square","square","square","square","square","square",
	# 	   "square","square","square","square","square","square","square","square",
	# 	   "square","square","square","square","square","square","square","square",
	# 	   "square","square","square","square","square","square","square","square",
	# 	   "PAWN","PAWN","PAWN","PAWN","PAWN","PAWN","PAWN","PAWN",
	# 	   "ROOK","KNIGHT","BISHOP","QUEEN","KING","BISHOP","KNIGHT","ROOK"]


	# r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4
	current_state_of_the_board = ""
	consecutive_empty_square_counter = 0
	for c in range(0,64):
		if c%8==0:
			print ""
			# Avoid initial slashbar
			if c != 0:
				# If there are empty squares on the right edge of the board, save how many
				if consecutive_empty_square_counter != 0:
					current_state_of_the_board += str(consecutive_empty_square_counter)
					consecutive_empty_square_counter = 0
				current_state_of_the_board += "/"
		if results[c] == "king":
			print "k",
			if consecutive_empty_square_counter != 0:
				current_state_of_the_board += str(consecutive_empty_square_counter)
				consecutive_empty_square_counter = 0
			current_state_of_the_board += "k"
		elif results[c] == "KING":
			print "K",
			if consecutive_empty_square_counter != 0:
				current_state_of_the_board += str(consecutive_empty_square_counter)
				consecutive_empty_square_counter = 0
			current_state_of_the_board += "K"
		elif results[c] == "queen":
			print "q",
			if consecutive_empty_square_counter != 0:
				current_state_of_the_board += str(consecutive_empty_square_counter)
				consecutive_empty_square_counter = 0
			current_state_of_the_board += "q"
		elif results[c] == "QUEEN":
			print "Q",
			if consecutive_empty_square_counter != 0:
				current_state_of_the_board += str(consecutive_empty_square_counter)
				consecutive_empty_square_counter = 0
			current_state_of_the_board += "Q"
		elif results[c] == "knight":
			print "n",
			if consecutive_empty_square_counter != 0:
				current_state_of_the_board += str(consecutive_empty_square_counter)
				consecutive_empty_square_counter = 0
			current_state_of_the_board += "n"
		elif results[c] == "KNIGHT":
			print "N",
			if consecutive_empty_square_counter != 0:
				current_state_of_the_board += str(consecutive_empty_square_counter)
				consecutive_empty_square_counter = 0
			current_state_of_the_board += "N"
		elif results[c] == "bishop":
			print "b",
			if consecutive_empty_square_counter != 0:
				current_state_of_the_board += str(consecutive_empty_square_counter)
				consecutive_empty_square_counter = 0
			current_state_of_the_board += "b"
		elif results[c] == "BISHOP":
			print "B",
			if consecutive_empty_square_counter != 0:
				current_state_of_the_board += str(consecutive_empty_square_counter)
				consecutive_empty_square_counter = 0
			current_state_of_the_board += "B"
		elif results[c] == "pawn":
			print "p",
			if consecutive_empty_square_counter != 0:
				current_state_of_the_board += str(consecutive_empty_square_counter)
				consecutive_empty_square_counter = 0
			current_state_of_the_board += "p"
		elif results[c] == "PAWN":
			print "P",
			if consecutive_empty_square_counter != 0:
				current_state_of_the_board += str(consecutive_empty_square_counter)
				consecutive_empty_square_counter = 0
			current_state_of_the_board += "P"
		elif results[c] == "rook":
			print "r",
			if consecutive_empty_square_counter != 0:
				current_state_of_the_board += str(consecutive_empty_square_counter)
				consecutive_empty_square_counter = 0
			current_state_of_the_board += "r"
		elif results[c] == "ROOK":
			print "R",
			if consecutive_empty_square_counter != 0:
				current_state_of_the_board += str(consecutive_empty_square_counter)
				consecutive_empty_square_counter = 0
			current_state_of_the_board += "R"
		else:
			print ".",
			consecutive_empty_square_counter += 1

	# IT CAN PROBABLY BE DELETED
	# if current_state_of_the_board == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR":
	# 	current_state_of_the_board += "w KQkq - 0 0"

	chessboard_state_details = " " + returned_state_of_the_board.split(" ", 1)[1]
	# print "\nDetails:", chessboard_state_details
	whose_turn = chessboard_state_details[1]
	print "\nTurn:", whose_turn
	current_state_of_the_board += chessboard_state_details

	if whose_turn == "w":
		returned_state_of_the_board, result = my_next_move(current_state_of_the_board)

	if result != "":
		print result


	time.sleep(1)
	# TODO
	# Check colour of the pieces

	########### TILL HERE
