import cv2
import mediapipe as mp
from pathlib import Path
from urllib.request import urlretrieve


MODEL_URL = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "face_landmarker.task"


def download_model():
	if not MODEL_PATH.exists():
		MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
		print("Baixando modelo do MediaPipe...")
		urlretrieve(MODEL_URL, MODEL_PATH)


def create_landmarker():
	download_model()

	base_options = mp.tasks.BaseOptions(model_asset_path=str(MODEL_PATH))
	options = mp.tasks.vision.FaceLandmarkerOptions(base_options=base_options)
	options.running_mode = mp.tasks.vision.RunningMode.VIDEO
	options.num_faces = 1
	options.min_face_detection_confidence = 0.5
	options.min_face_presence_confidence = 0.5
	options.min_tracking_confidence = 0.5

	return mp.tasks.vision.FaceLandmarker.create_from_options(options)


def find_face(landmarker, frame, timestamp):
	rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
	results = landmarker.detect_for_video(image, timestamp)

	if results.face_landmarks:
		return results.face_landmarks[0]

	return None


def draw_face(frame, face):
	height, width, _ = frame.shape

	for landmark in face:
		x = int(landmark.x * width)
		y = int(landmark.y * height)
		cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
