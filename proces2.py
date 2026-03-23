import cv2
import mediapipe as mp
import time
import numpy as np
import math
import keyboard
import pyautogui
from multiprocessing import Process

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose

def capture_and_process(camera_id, com):
    cap = cv2.VideoCapture(camera_id)
    pose = mpPose.Pose()
    pTime = 0
    angle = [0, 30, 55, 100, 120, 180]

    vpose = {
        'left-30' : [4, 5, 6, 7, 8],
        'left-60' : [9, 10, 11, 12, 13],
        'left-90' : [14, 15, 16, 17, 18],
        'left-angle[4]' : [19, 20, 21, 22, 23],
        'left-180' : [24, 25, 26, 27, 28],
        'right-30' : [4, 9, 14, 19, 24],
        'right-60' : [5, 10, 15, 20, 25],
        'right-90' : [6, 11, 16, 21, 26],
        'right-angle[4]' : [7, 12, 17, 22, 27],
        'right-180' : [8, 13, 18, 23, 28],
        'left-center' : [1, 2],
        'right-center' : [1, 3]
    }   

    def calculate_angle(lm1, lm2, lm3):
        v1_x = lm1.x - lm2.x
        v1_y = lm1.y - lm2.y

        v2_x = lm3.x - lm2.x
        v2_y = lm3.y - lm2.y

        dot_product = v1_x * v2_x + v1_y * v2_y

        magnitude_v1 = math.sqrt(v1_x ** 2 + v1_y ** 2)
        magnitude_v2 = math.sqrt(v2_x ** 2 + v2_y ** 2)

        if magnitude_v1 == 0 or magnitude_v2 == 0:
            return 0

        cos_theta = dot_product / (magnitude_v1 * magnitude_v2)
        cos_theta = max(-1.0, min(1.0, cos_theta))
        angle_radian = math.acos(cos_theta)
        angle_degree = math.degrees(angle_radian)

        return angle_degree
    
    def command(val):
        if com==3:
            if val==2:
                keyboard.press('up')
            else:
                keyboard.release('up')
                
        
        if com==2:
            if val in list(set(vpose['right-90']) & set(vpose['left-90'])):
                keyboard.press('f')
                keyboard.press('j')
            elif val in list(set(vpose['left-180'])):
                keyboard.press_and_release('f')
                keyboard.press_and_release('f')
            elif val in list(set(vpose['right-90'])):
                keyboard.press('j')
            elif val in list(set(vpose['left-90'])):
                keyboard.press('f')
            else:
                keyboard.release('f')
                keyboard.release('j')
                
        elif val in [1]:
            if com==0 or com==1:
                keyboard.press('r')
        
        elif val in list(set(vpose['right-90']) & set(vpose['left-180'])):
            if com==0:
                keyboard.press('right')
                keyboard.press('up')
            if com==1:
                keyboard.press('d')
                keyboard.press('w')

        elif val in list(set(vpose['left-90']) & set(vpose['right-180'])):
            if com==0:
                keyboard.press('left')
                keyboard.press('up')
            if com==1:
                keyboard.press('a')
                keyboard.press('w')

        elif val in vpose['right-90']:
            if com==0:
                keyboard.press('right')
            if com==1:
                keyboard.press('d')

        elif val in vpose['left-90']:
            if com==0:
                keyboard.press('left')
            if com==1:
                keyboard.press('a')

        elif val in list(set(vpose['right-180']) | set(vpose['left-180'])):
            if com==0:
                keyboard.press('up')
            if com==1:
                keyboard.press('w')

        else:
            if com==0:
                keyboard.release('right')
                keyboard.release('left')
                keyboard.release('up')
                keyboard.release('r')
            if com==1:
                keyboard.release('d')
                keyboard.release('a')
                keyboard.release('w')
                keyboard.release('r')

        return

    def check_arm_extension(landmarks, img_width):
        left_shoulder = landmarks[mpPose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[mpPose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[mpPose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks[mpPose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value]
        left_hip = landmarks[mpPose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mpPose.PoseLandmark.RIGHT_HIP.value]

        left_angle = calculate_angle(left_hip, left_shoulder, left_elbow)
        right_angle = calculate_angle(right_hip, right_shoulder, right_elbow)

        if com==3:
            theta = calculate_angle(right_hip, right_shoulder, right_wrist)
            if right_wrist.x > right_shoulder.x:
                theta = 360 - theta
            theta = (theta-7+360)%360
            theta -= 90
            theta_rad = -math.radians(theta)
            radius = 100
            pyautogui.moveTo(950 + radius*math.cos(theta_rad), 550 + radius*math.sin(theta_rad))
            
            if abs(left_wrist.y - left_shoulder.y) < 0.07 and abs(left_wrist.x - left_shoulder.x) < 0.12:
                print(theta, "dash")
                command(2)
            else:
                print(theta)
                command(0)
            
            # pyautogui.click()
            # print(theta)
            # current_position = pyautogui.position()
            # print(f"Current mouse position: {current_position}") # (950, 550)
            
            
            
        else:
            if abs(left_wrist.y - left_shoulder.y) < 0.07 and abs(left_wrist.x - left_shoulder.x) < 0.12 and abs(right_wrist.y - right_shoulder.y) < 0.07 and abs(right_wrist.x - right_shoulder.x) < 0.12 and abs(left_elbow.y - left_shoulder.y) < 0.07 and abs(left_elbow.x - left_shoulder.x) < 0.12 and abs(right_elbow.y - right_shoulder.y) < 0.07 and abs(right_elbow.x - right_shoulder.x) < 0.12:
                command(1)
                return "LR-CENTER"
            if abs(left_wrist.y - left_shoulder.y) < 0.07 and abs(left_wrist.x - left_shoulder.x) < 0.12:
                command(2)
                return "L-CENTER"
            if abs(right_wrist.y - right_shoulder.y) < 0.07 and abs(right_wrist.x - right_shoulder.x) < 0.12:
                command(3)
                return "R-CENTER"

            if angle[0] <= left_angle and left_angle < angle[1]:
                if angle[0] <= right_angle and right_angle < angle[1]:
                    command(4)
                    return "L-30 & R-30"
                if angle[1] <= right_angle and right_angle < angle[2]:
                    command(5)
                    return "L-30 & R-60"
                if angle[2] <= right_angle and right_angle < angle[3]:
                    command(6)
                    return "L-30 & R-90"
                if angle[3] <= right_angle and right_angle < angle[4]:
                    command(7)
                    return "L-30 & R-angle[4]"
                if angle[4] <= right_angle and right_angle < angle[5]:
                    command(8)
                    return "L-30 & R-180"

            if angle[1] <= left_angle and left_angle < angle[2]:
                if angle[0] <= right_angle and right_angle < angle[1]:
                    command(9)
                    return "L-60 & R-30"
                if angle[1] <= right_angle and right_angle < angle[2]:
                    command(10)
                    return "L-60 & R-60"
                if angle[2] <= right_angle and right_angle < angle[3]:
                    command(11)
                    return "L-60 & R-90"
                if angle[3] <= right_angle and right_angle < angle[4]:
                    command(12)
                    return "L-60 & R-120"
                if angle[4] <= right_angle and right_angle < angle[5]:
                    command(13)
                    return "L-60 & R-180"

            if angle[2] <= left_angle and left_angle < angle[3]:
                if angle[0] <= right_angle and right_angle < angle[1]:
                    command(14)
                    return "L-90 & R-30"
                if angle[1] <= right_angle and right_angle < angle[2]:
                    command(15)
                    return "L-90 & R-60"
                if angle[2] <= right_angle and right_angle < angle[3]:
                    command(16)
                    return "L-90 & R-90"
                if angle[3] <= right_angle and right_angle < angle[4]:
                    command(17)
                    return "L-90 & R-120"
                if angle[4] <= right_angle and right_angle < angle[5]:
                    command(18)
                    return "L-90 & R-180"

            if angle[3] <= left_angle and left_angle < angle[4]:
                if angle[0] <= right_angle and right_angle < angle[1]:
                    command(19)
                    return "L-120 & R-30"
                if angle[1] <= right_angle and right_angle < angle[2]:
                    command(20)
                    return "L-120 & R-60"
                if angle[2] <= right_angle and right_angle < angle[3]:
                    command(21)
                    return "L-120 & R-90"
                if angle[3] <= right_angle and right_angle < angle[4]:
                    command(22)
                    return "L-120 & R-120"
                if angle[4] <= right_angle and right_angle < angle[5]:
                    command(23)
                    return "L-120 & R-180"

            if angle[4] <= left_angle and left_angle < angle[5]:
                if angle[0] <= right_angle and right_angle < angle[1]:
                    command(24)
                    return "L-180 & R-30"
                if angle[1] <= right_angle and right_angle < angle[2]:
                    command(25)
                    return "L-180 & R-60"
                if angle[2] <= right_angle and right_angle < angle[3]:
                    command(26)
                    return "L-180 & R-90"
                if angle[3] <= right_angle and right_angle < angle[4]:
                    command(27)
                    return "L-180 & R-120"
                if angle[4] <= right_angle and right_angle < angle[5]:
                    command(28)
                    return "L-180 & R-180"

    while True:
        success, img = cap.read()
        if not success:
            print("웹캠을 열 수 없습니다.")
            break

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)

        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            landmarks = results.pose_landmarks.landmark
            direction = check_arm_extension(landmarks, img.shape[1])
            if direction:
                print(f"Camera {camera_id}: {direction}")

            for id, lm in enumerate(landmarks):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.imshow(f"Camera {camera_id}", cv2.flip(img, 1))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()