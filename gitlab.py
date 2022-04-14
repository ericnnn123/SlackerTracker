import requests

from datetime import date, timedelta
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from config import Config

class Gitlab:

    def __init__(self):
        self.config = Config()
        self.token = self.config.gitlab_token
        self.base_url = f"{self.config.gitlab_url}/api/v4"
        self.session = self.start_session()


    def start_session(self):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 501, 502, 503])
        session = requests.Session()
        session.verify = False
        session.headers.update({"Authorization": f"Bearer {self.token}"})
        session.mount("https://", HTTPAdapter(max_retries=retries))
        return session


    def quit(self):
        self.session.close()


    def get_users(self):
        endpoint = f"/users"
        users = self.session.get(self.base_url + endpoint).json()
        return users


    def get_user_by_username(self, username=None):
        endpoint = f"/users?username={username}"
        users = self.session.get(self.base_url + endpoint).json()
        if type(users) == list:
            for user in users:
                if username == user['username']:
                    return user
        return users


    def get_user_by_id(self, user):
        endpoint = f"/users/{user['id']}"
        user = self.session.get(self.base_url + endpoint).json()
        return user


    def get_users_projects(self, user):
        endpoint = f"/users/{user['id']}/projects"
        projects = self.session.get(self.base_url + endpoint).json()
        return projects


    def get_user_contributions(self, user, weeks_ago=4):
        endpoint = f"/users/{user['id']}/events"
        today = date.today()
        date_to_check = today - timedelta(7 * weeks_ago)
        payload = {
            "per_page": 100,
            "after": date_to_check
        }
        events = self.session.get(self.base_url + endpoint, params=payload).json()
        return events


    def get_projects(self, name=None):
        endpoint = "/projects"
        payload = None
        if name is not None:
            payload = {"search", name}
        
        projects = self.session.get(self.base_url + endpoint, params=payload).json()

        if type(projects) == list:
            for project in projects:
                if name == project['name']:
                    return project
        
        return projects


    def get_project_by_id(self, project):
        projects = self.get_projects()
        for query in projects:
            if project["project_id"] == query["id"]:
                return query
        raise Exception("project id could not be located")


    def get_project_users(self, project):
        endpoint = f"/project/{project['id']}/users"
        users = self.session.get(self.base_url + endpoint).json()
        return users


    def get_project_contributions(self, project, weeks_ago=4):
        endpoint = f"/projects/{project['id']}/events"
        today = date.today()
        date_to_check = today - timedelta(7 * weeks_ago)
        payload = {
            "per_page": 100,
            "after": date_to_check
        }
        events = self.session.get(self.base_url + endpoint, params=payload).json()
        return events


    def get_commit(self, project, commit_hash):
        endpoint = f"/projects/{project['project_id']}/repository/commits/{commit_hash}"
        commits = self.session.get(self.base_url + endpoint).json()
        return commits
