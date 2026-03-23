import cv2
import mediapipe as mp
import time
import numpy as np
import math
import keyboard
from multiprocessing import Process
from proces2 import capture_and_process

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose

if __name__ == '__main__':

    # p1 = Process(target=capture_and_process, args=(1, 0))
    # p2 = Process(target=capture_and_process, args=(0, 3))
    p3 = Process(target=capture_and_process, args=(0, 1))
    
    # p1.start()
    # p2.start()
    p3.start()
    
    # p1.join()
    # p2.join()
    p3.join()
