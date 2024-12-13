import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2 as cv
import time  # Added for timestamp handling

class GestureDetector:
    def __init__(self, gestureSpace):
        self.recognizer: vision.GestureRecognizer = None
        self.maxGestureCount = gestureSpace
        self.gestures: [] = []
        # https: // ai.google.dev / edge / mediapipe / solutions / vision / gesture_recognizer
        self.possibleGestures = ["None", "Closed_Fist", "Open_Palm", "Thumb_Down",
                                 "Thumb_Up", "ILoveYou"]

        self.frame_count: int = 0
        self.cam: cv.VideoCapture = None
        self.shrinkFactor = 5  # Factor to shrink the camera image from
        # DO NOT CHANGE
        self.width: int = 0
        self.height: int = 0

        self.last_timestamp_ms = 0  # Keeps track of the last timestamp
        self.configRecognizer("model/gesture_recognizer.task")

    def print_result(self, result: vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        if result.gestures != []:
            data = result.gestures[0][0]
            name = data.category_name
            confidence = data.score
            gestureData = {"Name": name, "Confidence": round(confidence * 100, 2), "Timestamp": timestamp_ms}
            self.appendGestureData(gestureData)
        else:
            gestureData = {"Name": None, "Confidence": None, "Timestamp": timestamp_ms}
            self.appendGestureData(gestureData)

    def appendGestureData(self, gestureData):
        if not self.gestures:
            self.gestures.append(gestureData)
            return

        if len(self.gestures) < 10:
            self.gestures.append(gestureData)
        else:
            self.gestures[0:9] = self.gestures[1:10]
            self.gestures[-1] = gestureData

    def configRecognizer(self, model_path):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.GestureRecognizerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            result_callback=self.print_result
        )
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

    def initStream(self):
        self.cam = cv.VideoCapture(1)

        if not self.cam.isOpened():
            print("Unable to access camera")
            self.cam.release()
            exit()

        self.width = int(self.cam.get(cv.CAP_PROP_FRAME_WIDTH) / self.shrinkFactor)
        self.height = int(self.cam.get(cv.CAP_PROP_FRAME_HEIGHT) / self.shrinkFactor)

        self.frame_count = 0
        self.last_timestamp_ms = int(time.time() * 1000)  # Initialize the timestamp in milliseconds

    def getCurrentFrame(self) -> np.array:
        retrieved, frame = self.cam.read()

        if not retrieved:
            print("Stream has likely ended")
            return None

        # Ensure the timestamp is monotonically increasing
        current_timestamp_ms = int(time.time() * 1000)
        if current_timestamp_ms <= self.last_timestamp_ms:
            current_timestamp_ms = self.last_timestamp_ms + 1
        self.last_timestamp_ms = current_timestamp_ms

        # Prepare the frame for MediaPipe
        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        self.recognizer.recognize_async(mp_img, current_timestamp_ms)

        # Resize the frame for display
        frame = cv.resize(frame, (self.width, self.height))
        return frame
