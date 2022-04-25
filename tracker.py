from dateutil import parser


class Tracker:

    def __init__(self, gitlab):
        self.gitlab = gitlab


    def compile_analytics_by_user(self, username, weeks_ago=4):
        analytics = {"commits":0, "additions": 0, "deletions": 0, "total": 0}
        user = self.gitlab.get_user_by_username(username)
        contributions = self.gitlab.get_user_contributions(user, weeks_ago)
        analytics["commits"] = len(contributions)

        for contribution in contributions:
            project = contribution

            if "push_data" in contribution:
                commit_hash = contribution["push_data"]["commit_to"]
                commit = self.gitlab.get_commit(project, commit_hash)

                if "stats" in commit:
                    analytics["additions"] += commit["stats"]["additions"]
                    analytics["deletions"] += commit["stats"]["deletions"]
                    analytics["total"] += commit["stats"]["total"]

        return analytics


    def dataset_user_contributions(self, username, weeks_ago=4):
        analytics = {"additions": [], "deletions": [], "total": [], "dates": []}
        user = self.gitlab.get_user_by_username(username)
        contributions = self.gitlab.get_user_contributions(user, weeks_ago)
        for contribution in contributions:
            project = contribution

            if "push_data" in contribution:
                commit_hash = contribution["push_data"]["commit_to"]
                commit = self.gitlab.get_commit(project, commit_hash)

                if "stats" in commit:
                    date = str(parser.parse(commit["created_at"]).strftime("%Y-%m-%d %H:%M"))
                    analytics["additions"].append(commit["stats"]["additions"])
                    analytics["deletions"].append(commit["stats"]["deletions"])
                    analytics["total"].append(commit["stats"]["total"])
                    analytics["dates"].append(date)

        return analytics


    def compile_analytics_by_user_project_contributions(self, username, sort=True, weeks_ago=4):
        analytics = list()
        user = self.gitlab.get_user_by_username(username)
        contributions = self.gitlab.get_user_contributions(user, weeks_ago)

        for contribution in contributions:
            project = contribution
            project_info = self.gitlab.get_project_by_id(project)
            project_name = project_info["name"]
            if not any(dataset["project"] == project_name for dataset in analytics):
                analytics.append(
                    {
                        "project_id": project_info["id"],
                        "link": project_info["web_url"],
                        "project": project_name,
                        "additions": 0,
                        "deletions": 0,
                        "total": 0
                    }
                )

            for dataset in analytics:
                if contribution["project_id"] == dataset["project_id"]:
                    if "push_data" in contribution:
                        commit_hash = contribution["push_data"]["commit_to"]
                        commit = self.gitlab.get_commit(project, commit_hash)

                        if "stats" in commit:
                            dataset["additions"] += commit["stats"]["additions"]
                            dataset["deletions"] += commit["stats"]["deletions"]
                            dataset["total"] += commit["stats"]["total"]
        if sort:
            analytics = sorted(analytics, key=lambda contribution: contribution["total"], reverse=True)

        return analytics


    def compile_analytics_by_project(self, project, weeks_ago=4, sort=True):
        analytics = list()
        contributions = self.gitlab.get_project_contributions(project, weeks_ago)
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
                        commit = self.gitlab.get_commit(project, commit_hash)

                        if "stats" in commit:
                            dataset["additions"] += commit["stats"]["additions"]
                            dataset["deletions"] += commit["stats"]["deletions"]
                            dataset["total"] += commit["stats"]["total"]

        if sort:
            analytics = sorted(analytics, key=lambda contribution: contribution["changes"]["total"], reverse=True)

        return analytics


    def dataset_analytics_by_project(self, project, weeks_ago=4):
        analytics = list()
        contributions = self.gitlab.get_project_contributions(project, weeks_ago)
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
                        commit = self.gitlab.get_commit(project, commit_hash)

                        if "stats" in commit:
                            date = str(parser.parse(commit["created_at"]).strftime("%Y-%m-%d %H:%M"))
                            dataset["additions"].append(commit["stats"]["additions"])
                            dataset["deletions"].append(commit["stats"]["deletions"])
                            dataset["total"].append(commit["stats"]["total"])
                            dataset["date"].append(date)

        return analytics


    def get_all_user_contributions(self, weeks_ago=4):
        data = list()
        for user in self.gitlab.get_users():
            user_analytics = self.compile_analytics_by_user(user['username'], weeks_ago=4)
            user_analytics["username"] = user["username"]
            data.append(user_analytics)

        return data


    def format_user_projects_bar_chart(self, username, weeks_ago=4):
        chart = {
            "projects": list(),
            "additions": list(),
            "deletions": list(),
            "totals": list()
        }
        project_contribution_data = self.compile_analytics_by_user_project_contributions(username, weeks_ago)
        
        for project in project_contribution_data:
            chart['projects'].append(project['project'])
            chart["additions"].append(project["additions"])
            chart["deletions"].append(project["deletions"])
            chart["totals"].append(project["total"])

        return chart

    