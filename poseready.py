import cv2, math
import numpy as np
import mediapipe as mp
mp_pose = mp.solutions.pose

########################## 素體人偶 ##########################
def drawPose(landmarks, frame, arm=None, body=90, leg=None, alpha=148.5):
    overlay = np.array(frame)
    h, w = overlay.shape[:2]
    x_face, y_face = landmarks[mp_pose.PoseLandmark(0).value].x, \
            landmarks[mp_pose.PoseLandmark(0).value].y
    if landmarks[mp_pose.PoseLandmark(11).value].visibility > landmarks[mp_pose.PoseLandmark(10).value].visibility:
    x_shoulder, y_shoulder = landmarks[mp_pose.PoseLandmark(11).value].x, \
            landmarks[mp_pose.PoseLandmark(11).value].y
    x_elbow, y_elbow = landmarks[mp_pose.PoseLandmark(13).value].x, \
            landmarks[mp_pose.PoseLandmark(13).value].y
    x_wrist, y_wrist = landmarks[mp_pose.PoseLandmark(15).value].x, \
            landmarks[mp_pose.PoseLandmark(15).value].y
    x_hip, y_hip = landmarks[mp_pose.PoseLandmark(23).value].x, \
            landmarks[mp_pose.PoseLandmark(23).value].y
    x_knee, y_knee = landmarks[mp_pose.PoseLandmark(25).value].x, \
            landmarks[mp_pose.PoseLandmark(25).value].y
    x_foot, y_foot = landmarks[mp_pose.PoseLandmark(27).value].x, \
            landmarks[mp_pose.PoseLandmark(27).value].y
    if body is not None:
        x1, y1 = x_hip*w, y_hip*h
        x2, y2 = x_shoulder*w, y_shoulder*h
        r = math.dist((x1, y1),(x2, y2))/2
        x_body = int(x1+r*math.cos(math.radians(body)))
        y_body = int(y1-r*math.sin(math.radians(body)))
        r = int(r+30*h/480)
        x3, y3 = x_face*w, y_face*h
        x4, y4 = landmarks[mp_pose.PoseLandmark(12).value].x*w,\
                 landmarks[mp_pose.PoseLandmark(12).value].y*h
        l1 = int(math.dist((x1, y1),(x2, y2)))
        l2 = int(math.dist((x3,y3), ((x2+x4)/2,(y2+y4)/2)))
        x_head = int(x_hip*w+l1*math.cos(math.radians(body))\
                     +l2*math.cos(math.radians(body)))
        y_head = int(y1-l1*math.sin(math.radians(body))\
                     -l2*math.sin(math.radians(body)))
        cv2.ellipse(overlay, (x_body,y_body),
                    (r, int(r/3)),
                    -body,
                    0, 360, (173, 203, 248, alpha), -1, cv2.LINE_AA)
        cv2.circle(overlay, (x_head, y_head),
                   l2,
                   (173, 203, 248, alpha), -1, cv2.LINE_AA)
        cv2.ellipse(overlay, (x_body,y_body),
                    (r, int(r/3)),
                    -body,
                    0, 360, (0, 0, 0, alpha), int(2*h/480), cv2.LINE_AA)
        cv2.circle(overlay, (x_head, y_head),
                   l2,
                   (0, 0, 0, alpha), int(2*h/480), cv2.LINE_AA)
    if leg is not None:
        x1, y1 = x_hip*w, y_hip*h
        x2, y2 = x_knee*w, y_knee*h
        x3, y3 = x_foot*w, y_foot*h
        l1 = math.dist((x1, y1), (x2, y2))/2
        l2 = math.dist((x2, y2), (x3, y3))/2
        x_thigh = int(x1+l1*math.cos(math.radians(leg[0])))
        y_thigh = int(y1+l1*math.sin(math.radians(-leg[0])))
        x_calf = int(x1+2*l1*math.cos(math.radians(leg[0]))\
                     +l2*math.cos(math.radians(leg[1])))
        y_calf = int(y1+2*l1*math.sin(math.radians(-leg[0]))\
                     +l2*math.sin(math.radians(-leg[1])))
        r_thigh = l1+30*h/480
        r_calf = l2+30*h/480
        cv2.ellipse(overlay, (x_thigh, y_thigh),
                    (int(r_thigh), int(r_thigh/2.5)),
                    -leg[0],
                    0, 360, (173, 203, 248, alpha), -1, cv2.LINE_AA)
        cv2.ellipse(overlay, (x_calf, y_calf),
                    (int(r_calf), int(r_calf/3)),
                    -leg[1],
                    0, 360, (173, 203, 248, alpha), -1, cv2.LINE_AA)
        cv2.ellipse(overlay, (x_thigh, y_thigh),
                    (int(r_thigh), int(r_thigh/2.5)),
                    -leg[0],
                    0, 360, (0, 0, 0, alpha), int(2*h/480), cv2.LINE_AA)
        cv2.ellipse(overlay, (x_calf, y_calf),
                    (int(r_calf), int(r_calf/3)),
                    -leg[1],
                    0, 360, (0, 0, 0, alpha), int(2*h/480), cv2.LINE_AA)
    if arm is not None:
        x0, y0 = x_hip*w, y_hip*h
        x1, y1 = x_shoulder*w, y_shoulder*h
        x2, y2 = x_elbow*w, y_elbow*h
        x3, y3 = x_wrist*w, y_wrist*h
        l0 = math.dist((x0, y0), (x1, y1))
        l1 = math.dist((x1, y1), (x2, y2))/2
        l2 = math.dist((x2, y2), (x3, y3))/2
        x_upperarm = int(x0+l0*math.cos(math.radians(body))\
                         +l1*math.cos(math.radians(-arm[0])))
        y_upperarm = int(y0-l0*math.sin(math.radians(body))\
                         +l1*math.sin(math.radians(-arm[0])))
        x_forearm = int(x0+l0*math.cos(math.radians(body))\
                        +2*l1*math.cos(math.radians(-arm[0]))\
                        +l2*math.cos(math.radians(-arm[1])))
        y_forearm = int(y0-l0*math.sin(math.radians(body))\
                        +2*l1*math.sin(math.radians(-arm[0]))\
                        +l2*math.sin(math.radians(-arm[1])))
        r_upperarm = l1+30*h/480
        r_forearm = l2+25*h/480
        cv2.ellipse(overlay, (x_upperarm, y_upperarm),
                    (int(r_upperarm), int(r_upperarm/2.5)),
                    -arm[0],
                    0, 360, (173, 203, 248, alpha), -1, cv2.LINE_AA)
        cv2.ellipse(overlay, (x_forearm, y_forearm),
                    (int(r_forearm), int(r_forearm/3)),
                    -arm[1],
                    0, 360, (173, 203, 248, alpha), -1, cv2.LINE_AA)
        cv2.ellipse(overlay, (x_upperarm, y_upperarm),
                    (int(r_upperarm), int(r_upperarm/2.5)),
                    -arm[0],
                    0, 360, (0, 0, 0, alpha), int(2*h/480), cv2.LINE_AA)
        cv2.ellipse(overlay, (x_forearm, y_forearm),
                    (int(r_forearm), int(r_forearm/3)),
                    -arm[1],
                    0, 360, (0, 0, 0, alpha), int(2*h/480), cv2.LINE_AA)
    return overlay

########################## 實際肢體 ##########################
def drawBody(landmarks, frame, arm=False, body=False, leg=False, alpha=255):
    overlay = np.array(frame)
    h, w = overlay.shape[:2]
    x_shoulder, y_shoulder = landmarks[mp_pose.PoseLandmark(11).value].x, \
            landmarks[mp_pose.PoseLandmark(11).value].y
    x_elbow, y_elbow = landmarks[mp_pose.PoseLandmark(13).value].x, \
            landmarks[mp_pose.PoseLandmark(13).value].y
    x_wrist, y_wrist = landmarks[mp_pose.PoseLandmark(15).value].x, \
            landmarks[mp_pose.PoseLandmark(15).value].y
    x_hip, y_hip = landmarks[mp_pose.PoseLandmark(23).value].x, \
            landmarks[mp_pose.PoseLandmark(23).value].y
    x_knee, y_knee = landmarks[mp_pose.PoseLandmark(25).value].x, \
            landmarks[mp_pose.PoseLandmark(25).value].y
    x_foot, y_foot = landmarks[mp_pose.PoseLandmark(27).value].x, \
            landmarks[mp_pose.PoseLandmark(27).value].y
    points = []
    if body:
        cv2.line(overlay,
                 (int(x_shoulder*w), int(y_shoulder*h)),
                 (int(x_hip*w), int(y_hip*h)),
                 (0, 0, 255, alpha), int(10*h/480))
        points.extend([0,11,23])
    if leg:
        cv2.line(overlay,
                 (int(x_hip*w), int(y_hip*h)),
                 (int(x_knee*w), int(y_knee*h)),
                 (0, 0, 255, alpha), int(10*h/480))
        cv2.line(overlay,
                 (int(x_knee*w), int(y_knee*h)),
                 (int(x_foot*w), int(y_foot*h)),
                 (0, 0, 255, alpha), int(10*h/480))
        points.extend([25,27])
    if arm:
        cv2.line(overlay,
                 (int(x_shoulder*w), int(y_shoulder*h)),
                 (int(x_elbow*w), int(y_elbow*h)),
                 (0, 0, 255, alpha), int(10*h/480))
        cv2.line(overlay,
                 (int(x_elbow*w), int(y_elbow*h)),
                 (int(x_wrist*w), int(y_wrist*h)),
                 (0, 0, 255, alpha), int(10*h/480))
        points.extend([13,15])
    for i in points:
        part = landmarks[mp_pose.PoseLandmark(i).value]
        x, y = int(part.x*w), int(part.y*h)
        if x<w and y<h:
            cv2.circle(overlay, (x, y),
                    int(10*h/480),
                    (255, 255, 255, alpha), -1, cv2.LINE_AA)
            cv2.circle(overlay, (x, y),
                    int(10*h/480),
                    (0, 0, 255, alpha), int(2.5*h/480), cv2.LINE_AA)
    return overlay