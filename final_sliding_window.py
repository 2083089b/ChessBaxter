import cv2
import math

#
# Write to file 64 images representing each square of the chessboard.
# These images will then be used by tensorflow to predict which piece,
# if any, sits on them.
def final_sliding_window(img, lines_coordinates):

	mid_point_top_x = lines_coordinates[26][0]
	mid_point_bottom_x = lines_coordinates[27][0]
	mid_point_average = int(round(mid_point_top_x+mid_point_bottom_x)/2)
	# print mid_point_average
	global_counter = 0
	points = []
	c = 2
	while c < len(lines_coordinates)/2:
		# print lines_coordinates[c]
		pt1 = lines_coordinates[c]
		pt2 = lines_coordinates[c+1]
		# print pt1,pt2
		mean_height = int(round((pt1[1]+pt2[1])/2))
		# cv2.line(img,(0,mean_height),(1800,mean_height),(0,0,0))
		c += 2

		pt3 = int(round(pt1[0]))
		pt4 = int(round(pt1[1]))
		pt5 = int(round(pt2[0]))
		pt6 = int(round(pt2[1]))
		# corners on the edges, right
		# cv2.circle(img, ((pt3),(pt4)), 5, (255, 0, 0), 5)
		# corners on the edges, left
		# cv2.circle(img, ((pt5),(pt6)), 5, (255, 0, 0), 5)
		# first_half_length_of_line = math.sqrt((pt6 - pt4)**2 + (pt5 - pt3)**2)
		# cv2.circle(img,((mid_point_average,mean_height)), 5, (255, 0, 0), 5)
		first_half_length_of_line = math.sqrt((mid_point_average - pt5)**2 + (mean_height - pt6)**2)
		# second_half_length_of_line = math.sqrt((pt6 - pt4)**2 + (pt5 - pt3)**2)
		second_half_length_of_line = math.sqrt((pt3 - mid_point_average)**2 + (pt4 - mean_height)**2)
		first_step = int(round(first_half_length_of_line/4))
		second_step = int(round(second_half_length_of_line/4))
		# print length_of_line, step
		current_point = pt5
		c2 = 0
		# points.append([])
		points = []
		while c2 < 5:
			# cv2.circle(img, ((current_point),(mean_height)), 5, (0, 0, 0), 5)
			points.append([current_point,mean_height])
			c2 += 1
			current_point = current_point + first_step

		while c2 < 9:
			# cv2.circle(img, ((current_point),(mean_height)), 5, (0, 0, 0), 5)
			points.append([current_point,mean_height])
			c2 += 1
			current_point = current_point + second_step

		# print c
		# print points, len(points)
		c3 = 0
		while c3 < 8:
			# change the height of the sliding window according to the distance from the camera
			# (the higher c, the closer to the camera, the bigger the sliding_window)
			if c < 14:
				sliding_window = img[mean_height-150:mean_height, points[c3][0]:points[c3+1][0]]
			elif c < 18:
				sliding_window = img[mean_height-200:mean_height, points[c3][0]:points[c3+1][0]]
			else:
				sliding_window = img[mean_height-250:mean_height, points[c3][0]:points[c3+1][0]]
			# cv2.imshow("sliding_window",sliding_window)
			# cv2.waitKey(0)
			cv2.imwrite('sliding_windows/sliding_window'+str(global_counter)+".jpg",sliding_window)
			c3 += 1
			global_counter += 1
