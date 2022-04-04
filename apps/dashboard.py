import pandas
import streamlit

from PIL import Image
from urllib import request
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode


def dashboard(gitlab, tracker):
    streamlit.title("Slacker Tracker")

    data = tracker.get_all_user_contributions()
    
    col1, col2 = streamlit.columns(2)
    with col1:
        hardest_worker = data["Users"][data["Total"].index(max(data["Total"]))]
        user = gitlab.get_user_by_username(hardest_worker)
        user_analytics = tracker.compile_analytics_by_user(hardest_worker)
        col1container = streamlit.container()
        request.urlretrieve(user["avatar_url"], "worker.png")
        image = Image.open("worker.png")

        col1container.success("Hardest Worker")
        streamlit.image(image)
        streamlit.subheader(hardest_worker)
        streamlit.markdown(f"**Commits:** `{user_analytics['commits']}`")
        streamlit.markdown(f"**Total:** `{user_analytics['total']}`")
        streamlit.markdown(f"**Additions:** `{user_analytics['additions']}`")
        streamlit.markdown(f"**Deletions:** `{user_analytics['deletions']}`")

    with col2:
        hardest_slacker = data["Users"][data["Total"].index(min(data["Total"]))]
        user = gitlab.get_user_by_username(hardest_slacker)
        user_analytics = tracker.compile_analytics_by_user(hardest_slacker)
        col2container = streamlit.container()
        request.urlretrieve(user["avatar_url"], "slacker.png")
        image = Image.open("slacker.png")
    
        col2container.error("Hardest Slacker")
        streamlit.image(image)
        streamlit.subheader(hardest_slacker)
        streamlit.markdown(f"**Commits:** `{user_analytics['commits']}`")
        streamlit.markdown(f"**Total:** `{user_analytics['total']}`")
        streamlit.markdown(f"**Additions:** `{user_analytics['additions']}`")
        streamlit.markdown(f"**Deletions:** `{user_analytics['deletions']}`")

 
    chart_data = pandas.DataFrame(data)
    options = GridOptionsBuilder.from_dataframe(
        chart_data, enableRowGroup=True, enableValue=True, enablePivot=True
    )
    selection = AgGrid(
        chart_data,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="dark",
    )