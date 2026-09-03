import cv2
from cam import close_camera, get_frame, open_camera
from face import create_landmarker, draw_face, find_face
from gaze import get_gaze_direction


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
PANEL_WIDTH = 320


def draw_screen_panel(frame, horizontal, vertical):
    panel_height = frame.shape[0]
    panel = frame.copy()
    panel = cv2.resize(panel, (PANEL_WIDTH, panel_height))
    panel[:] = (35, 35, 35)

    point_x = min(int(horizontal * PANEL_WIDTH), PANEL_WIDTH - 1)
    point_y = min(int(vertical * panel_height), panel_height - 1)
    cv2.rectangle(panel, (0, 0), (PANEL_WIDTH - 1, panel_height - 1), (255, 255, 255), 2)
    cv2.line(panel, (point_x, 0), (point_x, panel_height), (80, 80, 80), 1)
    cv2.line(panel, (0, point_y), (PANEL_WIDTH, point_y), (80, 80, 80), 1)
    cv2.circle(panel, (point_x, point_y), 8, (0, 0, 255), -1)
    return panel


def main():
    camera = open_camera()

    if camera is None:
        return

    with create_landmarker() as landmarker:
        timestamp = 0

        while True:
            frame = get_frame(camera)

            if frame is None:
                break

            face = find_face(landmarker, frame, timestamp)
            timestamp += 1

            if face is not None:
                height, width, _ = frame.shape
                direction, left_iris, right_iris, horizontal, vertical = get_gaze_direction(
                    face, width, height
                )
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
                cv2.putText(
                    frame,
                    f"X: {int(horizontal * SCREEN_WIDTH)} Y: {int(vertical * SCREEN_HEIGHT)}",
                    (20, 75),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )
                panel = draw_screen_panel(frame, horizontal, vertical)
                frame = cv2.hconcat([frame, panel])

            if face is None:
                panel = draw_screen_panel(frame, 0.5, 0.5)
                frame = cv2.hconcat([frame, panel])

            cv2.imshow("Eye Tracker", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    close_camera(camera)


if __name__ == "__main__":
    main()