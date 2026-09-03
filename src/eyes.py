LEFT_EYE_CORNERS = [33, 133]
RIGHT_EYE_CORNERS = [362, 263]
LEFT_EYE_TOP_BOTTOM = [159, 145]
RIGHT_EYE_TOP_BOTTOM = [386, 374]
LEFT_IRIS = [468, 469, 470, 471, 472]
RIGHT_IRIS = [473, 474, 475, 476, 477]


def get_point(landmarks, index, width, height):
	landmark = landmarks[index]
	return int(landmark.x * width), int(landmark.y * height)


def get_iris_center(landmarks, iris_indices, width, height):
	x_total = 0
	y_total = 0

	for index in iris_indices:
		x, y = get_point(landmarks, index, width, height)
		x_total += x
		y_total += y

	return x_total // len(iris_indices), y_total // len(iris_indices)
