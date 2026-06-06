import cv2, math
import numpy as np
from PIL import Image
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)


########################## 確認支援解析度 ##########################
def getResol(cam_num=0):
    cap = cv2.VideoCapture(cam_num)  # 開啟攝影機
    common_resolutions = [
        (640, 480),
        (800, 600),
        (1024, 768),
        (1280, 720),
        (1280, 1024),
        (1920, 1080),
    ]
    supported_resolutions = []
    for w, h in common_resolutions:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        if actual_width == w and actual_height == h:
            supported_resolutions.append((int(actual_width), int(actual_height)))
    cap.release()
    return max(supported_resolutions)


########################## mediapipe疊圖 ##########################
def poseProcess(frame):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)
    return results


########################## 反轉透明度 ##########################
def invert_opacity(image):
    r, g, b, a = image.split()
    inverted_alpha = a.point(lambda p: 255 - p)
    inverted_image = Image.merge("RGBA", (r, g, b, inverted_alpha))
    return inverted_image


########################## 預備圖的透明區域 ##########################
def checkAlpha(landmarks, frame, alpha_channel, points):
    for part in points:
        x = landmarks[mp_pose.PoseLandmark(part).value].x
        y = landmarks[mp_pose.PoseLandmark(part).value].y
        if x < 1 and y < 1:
            a = alpha_channel[
                math.floor(y * frame.size[1]), math.floor(x * frame.size[0])
            ]
        else:
            a = 0
        if x >= 1 or y >= 1 or not a:
            return True
    return False


########################## 計算夾角 ##########################
def calcAngle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    # arctan2(y,x)：(1,0)到(x,y)的逆時針夾角
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
        a[1] - b[1], a[0] - b[0]
    )
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle
