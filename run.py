from flask import Flask, render_template, redirect

from tracker import Tracker
from gitlab import Gitlab
from dashboard import construct_table_information, construct_worker_and_slacker
from users import get_user_rank
        

gitlab = Gitlab()
tracker = Tracker(gitlab)
all_users = sorted(tracker.get_all_user_contributions(), key = lambda user: user['total'])[::-1]
users_with_status = construct_table_information(all_users)
app = Flask(__name__)

@app.route('/')
@app.route('/dashboard')
def dashboard():
    worker, slacker = construct_worker_and_slacker(gitlab, tracker, all_users)
    return render_template('apps/dashboard.html', worker=worker, slacker=slacker, users=users_with_status)


@app.route('/users')
def users():
    return redirect(f"/users/{all_users[-1]['username']}")


@app.route('/users/<user_id>')
def user(user_id):
    current_user = list(filter(lambda person: person['username'] == user_id, users_with_status))[0]
    pie_data = tracker.compile_analytics_by_user(current_user["username"])
    line_data = tracker.dataset_user_contributions(current_user["username"])
    place, total_users = get_user_rank(current_user["username"], all_users)
    return render_template(
        'apps/users.html', 
        current_user=current_user,
        rank={"place": place, "total": total_users},
        users=users_with_status, 
        line_graph=line_data, 
        pie_graph=[pie_data['additions'], pie_data['deletions']]
    )


@app.route('/projects')
def projects():
    return render_template('apps/projects.html')

app.run(debug=True)
gitlab.quit()