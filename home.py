import cv2
import time
import json
from flask import Blueprint, Response, redirect, url_for, render_template, jsonify, g, request
from decimal import Decimal, ROUND_UP
from workout import Plank, Dumbbell, Situp, Squat, Pushup, Wallsit, getInfo
from dbfuns import get_db

bp = Blueprint('home', __name__, url_prefix='/home')
total_duration = 0
cam_number = 1
cam_resol = None
current_pose = None
camera = None

@bp.before_request
def check_login():
    if g.user is None:
        return redirect(url_for('auth.login'))
    return

@bp.route("/")
def welcome():
    return render_template("home.html")

@bp.route("/plank")
def plank():
    return render_template("plank.html")
@bp.route("/dumbbell")
def dumbbell():
    return render_template("dumbbell.html")
@bp.route("/wallsit")
def wallsit():
    return render_template("wallsit.html")
@bp.route("/squat")
def squat():
    return render_template("squat.html")
@bp.route("/situp")
def situp():
    return render_template("situp.html")
@bp.route("/pushup")
def pushup():
    return render_template("pushup.html")

@bp.route("/start")
def start():
    global cam_resol, camera
    camera = cv2.VideoCapture(cam_number)
    if cam_resol is None:
        common_resolutions = [(640, 480), (800, 600), (1024, 768),
                            (1280, 720), (1280, 1024), (1920, 1080)]
        supported_resolutions = []
        for w, h in common_resolutions:
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, w)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
            actual_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
            actual_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
            if actual_width==w and actual_height==h:
                supported_resolutions.append((int(actual_width), int(actual_height)))
        cam_resol = max(supported_resolutions)
    camera.release()
    return jsonify(success=True)

@bp.route("/stop")
def stop():
    global total_duration, camera
    end_time = time.time()
    db = get_db()
    if camera:
        camera.release()
    camera = None
    infos = getInfo()
    if infos['start_time']!=0:
        if infos["status"] and len(infos["status"])>infos["frames"]:
            infos["status"] = infos["status"][:infos["frames"]]
        total_duration = float(Decimal(end_time-infos['start_time']).quantize(Decimal('0.0'), rounding=ROUND_UP))
        status = json.dumps(infos['status'])
        match current_pose:
            case 'plank' | 'wallsit':
                db.execute(
                    '''
                    INSERT INTO records
                    (userid, pose, workoutDuration, status)
                    VALUES ((SELECT id FROM user WHERE username=?), ?, ?, ?)
                    ''',
                    (g.user['username'], current_pose, total_duration, status)
                    )
                db.commit()
                return jsonify(success=True,
                            time=total_duration,
                            systemlog="紀錄已更新:D")
            case _:
                counts = json.dumps(infos['counts'])
                db.execute(
                    '''
                    INSERT INTO records
                    (userid, pose, workoutDuration, status, counts)
                    VALUES ((SELECT id FROM user WHERE username=?), ?, ?, ?, ?)
                    ''',
                    (g.user['username'], current_pose, total_duration, status, counts)
                    )
                db.commit()
                return jsonify(success=True,
                            time=total_duration,
                            systemlog=f'一共 {infos["counts"][-1]}下 紀錄已更新:D')
    return jsonify(success=True,
                   time=0.0,
                   systemlog=f'無紀錄')

@bp.route("/video_feed")
def video_feed():
    print('開始偵測...')
    match current_pose:
        case 'plank':
            return Response(response=Plank(cam_number, cam_resol),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
        case 'wallsit':
            return Response(response=Wallsit(cam_number, cam_resol),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
        case 'dumbbell':
            return Response(response=Dumbbell(cam_number, cam_resol),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
        case 'situp':
            return Response(response=Situp(cam_number, cam_resol),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
        case 'squat':
            return Response(response=Squat(cam_number, cam_resol),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
        case 'pushup':
            return Response(response=Pushup(cam_number, cam_resol),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

@bp.route('/send_pose', methods=['POST'])
def send_pose():
    global current_pose
    data = request.get_json()
    current_pose = data.get('pose')
    print(f'Received pose: {current_pose}')
    return jsonify({'status': 'success'})
