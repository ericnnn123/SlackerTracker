import pandas
import streamlit

from tracker import Tracker
from gitlab import Gitlab
from apps.dashboard import dashboard
from apps.users import users

gitlab = Gitlab()
tracker = Tracker(gitlab)

with streamlit.sidebar:
    streamlit.subheader("Navigation")
    select = streamlit.radio(
        "Go To: ",
        ("Dashboard", "Users", "Projects")
    )

if select == "Dashboard":
    dashboard(gitlab, tracker)    

if select == "Users":
    users(gitlab, tracker)
    

if select == "Projects":
    pass

gitlab.quit()
