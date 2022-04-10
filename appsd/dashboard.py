import pandas
import streamlit

from PIL import Image
from urllib import request
from st_aggrid import AgGrid, GridOptionsBuilder


class Dashboard():

    def __init__(self, gitlab, tracker):
        self.gitlab = gitlab
        self.tracker = tracker
        self.data = self.tracker.get_all_user_contributions()

    def dashboard(self):
        self.title()
        self.leaderboard()
        self.interactive_table()

    def title(self):
        streamlit.title("Slacker Tracker")

    def leaderboard(self):
        col1, col2 = streamlit.columns(2)
        with col1:
            hardest_worker = self.data["Users"][self.data["Total"].index(max(self.data["Total"]))]
            user = self.gitlab.get_user_by_username(hardest_worker)
            user_analytics = self.tracker.compile_analytics_by_user(hardest_worker)
            col1container = streamlit.container()
            
            col1container.success("Hardest Worker")
            streamlit.markdown(f"![Worker]({user['avatar_url']})")
            streamlit.subheader(hardest_worker)
            streamlit.markdown(f"**Commits:** `{user_analytics['commits']}`")
            streamlit.markdown(f"**Total:** `{user_analytics['total']}`")
            streamlit.markdown(f"**Additions:** `{user_analytics['additions']}`")
            streamlit.markdown(f"**Deletions:** `{user_analytics['deletions']}`")

        with col2:
            hardest_slacker = self.data["Users"][self.data["Total"].index(min(self.data["Total"]))]
            user = self.gitlab.get_user_by_username(hardest_slacker)
            user_analytics = self.tracker.compile_analytics_by_user(hardest_slacker)
            col2container = streamlit.container()
        
            col2container.error("Hardest Slacker")
            streamlit.markdown(f"![Slacker]({user['avatar_url']})")
            streamlit.subheader(hardest_slacker)
            streamlit.markdown(f"**Commits:** `{user_analytics['commits']}`")
            streamlit.markdown(f"**Total:** `{user_analytics['total']}`")
            streamlit.markdown(f"**Additions:** `{user_analytics['additions']}`")
            streamlit.markdown(f"**Deletions:** `{user_analytics['deletions']}`")

    def interactive_table(self):
        chart_data = pandas.DataFrame(self.data)
        options = GridOptionsBuilder.from_dataframe(
            chart_data, enableRowGroup=True, enableValue=True, enablePivot=True
        )
        selection = AgGrid(
            chart_data,
            enable_enterprise_modules=True,
            gridOptions=options.build(),
            theme="dark",
            fit_columns_on_grid_load=True
        )

