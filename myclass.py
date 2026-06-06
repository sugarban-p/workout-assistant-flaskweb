
from flask_sqlalchemy import SQLAlchemy

########################## 資料庫 ##########################
db = SQLAlchemy()
class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    workoutTime = db.Column(db.DateTime)
    pose = db.Column(db.String(20))
    workoutDuration = db.Column(db.Float)
    status = db.Column(db.String())
    counts = db.Column(db.Integer)

########################## 姿勢 -> 部位 ##########################
class PoseInfo:
    def __init__(self):
        self.trans = {
            'plank': '棒式',
            'pushup': '伏地挺身',
            'wallsit': '靠牆蹲',
            'dumbbell': '二頭肌彎舉',
            'situp': '仰臥起坐',
            'squat': '深蹲'
        }
    def getPose(self, pose):
        return self.trans.get(pose.lower())