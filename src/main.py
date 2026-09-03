import cv2
from cam import close_camera, get_frame, open_camera
from calibration import get_direction, load_calibration, run_calibration, smooth_position
from display import create_display
from face import create_landmarker, draw_face, find_face
from gaze import get_gaze_direction


def main():
    camera = open_camera()

    if camera is None:
        return

    cv2.namedWindow("Eye Tracker", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(
        "Eye Tracker",
        cv2.WND_PROP_FULLSCREEN,
        cv2.WINDOW_FULLSCREEN,
    )

    with create_landmarker() as landmarker:
        timestamp = 0
        calibration = load_calibration()
        horizontal = 0.5
        vertical = 0.5

        if calibration is None:
            calibration, timestamp = run_calibration(camera, landmarker, timestamp)
            if calibration is None:
                close_camera(camera)
                return

        while True:
            frame = get_frame(camera)

            if frame is None:
                break

            face = find_face(landmarker, frame, timestamp)
            timestamp += 1

            if face is not None:
                height, width, _ = frame.shape
                direction, left_iris, right_iris, raw_horizontal, raw_vertical = get_gaze_direction(
                    face, width, height
                )
                new_position = calibration.transform(raw_horizontal, raw_vertical)
                horizontal, vertical = smooth_position((horizontal, vertical), new_position, 0.35)
                direction = get_direction(horizontal, vertical)
                draw_face(frame, face)
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
            display = create_display(frame, horizontal, vertical)
            cv2.imshow("Eye Tracker", display)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("c"):
                calibration, timestamp = run_calibration(camera, landmarker, timestamp)
                if calibration is None:
                    break
            if key == 27:
                break

    close_camera(camera)


if __name__ == "__main__":
    main()