from flask import Flask, render_template

from tracker import Tracker
from gitlab import Gitlab


gitlab = Gitlab()
tracker = Tracker(gitlab)

data = tracker.get_all_user_contributions()
all_users = tracker.get_all_user_contributions()
hardest_worker = all_users["Users"][all_users["Total"].index(max(all_users["Total"]))]
hardest_slacker = all_users["Users"][all_users["Total"].index(min(all_users["Total"]))]
worker_analytics = tracker.compile_analytics_by_user(hardest_worker)
slacker_analytics = tracker.compile_analytics_by_user(hardest_slacker)

app = Flask(__name__)

@app.route('/')
@app.route('/dashboard')
def dashboard():
    worker = {
        "name": hardest_worker,
        "img": gitlab.get_user_by_username(hardest_worker)['avatar_url'],
        "commits": worker_analytics['commits'],
        "total": worker_analytics['total'],
        "additions": worker_analytics['additions'],
        "deletions": worker_analytics['deletions']
    }
    slacker = {
        "name": hardest_slacker,
        "img": gitlab.get_user_by_username(hardest_slacker)['avatar_url'],
        "commits": slacker_analytics['commits'],
        "total": slacker_analytics['total'],
        "additions": slacker_analytics['additions'],
        "deletions": slacker_analytics['deletions']
    }
    return render_template('apps/dashboard.html', worker=worker, slacker=slacker)

@app.route('/users')
def users():
    return render_template('apps/users.html')

@app.route('/projects')
def projects():
    return render_template('apps/projects.html')

app.run(debug=True)
