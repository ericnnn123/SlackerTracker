import streamlit
import pandas
import plotly.graph_objects as graph

from streamlit_echarts import st_echarts
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

class Users:

    def __init__(self, gitlab, tracker):
        self.gitlab = gitlab
        self.tracker = tracker
        
    def users(self):
        self.title()
        self.user_contributions()
        self.commit_ratio()
        self.projects()

    def title(self):
        streamlit.title("User Analytics")
        self.option = streamlit.selectbox(
            'Which user would you like to view analytics on?',
            [user["username"] for user in self.gitlab.get_users()]
        )
        self.dataset, self.dates = self.tracker.dataset_user_contributions(self.option, weeks_ago=4)

    def user_contributions(self):
        if len(self.dataset["total"]) > 1:
            options = {
                "title": {"text": "Contributions"},
                "tooltip": {"trigger": "axis"},
                "legend": {"data": ["Additions", "Deletions", "Total"]},
                "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
                "toolbox": {"feature": {"saveAsImage": {}}},
                "xAxis": {
                    "type": "category",
                    "boundaryGap": False,
                    "data": self.dates,
                },
                "yAxis": {"type": "value"},
                "series": [
                    {
                        "name": "Additions",
                        "type": "line",
                        "data": self.dataset['additions'],
                    },
                    {
                        "name": "Deletions",
                        "type": "line",
                        "data": self.dataset['deletions'],
                    },
                    {
                        "name": "Total",
                        "type": "line",
                        "data": self.dataset['total'],
                    },
                ],
                "color": ["#237516", "#A90C0C", "yellow"]
            }
            st_echarts(options=options)
        else:
            streamlit.markdown(f"`{self.option}` doesn't have enough commit history to plot a graph")

    def commit_ratio(self):
        streamlit.subheader("Commit Ratio")

        additions = sum(self.dataset["additions"])
        deletions = sum(self.dataset["deletions"])
        if additions > 0 or deletions > 0:
            options = {
                "title": {"text": "Additions vs Deletions", "subtext": "Contribution Comparison", "left":"center"},
                "tooltip": {"trigger": "item"},
                "legend": {"top": "10%", "left": "center"},
                "series": [
                    {
                        "name": "Contribution",
                        "type": 'pie',
                        "radius": ['40%', '70%'],
                        "avoidLabelOverlap": False,
                        "label": {
                            "show": False,
                            "top": "5%",
                            "position": 'center',
                        },
                        "emphasis": {
                            "label": {
                                "show": True,
                                "fontSize": '30',
                                "fontWeight": 'bold',
                            }
                        },
                        "labelLine": {
                            "show": False,
                        },
                        "data":[
                            {"value": additions, "name": "Additions"},
                            {"value": deletions, "name": "Deletions"},
                        ],
                        "color": ["green", "red"]
                    },
                ],
            }
            st_echarts(
                options=options, height="600px",
            )


    def projects(self):
        streamlit.subheader("Projects")

        projects = self.tracker.compile_analytics_by_user_project_contributions(self.option)
        if len(projects) < 1:
            streamlit.markdown(f"`{self.option}` hasn't contributed to any projects")
        else:
            c1, c2, c3, c4, c5 = streamlit.columns(5)
            for project in projects:
                with c1:
                    pass
                with c2:
                    streamlit.markdown(f"[{project['project']}]({project['link']})")
                with c3:
                    streamlit.markdown(f"Additions:`{project['additions']}`")
                with c4: 
                    streamlit.markdown(f"Deletions: `{project['deletions']}`")
                with c5:
                    streamlit.markdown(f"Total: `{project['total']}`")
                

