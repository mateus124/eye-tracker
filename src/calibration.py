import json
from collections import deque
from pathlib import Path

import cv2
import numpy as np

from display import create_calibration_display
from face import find_face
from gaze import get_eye_position


CALIBRATION_PATH = Path(__file__).resolve().parent.parent / "models" / "calibration.json"
CALIBRATION_VERSION = 2
CALIBRATION_POINTS = [
	(0.05, 0.05),
	(0.50, 0.05),
	(0.95, 0.05),
	(0.05, 0.50),
	(0.50, 0.50),
	(0.95, 0.50),
	(0.05, 0.95),
	(0.50, 0.95),
	(0.95, 0.95),
]


class Calibration:
	def __init__(self, coefficients):
		self.coefficients = np.array(coefficients, dtype=float)

	def transform(self, horizontal, vertical):
		values = np.array([1, horizontal, vertical, horizontal * vertical])
		point = values @ self.coefficients
		return max(0, min(float(point[0]), 1)), max(0, min(float(point[1]), 1))


class GazeFilter:
	def __init__(self, amount=0.25, window_size=5):
		self.amount = amount
		self.positions = deque(maxlen=window_size)
		self.position = (0.5, 0.5)

	def reset(self, position=(0.5, 0.5)):
		self.positions.clear()
		self.position = position

	def update(self, position):
		self.positions.append(position)
		filtered_horizontal = float(np.median([point[0] for point in self.positions]))
		filtered_vertical = float(np.median([point[1] for point in self.positions]))
		old_horizontal, old_vertical = self.position
		horizontal = old_horizontal + (filtered_horizontal - old_horizontal) * self.amount
		vertical = old_vertical + (filtered_vertical - old_vertical) * self.amount
		self.position = horizontal, vertical
		return self.position


def load_calibration():
	if not CALIBRATION_PATH.exists():
		return None

	with CALIBRATION_PATH.open("r", encoding="utf-8") as file:
		data = json.load(file)

	if data.get("version") != CALIBRATION_VERSION:
		return None

	return Calibration(data["coefficients"])


def save_calibration(samples, targets):
	inputs = []
	for horizontal, vertical in samples:
		inputs.append([1, horizontal, vertical, horizontal * vertical])

	coefficients = np.linalg.lstsq(np.array(inputs), np.array(targets), rcond=None)[0]
	CALIBRATION_PATH.parent.mkdir(parents=True, exist_ok=True)

	with CALIBRATION_PATH.open("w", encoding="utf-8") as file:
		json.dump(
			{"version": CALIBRATION_VERSION, "coefficients": coefficients.tolist()},
			file,
			indent=2,
		)

	return Calibration(coefficients)


def run_calibration(camera, landmarker, timestamp):
	samples = []
	targets = []
	wait_frames = 20
	frames_to_collect = 20

	for step, (target_x, target_y) in enumerate(CALIBRATION_POINTS, start=1):
		waited = 0
		collected = []

		while len(collected) < frames_to_collect:
			success, frame = camera.read()
			if not success:
				return None, timestamp

			frame = cv2.flip(frame, 1)
			face = find_face(landmarker, frame, timestamp)
			timestamp += 1

			if face is not None and waited >= wait_frames:
				height, width, _ = frame.shape
				_, _, horizontal, vertical = get_eye_position(face, width, height)
				collected.append((horizontal, vertical))

			if face is not None:
				waited += 1

			display = create_calibration_display(
				frame,
				target_x,
				target_y,
				step,
				len(CALIBRATION_POINTS),
				len(collected),
				frames_to_collect,
			)
			cv2.imshow("Eye Tracker", display)
			key = cv2.waitKey(1) & 0xFF
			if key == 27:
				return None, timestamp

		average_horizontal = sum(point[0] for point in collected) / len(collected)
		average_vertical = sum(point[1] for point in collected) / len(collected)
		samples.append((average_horizontal, average_vertical))
		targets.append((target_x, target_y))

	return save_calibration(samples, targets), timestamp


def get_direction(horizontal, vertical):
	if horizontal < 0.35:
		return "esquerda"

	if horizontal > 0.65:
		return "direita"

	if vertical < 0.35:
		return "cima"

	if vertical > 0.65:
		return "baixo"

	return "centro"
