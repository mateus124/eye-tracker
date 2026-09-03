from eyes import (
	LEFT_EYE_CORNERS,
	LEFT_EYE_TOP_BOTTOM,
	LEFT_IRIS,
	RIGHT_EYE_CORNERS,
	RIGHT_EYE_TOP_BOTTOM,
	RIGHT_IRIS,
	get_iris_center,
	get_point,
)


def get_gaze_direction(face_landmarks, width, height):
	left_iris, right_iris, horizontal, vertical = get_eye_position(
		face_landmarks, width, height
	)

	direction = "centro"
	if horizontal < 0.35:
		direction = "esquerda"
	elif horizontal > 0.65:
		direction = "direita"
	elif vertical < 0.35:
		direction = "cima"
	elif vertical > 0.65:
		direction = "baixo"

	return direction, left_iris, right_iris, horizontal, vertical


def get_eye_position(face_landmarks, width, height):
	left_corner_a = get_point(face_landmarks, LEFT_EYE_CORNERS[0], width, height)
	left_corner_b = get_point(face_landmarks, LEFT_EYE_CORNERS[1], width, height)
	right_corner_a = get_point(face_landmarks, RIGHT_EYE_CORNERS[0], width, height)
	right_corner_b = get_point(face_landmarks, RIGHT_EYE_CORNERS[1], width, height)
	left_eye_top = get_point(face_landmarks, LEFT_EYE_TOP_BOTTOM[0], width, height)
	left_eye_bottom = get_point(face_landmarks, LEFT_EYE_TOP_BOTTOM[1], width, height)
	right_eye_top = get_point(face_landmarks, RIGHT_EYE_TOP_BOTTOM[0], width, height)
	right_eye_bottom = get_point(face_landmarks, RIGHT_EYE_TOP_BOTTOM[1], width, height)
	left_iris = get_iris_center(face_landmarks, LEFT_IRIS, width, height)
	right_iris = get_iris_center(face_landmarks, RIGHT_IRIS, width, height)

	left_min_x, left_max_x = sorted((left_corner_a[0], left_corner_b[0]))
	right_min_x, right_max_x = sorted((right_corner_a[0], right_corner_b[0]))
	left_horizontal = (left_iris[0] - left_min_x) / max(left_max_x - left_min_x, 1)
	right_horizontal = (right_iris[0] - right_min_x) / max(right_max_x - right_min_x, 1)
	horizontal = (left_horizontal + right_horizontal) / 2
	left_vertical = (left_iris[1] - left_eye_top[1]) / max(left_eye_bottom[1] - left_eye_top[1], 1)
	right_vertical = (right_iris[1] - right_eye_top[1]) / max(right_eye_bottom[1] - right_eye_top[1], 1)
	vertical = (left_vertical + right_vertical) / 2
	horizontal = max(0, min(horizontal, 1))
	vertical = max(0, min(vertical, 1))

	return left_iris, right_iris, horizontal, vertical
