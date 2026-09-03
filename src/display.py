import cv2
import numpy as np


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720
CAMERA_WIDTH = 280


def create_display(frame, horizontal, vertical):
    display = np.zeros((DISPLAY_HEIGHT, DISPLAY_WIDTH, 3), dtype=frame.dtype)
    display[:] = (25, 25, 25)

    point_x = min(int(horizontal * DISPLAY_WIDTH), DISPLAY_WIDTH - 1)
    point_y = min(int(vertical * DISPLAY_HEIGHT), DISPLAY_HEIGHT - 1)
    cv2.circle(display, (point_x, point_y), 22, (0, 0, 80), -1)
    cv2.circle(display, (point_x, point_y), 10, (0, 0, 255), -1)
    cv2.line(display, (point_x - 35, point_y), (point_x + 35, point_y), (0, 0, 255), 2)
    cv2.line(display, (point_x, point_y - 35), (point_x, point_y + 35), (0, 0, 255), 2)

    camera_height = int(frame.shape[0] * CAMERA_WIDTH / frame.shape[1])
    camera = cv2.resize(frame, (CAMERA_WIDTH, camera_height))
    camera_x = DISPLAY_WIDTH - CAMERA_WIDTH - 20
    camera_y = 20
    display[camera_y:camera_y + camera_height, camera_x:camera_x + CAMERA_WIDTH] = camera
    cv2.rectangle(
        display,
        (camera_x, camera_y),
        (camera_x + CAMERA_WIDTH, camera_y + camera_height),
        (255, 255, 255),
        2,
    )

    cv2.putText(
        display,
        f"X: {int(horizontal * SCREEN_WIDTH)} Y: {int(vertical * SCREEN_HEIGHT)}",
        (30, DISPLAY_HEIGHT - 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    return display


def create_calibration_display(
    frame, target_x, target_y, step, total_steps, collected=0, total_frames=0
):
    display = np.zeros((DISPLAY_HEIGHT, DISPLAY_WIDTH, 3), dtype=frame.dtype)
    display[:] = (25, 25, 25)

    point_x = int(target_x * DISPLAY_WIDTH)
    point_y = int(target_y * DISPLAY_HEIGHT)
    cv2.circle(display, (point_x, point_y), 24, (0, 0, 100), -1)
    cv2.circle(display, (point_x, point_y), 10, (0, 0, 255), -1)
    cv2.putText(
        display,
        f"Calibracao {step}/{total_steps} - olhe para o ponto",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        display,
        f"Amostras: {collected}/{total_frames}",
        (30, 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (200, 200, 200),
        2,
        cv2.LINE_AA,
    )

    camera_height = int(frame.shape[0] * CAMERA_WIDTH / frame.shape[1])
    camera = cv2.resize(frame, (CAMERA_WIDTH, camera_height))
    camera_x = DISPLAY_WIDTH - CAMERA_WIDTH - 20
    camera_y = 20
    display[camera_y:camera_y + camera_height, camera_x:camera_x + CAMERA_WIDTH] = camera
    cv2.rectangle(
        display,
        (camera_x, camera_y),
        (camera_x + CAMERA_WIDTH, camera_y + camera_height),
        (255, 255, 255),
        2,
    )
    return display
