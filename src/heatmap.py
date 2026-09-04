from datetime import datetime
from pathlib import Path

import cv2
import numpy as np


HEATMAP_WIDTH = 1280
HEATMAP_HEIGHT = 720
OUTPUT_DIRECTORY = Path(__file__).resolve().parent.parent / "reports"


class GazeHeatmap:
	def __init__(self, width=HEATMAP_WIDTH, height=HEATMAP_HEIGHT):
		self.width = width
		self.height = height
		self.accumulator = np.zeros((height, width), dtype=np.float32)
		self.samples = 0

	def add(self, horizontal, vertical):
		point_x = min(max(int(horizontal * self.width), 0), self.width - 1)
		point_y = min(max(int(vertical * self.height), 0), self.height - 1)
		self.accumulator[point_y, point_x] += 1
		self.samples += 1

	def save(self, output_directory=OUTPUT_DIRECTORY):
		if self.samples == 0:
			return None

		smoothed = cv2.GaussianBlur(self.accumulator, (0, 0), 28)
		normalized = cv2.normalize(smoothed, None, 0, 255, cv2.NORM_MINMAX)
		heatmap = cv2.applyColorMap(normalized.astype(np.uint8), cv2.COLORMAP_JET)
		heatmap[smoothed == 0] = (25, 25, 25)

		peak_y, peak_x = np.unravel_index(np.argmax(smoothed), smoothed.shape)
		cv2.drawMarker(
			heatmap,
			(int(peak_x), int(peak_y)),
			(255, 255, 255),
			cv2.MARKER_CROSS,
			30,
			2,
		)
		cv2.putText(
			heatmap,
			f"Amostras: {self.samples}",
			(20, 40),
			cv2.FONT_HERSHEY_SIMPLEX,
			0.9,
			(255, 255, 255),
			2,
			cv2.LINE_AA,
		)

		output_directory.mkdir(parents=True, exist_ok=True)
		output_path = output_directory / (
			f"gaze_heatmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
		)
		cv2.imwrite(str(output_path), heatmap)
		return output_path