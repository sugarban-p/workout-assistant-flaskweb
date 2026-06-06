import os
import json
import auth
import home
from flask import Flask, render_template, redirect, url_for, g
from collections import defaultdict
from ast import literal_eval
from myclass import PoseInfo, Record, db
from dbfuns import init_db


app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config.from_mapping(
    DATABASE=os.path.join(base_dir, 'project.db'),
    SECRET_KEY='your_secret_key',
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(base_dir, 'project.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db.init_app(app)

app.register_blueprint(auth.bp)
app.register_blueprint(home.bp)
with open(os.path.join(base_dir, 'articles.json'), 'r', encoding='utf-8') as file:
    articles = json.load(file)

@app.route('/')
def index():
    if g.user is None:
        return render_template('home.html')
    return redirect(url_for('home.welcome'))

@app.route('/workout')
@auth.login_required
def workout():
    return render_template('workout.html',articles=articles)

@app.route('/data')
@auth.login_required
def data():
    records = Record.query.filter_by(userid=g.user['id']).all()
    record_data = []

    for record in records:
        if record.workoutTime is None:
            continue

        record_dict = {
            'id': record.id,
            'workoutTime': record.workoutTime.strftime('%Y-%m-%d %H:%M:%S') if record.workoutTime else '',
            'pose': PoseInfo().getPose(record.pose) if record.pose else '',
            'totalTime': record.workoutDuration if record.workoutDuration is not None else 0,
            'status': record.status if record.status else '--',
            'counts': record.counts if record.counts is not None else 0
        }
        record_data.append(record_dict)

    poses = sorted(set(record['pose'] for record in record_data if record['pose']))
    pose_counts = defaultdict(int)
    pose_total_times = defaultdict(float)
    daily_pose_times = defaultdict(lambda: defaultdict(float))

    for record in record_data:
        pose = record['pose']
        if pose:
            counts = record['counts']
            if isinstance(counts, str):
                try:
                    counts_list = literal_eval(counts)
                    counts = max(counts_list)
                    # counts = next((x for x in reversed(counts_list) if x != 0), 0)
                except:
                    counts = 0
            pose_counts[pose] += counts
            pose_total_times[pose] += float(record['totalTime'])
            
            date_str = record['workoutTime'].split()[0]
            daily_pose_times[date_str][pose] += float(record['totalTime'])

    dates = sorted(daily_pose_times.keys())
    daily_pose_data = {pose: [daily_pose_times[date][pose] for date in dates] for pose in poses}

    chart_data = {
        'poses': poses,
        'poseCounts': [int(pose_counts[pose]) for pose in poses],
        'poseTotalTimes': [round(pose_total_times[pose],1) for pose in poses],
        'dates': dates,
        'dailyPoses': [{'name': pose, 'times': daily_pose_data[pose]} for pose in poses]
    }

    return render_template('result.html', records=record_data, chart_data=chart_data)

with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)