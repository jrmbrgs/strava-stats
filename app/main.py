import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd

from queries import stats

st.title("JB's Trail metrics")

st.header("YoY key metrics", divider="rainbow")
st.caption("2023 vs 2023 diffs")


# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)


@st.cache_data
def run_query(query: str) -> pd.DataFrame:
    query_job = client.query(query)
    df: pd.DataFrame = query_job.result().to_dataframe()
    return df


stats_df = run_query(stats)

current = stats_df.loc[stats_df["weekno"] == stats_df["current_weekno"]]
diff_nb_run = (
    current["cumulative_nb_run_2024"].values[0]
    - current["cumulative_nb_run_2023"].values[0]
)

diff_kms = (
    current["cumulative_distance_2024"].values[0]
    - current["cumulative_distance_2023"].values[0]
)

diff_time = round(
    (
        (
            current["cumulative_elapsed_time_2024"].values[0]
            - current["cumulative_elapsed_time_2023"].values[0]
        )
        / 60
        / 60
    ),
    2,
)

diff_elevation = (
    current["cumulative_elevation_gain_2024"].values[0]
    - current["cumulative_elevation_gain_2023"].values[0]
)


col1, col2, col3, col4 = st.columns(4)
with col1:
    current_distance = current["cumulative_distance_2024"].values[0]
    st.metric(
        label="Distance",
        value=f"{current_distance}",
        delta=f"{diff_kms} Kms",
    )
    distance_obj = 2000
    distance_target = st.progress(
        current_distance / distance_obj, text=f"Objective {distance_obj} kms"
    )

with col3:
    st.metric(
        label="Time",
        value=round(current["cumulative_elapsed_time_2024"].values[0] / 60 / 60, 2),
        delta=f"{diff_time} Hours",
    )
with col2:
    current_elevation = current["cumulative_elevation_gain_2024"].values[0]
    st.metric(
        label="Elevation",
        value=f"{current_elevation}",
        delta=f"{diff_elevation} Meters",
    )
    elevation_obj = 50000
    elevation_target = st.progress(
        current_elevation / elevation_obj, text=f"Objective {elevation_obj} m"
    )

with col4:
    st.metric(
        label="Runs",
        value=current["cumulative_nb_run_2024"].values[0],
        delta=f"{diff_nb_run} Runs",
    )
##st.table(data=stats_df)

st.header("YtD charts metrics", divider="rainbow")
st.caption("2023 vs 2023 progression.")
chart_col1, chart_col2, chart_col3, chart_col4 = st.columns(4)
ytd_df = stats_df[stats_df["cumulative_nb_run_2024"].notnull()]
ytd_df["cumulative_elapsed_time_2023"] = (
    ytd_df["cumulative_elapsed_time_2023"].div(3600).round(2)
)
ytd_df["cumulative_elapsed_time_2024"] = (
    ytd_df["cumulative_elapsed_time_2024"].div(3600).round(2)
)


with chart_col1:
    st.subheader("Distance")
    st.caption("Distance in _kms_.")
    st.line_chart(
        ytd_df, x="weekno", y=["cumulative_distance_2023", "cumulative_distance_2024"]
    )
with chart_col2:
    st.subheader("Elevation")
    st.caption("Elevation in _meters_.")
    st.line_chart(
        ytd_df,
        x="weekno",
        y=["cumulative_elevation_gain_2023", "cumulative_elevation_gain_2024"],
    )

with chart_col3:
    st.subheader("Nb Runs")
    st.caption("Number of runs.")
    st.line_chart(
        ytd_df, x="weekno", y=["cumulative_nb_run_2023", "cumulative_nb_run_2024"]
    )
with chart_col4:
    st.subheader("Time")
    st.caption("Time in _hours_.")
    st.line_chart(
        ytd_df,
        x="weekno",
        y=["cumulative_elapsed_time_2023", "cumulative_elapsed_time_2024"],
    )
