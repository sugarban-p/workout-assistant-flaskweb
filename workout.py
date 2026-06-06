import time, cv2, math
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import mediapipe as mp
mp_pose = mp.solutions.pose
from funs import poseProcess, checkAlpha
from posecheck import isPlankCorrect, isWallsitCorrect, isPushupCorrect, isSquatCorrect, isSitupCorrect, isArmCorrect 
from poseready import drawPose, drawBody
font_path = "./SourceHanSansSC-Medium.otf"
stream_info = {}
camera = None

def Plank(cam_num, cam_resol):
    global camera
    stream_info["start_time"] = 0
    font = ImageFont.truetype(font_path, int(28*cam_resol[1]/480))
    camera = cv2.VideoCapture(cam_num)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_resol[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_resol[1])
    pose_set = Image.open('./static/frame.png')
    pose_set = pose_set.resize(cam_resol, Image.LANCZOS).convert("RGBA")
    points = [0,11,23,25,27,13,15]
    preparing = True
    stream_info["status"] = []
    stream_info["frames"] = 0   # 幀數
    while camera is not None and camera.isOpened():
        success, frame = camera.read()
        if not success:
            break
        else:
            if not cam_num:
                frame = cv2.flip(frame, 1)
            image = frame.copy()
            results = poseProcess(image)
            if preparing:
                if results.pose_landmarks is not None:
                    new_pose_set = drawPose(results.pose_landmarks.landmark, pose_set,
                                            body=170, leg=[-10,-10], arm=[-90,180])
                    alpha_channel = new_pose_set[:, :, 3]/255.0
                    image = Image.alpha_composite(Image.fromarray(image).convert("RGBA"), Image.fromarray(new_pose_set))
                    preparing = checkAlpha(results.pose_landmarks.landmark, image, alpha_channel, points)
                    image = drawBody(results.pose_landmarks.landmark, image.convert("RGBA"),
                                         body=True, leg=True, arm=True)
            else:
                time0 = time.time()
                if results.pose_landmarks is not None:                                          #####
                    image = drawBody(results.pose_landmarks.landmark, Image.fromarray(image).convert("RGBA"),#####
                                     body=True, leg=True, arm=True)                                       #####
                cv2.rectangle(image,
                              (int(cam_resol[0]*0.015),int(cam_resol[1]*0.05)),
                              (int(cam_resol[0]*0.3),int(cam_resol[1]*0.2)),
                              (0, 0, 0), -1)
                image = Image.fromarray(image)
                if not stream_info["frames"]:
                    stream_info["start_time"] = time0
                draw = ImageDraw.Draw(image)
                try:
                    landmarks = results.pose_landmarks.landmark
                    shoulders = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    hips = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    ankles = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                    # 檢查姿勢是否正確
                    angle, status, color = isPlankCorrect(shoulders, hips, ankles)
                    stream_info["status"].append("true") if status=="正確" else stream_info["status"].append("false")
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.93)),
                                f'{math.floor(angle*10)/10.0}',
                                font=ImageFont.truetype(font_path, int(12*cam_resol[1]/480)),
                                fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.05)),
                                f'姿勢: {status}',
                                font=font, fill=color)
                except:
                    stream_info["status"].append("None")
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.93)),
                                f'----',
                                font=ImageFont.truetype(font_path, int(12*(cam_resol[1]/480))),
                                fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.05)),
                                f'姿勢: ----',
                                font=font, fill=(255, 255, 255))
                draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.12)),
                            f'時間: {(time0-stream_info["start_time"]):.1f}s',
                            font=font, fill=(255, 255, 255))
                stream_info["frames"] += 1
            image = np.array(image)
            _, buffer = cv2.imencode('.jpg', image)
            image = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

def Dumbbell(cam_num, cam_resol):
    global camera
    stream_info["start_time"] = 0
    font = ImageFont.truetype(font_path, int(28*cam_resol[1]/480))
    camera = cv2.VideoCapture(cam_num)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_resol[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_resol[1])
    pose_set = Image.open('./static/frame.png')
    pose_set = pose_set.resize(cam_resol, Image.LANCZOS).convert("RGBA")
    points = [0,11,23,13,15]
    preparing = True
    stream_info["status"] = []
    stream_info["frames"] = 0   # 幀數
    stream_info["counts"] = []
    counts, stage, status = 0, '----', ''
    while camera is not None and camera.isOpened():
        success, frame = camera.read()
        if not success:
            break
        else:
            if not cam_num:
                frame = cv2.flip(frame, 1)
            image = frame.copy()
            results = poseProcess(image)
            if preparing:
                if results.pose_landmarks is not None:
                    new_pose_set = drawPose(results.pose_landmarks.landmark, pose_set,
                                            body=90, arm=[-90,-90])
                    alpha_channel = new_pose_set[:, :, 3]/255.0
                    image = Image.alpha_composite(Image.fromarray(image).convert("RGBA"), Image.fromarray(new_pose_set))
                    preparing = checkAlpha(results.pose_landmarks.landmark, image, alpha_channel, points)
                    image = drawBody(results.pose_landmarks.landmark, image.convert("RGBA"),
                                         body=True, arm=True)
            else:
                time0 = time.time()
                if results.pose_landmarks is not None:                                          #####
                    image = drawBody(results.pose_landmarks.landmark, Image.fromarray(image).convert("RGBA"),#####
                                     body=True, arm=True)                                       #####
                cv2.rectangle(image,
                              (int(cam_resol[0]*0.015),int(cam_resol[1]*0.05)),
                              (int(cam_resol[0]*0.46),int(cam_resol[1]*0.2)),
                              (0, 0, 0), -1)
                image = Image.fromarray(image)
                if not stream_info["frames"]:
                    stream_info["start_time"] = time0
                draw = ImageDraw.Draw(image)
                try:
                    landmarks = results.pose_landmarks.landmark
                    shoulders = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    # 檢查姿勢是否正確
                    angle, stage, status, color, counts = isArmCorrect(shoulders, elbow, wrist, counts)
                    if status=="Good!":
                        stream_info["status"].append("true")
                    elif not status:
                        stream_info["status"].append("None")
                    else:
                        stream_info["status"].append("false")
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.93)),
                                f'{math.floor(angle*10)/10.0}',
                                font=ImageFont.truetype(font_path, 12),
                                fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.05)),
                                f'{counts} 下',
                                font=font, fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.15),int(cam_resol[1]*0.05)),
                                stage,
                                font=font, fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.3),int(cam_resol[1]*0.05)),
                                status,
                                font=font, fill=color)
                except:
                    stream_info["status"].append("None")
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.93)),
                                f'----',
                                font=ImageFont.truetype(font_path, 12),
                                fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.05)),
                                f'{counts} 下',
                                font=font, fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.15),int(cam_resol[1]*0.05)),
                                stage,
                                font=font, fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.3),int(cam_resol[1]*0.05)),
                                status,
                                font=font, fill=color)
                draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.12)),
                            f'時間: {(time0-stream_info["start_time"]):.1f}s',
                            font=font, fill=(255, 255, 255))
                stream_info["counts"].append(counts)
                stream_info["frames"] += 1
            image = np.array(image)
            _, buffer = cv2.imencode('.jpg', image)
            image = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

def Wallsit(cam_num, cam_resol):
    global camera
    stream_info["start_time"] = 0
    font = ImageFont.truetype(font_path, int(28*cam_resol[1]/480))
    camera = cv2.VideoCapture(cam_num)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_resol[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_resol[1])
    pose_set = Image.open('./static/frame.png')
    pose_set = pose_set.resize(cam_resol, Image.LANCZOS).convert("RGBA")
    points = [0,11,23,25,27]
    preparing = True
    stream_info["status"] = []
    stream_info["frames"] = 0   # 幀數
    while camera is not None and camera.isOpened():
        success, frame = camera.read()
        if not success:
            break
        else:
            if not cam_num:
                frame = cv2.flip(frame, 1)
            image = frame.copy()
            results = poseProcess(image)
            if preparing:
                if results.pose_landmarks is not None:
                    new_pose_set = drawPose(results.pose_landmarks.landmark, pose_set,
                                            body=90, leg=[180,-90])
                    alpha_channel = new_pose_set[:, :, 3]/255.0
                    image = Image.alpha_composite(Image.fromarray(image).convert("RGBA"), Image.fromarray(new_pose_set))
                    preparing = checkAlpha(results.pose_landmarks.landmark, image, alpha_channel, points)
                    image = drawBody(results.pose_landmarks.landmark, image.convert("RGBA"),
                                         body=True, leg=True)
            else:
                time0 = time.time()
                if results.pose_landmarks is not None:                                          #####
                    image = drawBody(results.pose_landmarks.landmark, Image.fromarray(image).convert("RGBA"),#####
                                     body=True, leg=True)                                       #####
                cv2.rectangle(image,
                              (int(cam_resol[0]*0.015),int(cam_resol[1]*0.05)),
                              (int(cam_resol[0]*0.3),int(cam_resol[1]*0.2)),
                              (0, 0, 0), -1)
                image = Image.fromarray(image)
                if not stream_info["frames"]:
                    stream_info["start_time"] = time0
                draw = ImageDraw.Draw(image)
                try:
                    landmarks = results.pose_landmarks.landmark
                    shoulders = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    hips = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    knees = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    ankles = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                    # 檢查姿勢是否正確
                    angle1, angle2, status, color = isWallsitCorrect(shoulders, hips, knees, ankles)
                    stream_info["status"].append("true") if status=="正確" else stream_info["status"].append("false")
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.93)),
                                f'hip-{math.floor(angle1*10)/10.0}, knee-{math.floor(angle2*10)/10.0}',
                                font=ImageFont.truetype(font_path, int(12*cam_resol[1]/480)),
                                fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.05)),
                                f'姿勢: {status}',
                                font=font, fill=color)
                except:
                    stream_info["status"].append("None")
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.93)),
                                f'----',
                                font=ImageFont.truetype(font_path, int(12*(cam_resol[1]/480))),
                                fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.05)),
                                f'姿勢: ----',
                                font=font, fill=(255, 255, 255))
                draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.12)),
                            f'時間: {(time0-stream_info["start_time"]):.1f}s',
                            font=font, fill=(255, 255, 255))
                stream_info["frames"] += 1
            image = np.array(image)
            _, buffer = cv2.imencode('.jpg', image)
            image = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

def Situp(cam_num, cam_resol):
    global camera
    stream_info["start_time"] = 0
    font = ImageFont.truetype(font_path, int(28*cam_resol[1]/480))
    camera = cv2.VideoCapture(cam_num)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_resol[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_resol[1])
    pose_set = Image.open('./static/frame.png')
    pose_set = pose_set.resize(cam_resol, Image.LANCZOS).convert("RGBA")
    points = [0,11,23,25,27,13,15]
    preparing = True
    stream_info["status"] = []
    stream_info["frames"] = 0   # 幀數
    stream_info["counts"] = []
    counts, stage, status = 0, '----', ''
    while camera is not None and camera.isOpened():
        success, frame = camera.read()
        if not success:
            break
        else:
            if not cam_num:
                frame = cv2.flip(frame, 1)
            image = frame.copy()
            results = poseProcess(image)
            if preparing:
                if results.pose_landmarks is not None:
                    new_pose_set = drawPose(results.pose_landmarks.landmark, pose_set,
                                            body=180, leg=[45,-45], arm=[100,-120])
                    alpha_channel = new_pose_set[:, :, 3]/255.0
                    image = Image.alpha_composite(Image.fromarray(image).convert("RGBA"), Image.fromarray(new_pose_set))
                    preparing = checkAlpha(results.pose_landmarks.landmark, image, alpha_channel, points)
                    image = drawBody(results.pose_landmarks.landmark, image.convert("RGBA"),
                                         body=True, leg=True, arm=True)
            else:
                time0 = time.time()
                if results.pose_landmarks is not None:                                          #####
                    image = drawBody(results.pose_landmarks.landmark, Image.fromarray(image).convert("RGBA"),#####
                                     body=True, leg=True, arm=True)                                       #####
                cv2.rectangle(image,
                              (int(cam_resol[0]*0.015),int(cam_resol[1]*0.05)),
                              (int(cam_resol[0]*0.46),int(cam_resol[1]*0.2)),
                              (0, 0, 0), -1)
                image = Image.fromarray(image)
                if not stream_info["frames"]:
                    stream_info["start_time"] = time0
                draw = ImageDraw.Draw(image)
                try:
                    landmarks = results.pose_landmarks.landmark
                    shoulders = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    # 檢查姿勢是否正確
                    angle, stage, status, color, counts = isSitupCorrect(shoulders, hip, knee, counts)
                    if status=="Good!":
                        stream_info["status"].append("true")
                    elif not status:
                        stream_info["status"].append("None")
                    else:
                        stream_info["status"].append("false")
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.93)),
                                f'{math.floor(angle*10)/10.0}',
                                font=ImageFont.truetype(font_path, 12),
                                fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.05)),
                                f'{counts} 下',
                                font=font, fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.15),int(cam_resol[1]*0.05)),
                                stage,
                                font=font, fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.3),int(cam_resol[1]*0.05)),
                                status,
                                font=font, fill=color)
                except:
                    stream_info["status"].append("None")
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.93)),
                                f'----',
                                font=ImageFont.truetype(font_path, 12),
                                fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.05)),
                                f'{counts} 下',
                                font=font, fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.15),int(cam_resol[1]*0.05)),
                                stage,
                                font=font, fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.3),int(cam_resol[1]*0.05)),
                                status,
                                font=font, fill=color)
                draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.12)),
                            f'時間: {(time0-stream_info["start_time"]):.1f}s',
                            font=font, fill=(255, 255, 255))
                stream_info["counts"].append(counts)
                stream_info["frames"] += 1
            image = np.array(image)
            _, buffer = cv2.imencode('.jpg', image)
            image = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

def Squat(cam_num, cam_resol):
    global camera
    stream_info["start_time"] = 0
    font = ImageFont.truetype(font_path, int(28*cam_resol[1]/480))
    camera = cv2.VideoCapture(cam_num)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_resol[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_resol[1])
    pose_set = Image.open('./static/frame.png')
    pose_set = pose_set.resize(cam_resol, Image.LANCZOS).convert("RGBA")
    points = [0,11,23,25,27,13,15]
    preparing = True
    stream_info["status"] = []
    stream_info["frames"] = 0   # 幀數
    stream_info["counts"] = []
    counts, stage, status = 0, '----', ''
    while camera is not None and camera.isOpened():
        success, frame = camera.read()
        if not success:
            break
        else:
            if not cam_num:
                frame = cv2.flip(frame, 1)
            image = frame.copy()
            results = poseProcess(image)
            if preparing:
                if results.pose_landmarks is not None:
                    new_pose_set = drawPose(results.pose_landmarks.landmark, pose_set,
                                            body=90, leg=[-90,-90], arm=[-120,120])
                    alpha_channel = new_pose_set[:, :, 3]/255.0
                    image = Image.alpha_composite(Image.fromarray(image).convert("RGBA"), Image.fromarray(new_pose_set))
                    preparing = checkAlpha(results.pose_landmarks.landmark, image, alpha_channel, points)
                    image = drawBody(results.pose_landmarks.landmark, image.convert("RGBA"),
                                         body=True, leg=True, arm=True)
            else:
                time0 = time.time()
                if results.pose_landmarks is not None:                                          #####
                    image = drawBody(results.pose_landmarks.landmark, Image.fromarray(image).convert("RGBA"),#####
                                     body=True, leg=True, arm=True)                                       #####
                cv2.rectangle(image,
                              (int(cam_resol[0]*0.015),int(cam_resol[1]*0.05)),
                              (int(cam_resol[0]*0.46),int(cam_resol[1]*0.2)),
                              (0, 0, 0), -1)
                image = Image.fromarray(image)
                if not stream_info["frames"]:
                    stream_info["start_time"] = time0
                draw = ImageDraw.Draw(image)
                try:
                    landmarks = results.pose_landmarks.landmark
                    shoulders = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    # 檢查姿勢是否正確
                    angle, stage, status, color, counts = isSquatCorrect(shoulders, hip, knee, counts)
                    if status=="Good!":
                        stream_info["status"].append("true")
                    elif not status:
                        stream_info["status"].append("None")
                    else:
                        stream_info["status"].append("false")
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.93)),
                                f'{math.floor(angle*10)/10.0}',
                                font=ImageFont.truetype(font_path, 12),
                                fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.05)),
                                f'{counts} 下',
                                font=font, fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.15),int(cam_resol[1]*0.05)),
                                stage,
                                font=font, fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.3),int(cam_resol[1]*0.05)),
                                status,
                                font=font, fill=color)
                except:
                    stream_info["status"].append("None")
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.93)),
                                f'----',
                                font=ImageFont.truetype(font_path, 12),
                                fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.05)),
                                f'{counts} 下',
                                font=font, fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.15),int(cam_resol[1]*0.05)),
                                stage,
                                font=font, fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.3),int(cam_resol[1]*0.05)),
                                status,
                                font=font, fill=color)
                draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.12)),
                            f'時間: {(time0-stream_info["start_time"]):.1f}s',
                            font=font, fill=(255, 255, 255))
                stream_info["counts"].append(counts)
                stream_info["frames"] += 1
            image = np.array(image)
            _, buffer = cv2.imencode('.jpg', image)
            image = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
            
def Pushup(cam_num, cam_resol):
    global camera
    stream_info["start_time"] = 0
    font = ImageFont.truetype(font_path, int(28*cam_resol[1]/480))
    camera = cv2.VideoCapture(cam_num)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_resol[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_resol[1])
    pose_set = Image.open('./static/frame.png')
    pose_set = pose_set.resize(cam_resol, Image.LANCZOS).convert("RGBA")
    points = [0,11,23,25,27,13,15]
    preparing = True
    stream_info["status"] = []
    stream_info["frames"] = 0   # 幀數
    stream_info["counts"] = []
    counts, stage, status = 0, '----', ''
    while camera is not None and camera.isOpened():
        success, frame = camera.read()
        if not success:
            break
        else:
            if not cam_num:
                frame = cv2.flip(frame, 1)
            image = frame.copy()
            results = poseProcess(image)
            if preparing:
                if results.pose_landmarks is not None:
                    new_pose_set = drawPose(results.pose_landmarks.landmark, pose_set,
                                            body=160, leg=[-20,-20], arm=[-90,-90])
                    alpha_channel = new_pose_set[:, :, 3]/255.0
                    image = Image.alpha_composite(Image.fromarray(image).convert("RGBA"), Image.fromarray(new_pose_set))
                    preparing = checkAlpha(results.pose_landmarks.landmark, image, alpha_channel, points)
                    image = drawBody(results.pose_landmarks.landmark, image.convert("RGBA"),
                                         body=True, leg=True, arm=True)
            else:
                time0 = time.time()
                if results.pose_landmarks is not None:                                          #####
                    image = drawBody(results.pose_landmarks.landmark, Image.fromarray(image).convert("RGBA"),#####
                                     body=True, leg=True, arm=True)                                       #####
                cv2.rectangle(image,
                              (int(cam_resol[0]*0.015),int(cam_resol[1]*0.05)),
                              (int(cam_resol[0]*0.46),int(cam_resol[1]*0.2)),
                              (0, 0, 0), -1)
                image = Image.fromarray(image)
                if not stream_info["frames"]:
                    stream_info["start_time"] = time0
                draw = ImageDraw.Draw(image)
                try:
                    landmarks = results.pose_landmarks.landmark
                    shoulders = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    knees = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    # 檢查姿勢是否正確
                    angle, stage, status, color, counts = isPushupCorrect(shoulders, elbow, wrist, hip, knees, counts)
                    if status=="Good!":
                        stream_info["status"].append("true")
                    elif not status:
                        stream_info["status"].append("None")
                    else:
                        stream_info["status"].append("false")
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.93)),
                                f'{math.floor(angle*10)/10.0}',
                                font=ImageFont.truetype(font_path, 12),
                                fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.05)),
                                f'{counts} 下',
                                font=font, fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.15),int(cam_resol[1]*0.05)),
                                stage,
                                font=font, fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.3),int(cam_resol[1]*0.05)),
                                status,
                                font=font, fill=color)
                except:
                    stream_info["status"].append("None")
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.93)),
                                f'----',
                                font=ImageFont.truetype(font_path, 12),
                                fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.05)),
                                f'{counts} 下',
                                font=font, fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.15),int(cam_resol[1]*0.05)),
                                stage,
                                font=font, fill=(255, 255, 255))
                    draw.text((int(cam_resol[0]*0.3),int(cam_resol[1]*0.05)),
                                status,
                                font=font, fill=color)
                draw.text((int(cam_resol[0]*0.016),int(cam_resol[1]*0.12)),
                            f'時間: {(time0-stream_info["start_time"]):.1f}s',
                            font=font, fill=(255, 255, 255))
                stream_info["counts"].append(counts)
                stream_info["frames"] += 1
            image = np.array(image)
            _, buffer = cv2.imencode('.jpg', image)
            image = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

########################## 取得 sendFrame() 內部變數 ##########################
def getInfo():
    global camera
    camera.release()
    camera = None
    return stream_info