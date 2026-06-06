from funs import calcAngle
import math
stage = "----"
one_count = False
coords, angles = [], []
m, n = 0, 0
status = ""
color = (0, 0, 0)

########################## 姿勢檢測--棒式 ##########################
def isPlankCorrect(shoulders, hips, ankles, threshold=15):
    angle = calcAngle(shoulders, hips, ankles)
    if abs(angle-180)<threshold:
        status = "正確"
        color = (0, 255, 0)
    else:
        status = "不正確"
        color = (0, 0, 255)
    return angle, status, color

########################## 姿勢檢測--靠牆蹲 ##########################
def isWallsitCorrect(shoulders, hips, knees, ankles, threshold=20):
    angle1 = calcAngle(shoulders, hips, knees)
    angle2 = calcAngle(hips, knees, ankles)
    if abs(angle1-90)>threshold or abs(angle2-90)>threshold:
        status = "不正確"
        color = (0, 0, 255)
    else:
        status = "正確"
        color = (0, 255, 0)
    return angle1, angle2, status, color

########################## 姿勢檢測--二頭肌彎舉 ##########################
def isArmCorrect(shoulder, elbow, wrist, counts, thres1=150, thres2=60, thres3=0.1):
    global stage, one_count, coords, n, m, status, color
    angle = calcAngle(shoulder, elbow, wrist)
    if angle<=thres2:
        stage = "up"
    elif angle>=thres1 and stage=='up':
        stage = "down"
        counts += 1
    if not counts and not m:
        color = (0, 0, 0)
        status = ""
        m, n = 1, 0
        coords = []
    elif counts:
        m = 0
    if stage=="down" and counts and not n:
        one_count = True
    coords.append(shoulder)
    if one_count:
        coord_min = (min(coords, key=lambda x:x[0])[0],min(coords, key=lambda x:x[1])[1])
        coord_max = (max(coords, key=lambda x:x[0])[0],max(coords, key=lambda x:x[1])[1])
        if math.dist(coord_min, coord_max)>thres3:
            status = "Bad!"
            color = (0, 0, 255)
        else:
            status = "Good!"
            color = (0, 255, 0)
        n = 1
        coords = []
        one_count = False
    elif stage=="up":
        n = 0
        status = ""
    return angle, stage, status, color, counts

########################## 姿勢檢測--仰臥起坐 ##########################
def isSitupCorrect(shoulder, hip, knee, counts, thres_up=60, thres_down=115, thres3=60):
    global stage, one_count, angles, n, m, status, color
    angle = calcAngle(shoulder, hip, knee)
    if angle < thres_up:
        stage = "up"
    elif angle > thres_down and stage == "up":
        stage = "down"
        counts += 1
    if not counts and not m:
        color = (0, 0, 0)
        status = ""
        m, n = 1, 0
        angles = []
    elif counts:
        m = 0
    if stage=="down" and counts and not n:
        one_count = True
    angles.append(angle)
    if one_count:
        if min(angles)>thres3:
            status = "Bad!"
            color = (0, 0, 255)
        else:
            status = "Good!"
            color = (0, 255, 0)
        n = 1
        angles = []
        one_count = False
    elif stage=="up":
        n = 0
        status = ""
    return angle, stage, status, color, counts

########################## 姿勢檢測--深蹲 ##########################
def isSquatCorrect(shoulder, hip, knee, counts, thres_up=160, thres_down=105, thres3=90):
    global stage, one_count, angles, n, m, status, color
    angle = calcAngle(shoulder, hip, knee)
    if angle < thres_down:
        stage = "down"
    elif angle > thres_up and stage == "down":
        stage = "up"
        counts += 1
    if not counts and not m:
        color = (0, 0, 0)
        status = ""
        m, n = 1, 0
        angles = []
    elif counts:
        m = 0
    if stage=="up" and counts and not n:
        one_count = True
    angles.append(angle)
    if one_count:
        if min(angles)>thres3:
            status = "Bad!"
            color = (0, 0, 255)
        else:
            status = "Good!"
            color = (0, 255, 0)
        n = 1
        angles = []
        one_count = False
    elif stage=="down":
        n = 0
        status = ""
    return angle, stage, status, color, counts

########################## 姿勢檢測--伏地挺身 ##########################
def isPushupCorrect(shoulder, elbow, wrist, hip, knee, counts, thres_down=110, thres_up=160, thres3=20):
    global stage, one_count, angles, n, m, status, color
    arm_angle = calcAngle(shoulder, elbow, wrist)
    body_angle = calcAngle(shoulder, hip, knee)
    
    if arm_angle < thres_down:
        stage = "down"
    elif arm_angle > thres_up and stage == "down":
        stage = "up"
        counts += 1
    if not counts and not m:
        color = (0, 0, 0)
        status = ""
        m, n = 1, 0
        angles = []
    elif counts:
        m = 0
    if stage=="down" and counts and not n:
        one_count = True
    angles.append(body_angle)
    if one_count:
        if 180-min(angles)>thres3:
            status = "Bad!"
            color = (0, 0, 255)
        else:
            status = "Good!"
            color = (0, 255, 0)
        n = 1
        angles = []
        one_count = False
    elif stage=="up":
        n = 0
        status = ""
    return arm_angle, stage, status, color, counts