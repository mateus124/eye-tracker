import cv2
import mediapipe as mp
from pathlib import Path
from urllib.request import urlretrieve

LEFT_EYE_CORNERS = [33, 133]
RIGHT_EYE_CORNERS = [362, 263]
LEFT_IRIS = [468, 469, 470, 471, 472]
RIGHT_IRIS = [473, 474, 475, 476, 477]
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "face_landmarker.task"

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

def get_gaze_direction(face_landmarks, width, height):
    left_corner_a = get_point(face_landmarks, LEFT_EYE_CORNERS[0], width, height)
    left_corner_b = get_point(face_landmarks, LEFT_EYE_CORNERS[1], width, height)
    right_corner_a = get_point(face_landmarks, RIGHT_EYE_CORNERS[0], width, height)
    right_corner_b = get_point(face_landmarks, RIGHT_EYE_CORNERS[1], width, height)
    left_iris = get_iris_center(face_landmarks, LEFT_IRIS, width, height)
    right_iris = get_iris_center(face_landmarks, RIGHT_IRIS, width, height)

    left_min_x, left_max_x = sorted((left_corner_a[0], left_corner_b[0]))
    right_min_x, right_max_x = sorted((right_corner_a[0], right_corner_b[0]))
    left_center_y = (left_corner_a[1] + left_corner_b[1]) / 2
    right_center_y = (right_corner_a[1] + right_corner_b[1]) / 2

    left_horizontal = (left_iris[0] - left_min_x) / max(left_max_x - left_min_x, 1)
    right_horizontal = (right_iris[0] - right_min_x) / max(right_max_x - right_min_x, 1)
    horizontal = (left_horizontal + right_horizontal) / 2
    vertical = ((left_iris[1] - left_center_y) + (right_iris[1] - right_center_y)) / 2

    if horizontal < 0.35:
        return "esquerda", left_iris, right_iris
    if horizontal > 0.65:
        return "direita", left_iris, right_iris
    if vertical < -4:
        return "cima", left_iris, right_iris
    if vertical > 4:
        return "baixo", left_iris, right_iris
    return "centro", left_iris, right_iris


def main():
    if not MODEL_PATH.exists():
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        print("Baixando modelo do MediaPipe...")
        urlretrieve(MODEL_URL, MODEL_PATH)

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Erro: não foi possível abrir a webcam.")
        return

    base_options = mp.tasks.BaseOptions(model_asset_path=str(MODEL_PATH))
    options = mp.tasks.vision.FaceLandmarkerOptions(base_options=base_options)
    options.running_mode = mp.tasks.vision.RunningMode.VIDEO
    options.num_faces = 1
    options.min_face_detection_confidence = 0.5
    options.min_face_presence_confidence = 0.5
    options.min_tracking_confidence = 0.5

    with mp.tasks.vision.FaceLandmarker.create_from_options(options) as landmarker:
        timestamp = 0

        while True:
            success, frame = camera.read()

            if not success:
                print("Erro ao capturar frame.")
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            results = landmarker.detect_for_video(image, timestamp)
            timestamp += 1

            if results.face_landmarks:
                height, width, _ = frame.shape
                face = results.face_landmarks[0]
                direction, left_iris, right_iris = get_gaze_direction(face, width, height)

                for landmark in face:
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)
                    cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

                cv2.circle(frame, left_iris, 4, (0, 0, 255), -1)
                cv2.circle(frame, right_iris, 4, (0, 0, 255), -1)
                cv2.putText(
                    frame,
                    f"Olhar: {direction}",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

            cv2.imshow("Eye Tracker", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()