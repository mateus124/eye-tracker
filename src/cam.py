import cv2


def open_camera():
	camera = cv2.VideoCapture(0)

	if not camera.isOpened():
		print("Erro: não foi possível abrir a webcam.")
		return None

	return camera


def get_frame(camera):
	success, frame = camera.read()

	if not success:
		print("Erro ao capturar frame.")
		return None

	return cv2.flip(frame, 1)


def close_camera(camera):
	camera.release()
	cv2.destroyAllWindows()
