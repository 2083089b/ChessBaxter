# ChessBaxter
# 4th year project - Lorenzo Betto

[Abstract of the dissertation]

The purpose of this project is to develop computer vision modules that allow Baxter the robot to understand the state of the chessboard and be able to inform on the next move. Since object recognition is an especially challenging problem for small objects like chess pieces, what seemed more logical was to follow the trial and error method for finding the most suitable classification model. Several computer vision and machine learning techniques were used, each giving different comparable results that helped deciding on their suitability for this particular context.
When it came to carrying out piece recognition to detect the state of the board, machine learning was not the only field that this project explored. When the tests with machine learning classification models were not giving the expected results, the cutting-edge field of Deep Learning was also tried out and as it turns out, it performs much better than other techniques surveyed in this project. With Deep Learning it is in fact possible to perform image classification using a pre-trained classifier that is re-trained to be able to classify new objects. The final results show that deep learning is a much powerful tool for image classification and that with as little as 663 training images for six classes, it can reach more than 90% accuracy.


[Main files]

The directory 'FINAL_working_files/code' contains the code for the final pipeline, which includes the code for the detection of the chessboard, three deep learning classifiers (piece, colour and empty and non-empty square classifications) and the code for the chess engine. No training data was uploaded to this GitHub repo.