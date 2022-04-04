from dateutil import parser
from gitlab import Gitlab


class Tracker:

    def __init__(self, gitlab):
        self.gitlab = gitlab


    def compile_analytics_by_user(self, username, weeks_ago=4):
        analytics = {"commits":0, "additions": 0, "deletions": 0, "total": 0}
        user_id = self.gitlab.get_user_by_username(username)["id"]
        contributions = self.gitlab.get_user_contributions(user_id, weeks_ago)
        analytics["commits"] = len(contributions)

        for contribution in contributions:
            project_id = contribution["project_id"]

            if "push_data" in contribution:
                commit_hash = contribution["push_data"]["commit_to"]
                commit = self.gitlab.get_commit(project_id, commit_hash)

                if "stats" in commit:
                    analytics["additions"] += commit["stats"]["additions"]
                    analytics["deletions"] += commit["stats"]["deletions"]
                    analytics["total"] += commit["stats"]["total"]

        return analytics


    def compile_analytics_by_project(self, project_id, weeks_ago=4, sort=True):
        analytics = list()
        contributions = self.gitlab.get_project_contributions(project_id, weeks_ago)
        for contribution in contributions:
            user = contribution["author"]["name"]
            if not any(dataset["author"] == user for dataset in analytics):
                analytics.append(
                    {
                        "author": user,
                        "changes": {
                            "additions": 0,
                            "deletions": 0,
                            "total": 0
                        }
                    }
                )

            for dataset in analytics:
                if contribution["author"]["name"] == dataset["author"]:
                    if "push_data" in contribution:
                        commit_hash = contribution["push_data"]["commit_to"]
                        commit = self.gitlab.get_commit(project_id, commit_hash)

                        if "stats" in commit:
                            dataset["additions"] += commit["stats"]["additions"]
                            dataset["deletions"] += commit["stats"]["deletions"]
                            dataset["total"] += commit["stats"]["total"]

        if sort:
            analytics = sorted(analytics, key=lambda contribution: contribution["changes"]["total"], reverse=True)

        return analytics


    def dataset_user_contributions(self, username, weeks_ago=4):
        analytics = {"additions": [], "deletions": [], "total": []}
        dates = list()
        user_id = self.gitlab.get_user_by_username(username)["id"]
        contributions = self.gitlab.get_user_contributions(user_id, weeks_ago)

        for contribution in contributions:
            project_id = contribution["project_id"]

            if "push_data" in contribution:
                commit_hash = contribution["push_data"]["commit_to"]
                commit = self.gitlab.get_commit(project_id, commit_hash)

                if "stats" in commit:
                    date = str(parser.parse(commit["created_at"]).strftime("%Y-%m-%d %H:%M"))
                    analytics["additions"].append(commit["stats"]["additions"])
                    analytics["deletions"].append(commit["stats"]["deletions"])
                    analytics["total"].append(commit["stats"]["total"])
                    dates.append(date)

        return analytics, dates


    def dataset_analytics_by_project(self, project_id, weeks_ago=4):
        analytics = list()
        contributions = self.gitlab.get_project_contributions(project_id, weeks_ago)
        for contribution in contributions:
            user = contribution["author"]["name"]
            if not any(dataset["author"] == user for dataset in analytics):
                analytics.append(
                    {
                        "author": user,
                        "changes": {
                            "additions": [],
                            "deletions": [],
                            "total": [],
                            "date": []
                        }
                    }
                )

            for dataset in analytics:
                if contribution["author"]["name"] == dataset["author"]:
                    if "push_data" in contribution:
                        commit_hash = contribution["push_data"]["commit_to"]
                        commit = self.gitlab.get_commit(project_id, commit_hash)

                        if "stats" in commit:
                            date = str(parser.parse(commit["created_at"]).strftime("%Y-%m-%d %H:%M"))
                            dataset["additions"].append(commit["stats"]["additions"])
                            dataset["deletions"].append(commit["stats"]["deletions"])
                            dataset["total"].append(commit["stats"]["total"])
                            dataset["date"].append(date)

        return analytics


    def get_all_user_contributions(self, weeks_ago=4):
        data = {"Users": list(), "Commits": list(), "Additions": list(), "Deletions": list(), "Total": list()}
        for user in self.gitlab.get_users():
            user_analytics = self.compile_analytics_by_user(user['username'], weeks_ago=4)
            data["Users"].append(user['username'])
            data["Commits"].append(user_analytics["commits"])
            data["Additions"].append(user_analytics["additions"])
            data["Deletions"].append(user_analytics["deletions"])
            data["Total"].append(user_analytics["total"])

        return data
