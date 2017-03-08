import tensorflow as tf, sys
import cv2


def label_image(image_path):

	# image_path = "sliding_windows/"+image_name
	# Read in the image_data
	image_data = tf.gfile.FastGFile(image_path, 'rb').read()
	# image_data = image_path

	# Loads label file, strips off carriage return
	label_lines = [line.rstrip() for line
					   in tf.gfile.GFile("retrained_labels.txt")]



	with tf.Session() as sess:

		# Feed the image_data as input to the graph and get first prediction
		softmax_tensor = sess.graph.get_tensor_by_name('hi/final_result:0')

		predictions = sess.run(softmax_tensor, \
				 {'hi/DecodeJpeg/contents:0': image_data})

		# Sort to show labels of first prediction in order of confidence
		top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

		boo = True
		# print "\n"
		for node_id in top_k:
			human_string = label_lines[node_id]
			score = predictions[0][node_id]
			# print('%s (score = %.5f)' % (human_string, score))
			if boo:
				prediction = human_string
				prediction_score = score
				boo = False

		# if prediction_score > 0.70:
		# cv2.imshow("Detected",cv2.imread(image_path))
		# cv2.waitKey(0)
	return prediction, prediction_score
