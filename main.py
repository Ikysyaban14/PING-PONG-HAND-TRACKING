import cv2
import pygame

from hand_detector import HandDetector
from game_logic import PongGame


def main():
    pygame.init()

    game = PongGame(width=1000, height=600)
    detector = HandDetector(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
    )

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: webcam tidak dapat dibuka.")
        pygame.quit()
        return

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    running = True

    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            success, frame = camera.read()

            if not success:
                hand_detected = False
                hand_y = None
            else:
                frame = cv2.flip(frame, 1)

                detector.find_hands(frame)
                hand_detected = detector.is_hand_detected()
                hand_y = detector.get_index_finger_y()

                # Gambar landmark tangan ke frame
                frame = detector.draw_landmarks(frame)

                # Tulis status "Hand Detected"
                if hand_detected:
                    cv2.putText(
                        frame,
                        "Hand Detected: YES",
                        (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2,
                    )
                else:
                    cv2.putText(
                        frame,
                        "Hand Detected: NO",
                        (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2,
                    )

                # Tampilkan jendela webcam
                cv2.imshow("Hand Tracking", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    running = False

            dt = game.tick(60)
            game.update(
                hand_y_normalized=hand_y,
                hand_detected=hand_detected,
                dt=dt,
            )

            game.draw(hand_detected)

    finally:
        camera.release()
        detector.close()
        cv2.destroyAllWindows()
        pygame.quit()


if __name__ == "__main__":
    main()