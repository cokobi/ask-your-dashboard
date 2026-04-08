import streamlit as st
import plotly.express as px

from data_prep import (
    QUESTION_LOWEST_ADOPTION,
    QUESTION_TOP_FEATURE,
    QUESTION_TOP_PLAN,
    QUESTION_TOP_REGION,
    QUESTION_TRENDING,
    answer_question,
    compute_chart_data,
    compute_insights,
    compute_kpis,
    load_data,
)

st.set_page_config(page_title="Ask Your Dashboard", layout="wide")

df = load_data()
kpis = compute_kpis(df)
chart_data = compute_chart_data(df)
insights = compute_insights(df)

questions = [
    QUESTION_TRENDING,
    QUESTION_TOP_REGION,
    QUESTION_LOWEST_ADOPTION,
    QUESTION_TOP_PLAN,
    QUESTION_TOP_FEATURE,
]

if "selected_question" not in st.session_state:
    st.session_state.selected_question = QUESTION_TRENDING

st.title("Ask Your Dashboard")
st.subheader("Ask questions about your product analytics data")
st.caption("Dataset: SaaS Product Usage (Last 30 Days)")

st.markdown("---")

top_left, top_right = st.columns([1.2, 1])

with top_left:
    st.markdown("### Ask Your Dashboard")
    st.markdown(
        """
Try asking:

- Which feature is trending this week?
- Which region uses the product the most?
- Which feature has the lowest adoption?
- Which plan uses analytics the most?
- What is the most used feature overall?
"""
    )

    selected_question = st.selectbox(
        "Choose a question",
        questions,
        index=questions.index(st.session_state.selected_question),
    )
    st.session_state.selected_question = selected_question

with top_right:
    st.markdown("### Answer")
    answer = answer_question(df, st.session_state.selected_question)
    st.info(answer)

st.markdown("---")

st.markdown("### KPI Summary")
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.metric("Total Events", f"{kpis['total_events']:,}")

with kpi_col2:
    st.metric("Active Companies", f"{kpis['active_companies']:,}")

with kpi_col3:
    st.metric("Top Feature", kpis["most_used_feature"])

with kpi_col4:
    st.metric("Fastest Growth", kpis["fastest_feature"])

st.markdown("---")

st.markdown("### Product Analytics Snapshot")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    feature_line = px.line(
        chart_data["feature_usage_over_time"],
        x="date",
        y="events",
        color="feature_label",
        title="Feature Usage Over Time",
        markers=True,
    )
    feature_line.update_layout(
        xaxis_title="Date",
        yaxis_title="Events",
        legend_title="Feature",
        height=360,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    st.plotly_chart(feature_line, use_container_width=True)

with chart_col2:
    region_bar = px.bar(
        chart_data["usage_by_region"],
        x="region",
        y="events",
        title="Usage by Region",
        text="events",
    )
    region_bar.update_layout(
        xaxis_title="Region",
        yaxis_title="Events",
        height=360,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    st.plotly_chart(region_bar, use_container_width=True)

st.markdown("---")

st.markdown("### Insights")
insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    st.success(
        f"**{insights['fastest_feature']}** grew the fastest this week, up **{insights['fastest_growth_pct']}%**."
    )

with insight_col2:
    st.success(
        f"**{insights['top_region']}** generates the highest product activity."
    )

with insight_col3:
    st.success(
        f"**{insights['lowest_feature']}** has the lowest adoption at **{insights['lowest_feature_rate']}%** of active companies."
    )

st.markdown("---")

st.caption(
    "This prototype demonstrates how Sisense-powered analytics can become an answer-driven product experience."
)