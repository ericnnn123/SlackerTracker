from importlib_metadata import Deprecated
import pandas
import streamlit

from tracker import Tracker
from gitlab import Gitlab
from appsd.dashboard import Dashboard
from appsd.users import Users

gitlab = Gitlab()
tracker = Tracker(gitlab)

with streamlit.sidebar:
    streamlit.subheader("Navigation")
    select = streamlit.radio(
        "Go To: ",
        ("Dashboard", "Users", "Projects")
    )

if select == "Dashboard":
    Dashboard(gitlab, tracker).dashboard()    

if select == "Users":
    Users(gitlab, tracker).users()
    

if select == "Projects":
    pass

gitlab.quit()
