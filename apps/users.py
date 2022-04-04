import streamlit
import pandas
import plotly.graph_objects as graph

def users(gitlab, tracker):
    streamlit.title("User Analytics")
    
    option = streamlit.selectbox(
        'Which user would you like to view analytics on?',
        [user["username"] for user in gitlab.get_users()]
    )

    dataset, dates = tracker.dataset_user_contributions(option, weeks_ago=4)
    if len(dataset["total"]) > 1:
        chart_data = pandas.DataFrame(
            data=dataset,
            index=dates
        )
        streamlit.line_chart(chart_data)
    else:
        streamlit.markdown(f"`{option}` doesn't have enough commit history to plot a graph")

    streamlit.subheader("Commit Ratio")
    col1, col2 = streamlit.columns(2)
    additions = sum(dataset["additions"])
    deletions = sum(dataset["deletions"])
    if additions > 0 or deletions > 0:
        with col1:
            labels = ["Additions", "Deletions"]
            values = [additions, deletions]
            figure = graph.Figure(data=[graph.Pie(labels=labels, values=values)])
            figure.update_traces(marker=dict(colors=['green', 'red']))
            streamlit.plotly_chart(figure, use_container_width=True)
            

        with col2:
            streamlit.markdown(f"**Addition %:** `%{int(round((additions / (additions + deletions)) * 100))}`")
            streamlit.markdown(f"**Deletion %:** `%{int(round((deletions / (additions + deletions)) * 100))}`")
            streamlit.markdown(f"**Additions/Deletions:** `1:{round(additions/deletions, 2)}`")
            streamlit.markdown(f"**Deletions/Additions:** `1:{round(deletions/additions, 2)}`")
    else:
            streamlit.markdown(f"`{option}` doesn't have any additions/deletions")
