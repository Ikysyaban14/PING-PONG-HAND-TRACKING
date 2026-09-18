import cv2
import mediapipe as mp


class HandDetector:
    """
    Mengisolasi proses:
    - Membaca frame webcam
    - Mendeteksi tangan menggunakan MediaPipe
    - Menggambar landmark tangan
    - Mengambil koordinat Y jari telunjuk dan telapak tangan
    """

    def __init__(
        self,
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
    ):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

        self.results = None

    def find_hands(self, frame):
        """
        Mendeteksi tangan dari frame BGR OpenCV.

        Returns:
            frame_rgb: Frame RGB hasil konversi untuk MediaPipe.
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frame_rgb)

        return frame_rgb

    def draw_landmarks(self, frame):
        """
        Menggambar landmark tangan pada frame.
        """
        if self.results is None or not self.results.multi_hand_landmarks:
            return frame

        for hand_landmarks in self.results.multi_hand_landmarks:
            self.mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
            )

        return frame

    def is_hand_detected(self):
        """
        Returns:
            bool: True jika minimal satu tangan terdeteksi.
        """
        return (
            self.results is not None
            and self.results.multi_hand_landmarks is not None
            and len(self.results.multi_hand_landmarks) > 0
        )

    def get_index_finger_y(self):
        """
        Mengambil posisi Y jari telunjuk.

        MediaPipe mengembalikan koordinat normalized:
            0.0 = bagian atas frame
            1.0 = bagian bawah frame

        Returns:
            float atau None
        """
        if not self.is_hand_detected():
            return None

        hand_landmarks = self.results.multi_hand_landmarks[0]

        index_finger_tip = hand_landmarks.landmark[
            self.mp_hands.HandLandmark.INDEX_FINGER_TIP
        ]

        return index_finger_tip.y

    def get_palm_y(self):
        """
        Mengambil posisi Y telapak tangan menggunakan landmark WRIST.

        Returns:
            float atau None
        """
        if not self.is_hand_detected():
            return None

        hand_landmarks = self.results.multi_hand_landmarks[0]

        wrist = hand_landmarks.landmark[
            self.mp_hands.HandLandmark.WRIST
        ]

        return wrist.y

    def close(self):
        """
        Membersihkan resource MediaPipe.
        """
        self.hands.close()