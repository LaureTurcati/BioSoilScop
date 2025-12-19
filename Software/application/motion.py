import cv2
import numpy as np

class Motion:
    def __init__(self, config):
        self.config = config

    def basic_motion_detect (self, frame1, frame2):
        diff_frame = cv2.absdiff(frame1, frame2)
        binary_frame = cv2.threshold(src=diff_frame, thresh=self.config.motion_detect_threshold, maxval=255, type=cv2.THRESH_BINARY)[1]
        ones = np.count_nonzero(binary_frame)
        if (ones > self.config.mov_area) & (ones < self.config.vib_threshold):
            return ones, True
        else:
            return ones, False
