import pandas as pd


QUESTION_TRENDING = "Which feature is trending this week?"
QUESTION_TOP_REGION = "Which region uses the product the most?"
QUESTION_LOWEST_ADOPTION = "Which feature has the lowest adoption?"
QUESTION_TOP_PLAN = "Which plan uses analytics the most?"
QUESTION_TOP_FEATURE = "What is the most used feature overall?"


def format_feature_name(value: str) -> str:
    return value.replace("_", " ").title()


def load_data(path: str = "product_usage.csv") -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["date"])
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()
    df["feature_label"] = df["feature"].apply(format_feature_name)
    return df


def get_time_windows(df: pd.DataFrame) -> tuple[pd.Timestamp, pd.Timestamp, pd.Timestamp]:
    last_date = df["date"].max()
    last_week_start = last_date - pd.Timedelta(days=6)
    previous_week_start = last_week_start - pd.Timedelta(days=7)
    return last_date, last_week_start, previous_week_start


def compute_feature_growth(df: pd.DataFrame) -> pd.DataFrame:
    _, last_week_start, previous_week_start = get_time_windows(df)

    last_week = df[df["date"] >= last_week_start]
    previous_week = df[(df["date"] >= previous_week_start) & (df["date"] < last_week_start)]

    last_week_counts = (
        last_week.groupby("feature")
        .size()
        .rename("last_week_events")
    )

    previous_week_counts = (
        previous_week.groupby("feature")
        .size()
        .rename("previous_week_events")
    )

    growth_df = pd.concat([last_week_counts, previous_week_counts], axis=1).fillna(0)
    growth_df["absolute_growth"] = growth_df["last_week_events"] - growth_df["previous_week_events"]
    growth_df["growth_pct"] = growth_df.apply(
        lambda row: (
            ((row["last_week_events"] - row["previous_week_events"]) / row["previous_week_events"]) * 100
            if row["previous_week_events"] > 0
            else 100.0
        ),
        axis=1,
    )

    growth_df = growth_df.sort_values(
        by=["absolute_growth", "growth_pct"],
        ascending=[False, False],
    )

    return growth_df


def compute_kpis(df: pd.DataFrame) -> dict:
    total_events = len(df)
    active_companies = df["company_id"].nunique()

    most_used_feature_raw = df["feature"].value_counts().idxmax()
    most_used_feature = format_feature_name(most_used_feature_raw)

    growth_df = compute_feature_growth(df)
    fastest_feature_raw = growth_df.index[0]
    fastest_feature = format_feature_name(fastest_feature_raw)

    return {
        "total_events": total_events,
        "active_companies": active_companies,
        "most_used_feature": most_used_feature,
        "fastest_feature": fastest_feature,
    }


def compute_chart_data(df: pd.DataFrame) -> dict:
    feature_usage_over_time = (
        df.groupby(["date", "feature_label"])
        .size()
        .reset_index(name="events")
        .sort_values(["date", "feature_label"])
    )

    usage_by_region = (
        df.groupby("region")
        .size()
        .reset_index(name="events")
        .sort_values("events", ascending=False)
    )

    usage_by_plan = (
        df.groupby("plan")
        .size()
        .reset_index(name="events")
        .sort_values("events", ascending=False)
    )

    return {
        "feature_usage_over_time": feature_usage_over_time,
        "usage_by_region": usage_by_region,
        "usage_by_plan": usage_by_plan,
    }


def compute_adoption_by_feature(df: pd.DataFrame) -> pd.DataFrame:
    active_companies = df["company_id"].nunique()

    adoption_by_feature = (
        df.groupby("feature")["company_id"]
        .nunique()
        .reset_index(name="active_companies_using_feature")
    )

    adoption_by_feature["adoption_rate"] = (
        adoption_by_feature["active_companies_using_feature"] / active_companies
    ) * 100

    adoption_by_feature["feature_label"] = adoption_by_feature["feature"].apply(format_feature_name)
    adoption_by_feature = adoption_by_feature.sort_values("adoption_rate", ascending=True)

    return adoption_by_feature


def compute_insights(df: pd.DataFrame) -> dict:
    growth_df = compute_feature_growth(df)

    fastest_feature_raw = growth_df.index[0]
    fastest_growth_pct = round(growth_df.iloc[0]["growth_pct"])

    top_region_raw = df["region"].value_counts().idxmax()

    adoption_by_feature = compute_adoption_by_feature(df)
    lowest_feature_raw = adoption_by_feature.iloc[0]["feature"]
    lowest_feature_rate = round(adoption_by_feature.iloc[0]["adoption_rate"])

    return {
        "fastest_feature": format_feature_name(fastest_feature_raw),
        "fastest_growth_pct": fastest_growth_pct,
        "top_region": top_region_raw,
        "lowest_feature": format_feature_name(lowest_feature_raw),
        "lowest_feature_rate": lowest_feature_rate,
    }


def answer_question(df: pd.DataFrame, question: str) -> str:
    growth_df = compute_feature_growth(df)

    if question == QUESTION_TRENDING:
        fastest_feature_raw = growth_df.index[0]
        fastest_feature = format_feature_name(fastest_feature_raw)
        growth_pct = round(growth_df.iloc[0]["growth_pct"])
        return f"{fastest_feature} usage increased by {growth_pct}% this week and is the fastest growing feature."

    if question == QUESTION_TOP_REGION:
        region_counts = df["region"].value_counts()
        top_region = region_counts.idxmax()
        top_region_events = int(region_counts.iloc[0])
        total_events = len(df)
        share_pct = round((top_region_events / total_events) * 100)
        return f"{top_region} accounts generate the highest product activity, representing {share_pct}% of all events."

    if question == QUESTION_LOWEST_ADOPTION:
        adoption_by_feature = compute_adoption_by_feature(df)
        feature = adoption_by_feature.iloc[0]["feature_label"]
        adoption_rate = round(adoption_by_feature.iloc[0]["adoption_rate"])
        return f"{feature} has the lowest adoption, used by {adoption_rate}% of active companies."

    if question == QUESTION_TOP_PLAN:
        plan_counts = df["plan"].value_counts()
        top_plan = plan_counts.idxmax().title()
        top_plan_events = int(plan_counts.iloc[0])
        total_events = len(df)
        share_pct = round((top_plan_events / total_events) * 100)
        return f"{top_plan} customers generate the most analytics usage, accounting for {share_pct}% of all events."

    if question == QUESTION_TOP_FEATURE:
        feature_counts = df["feature"].value_counts()
        feature_raw = feature_counts.idxmax()
        feature = format_feature_name(feature_raw)
        events = int(feature_counts.iloc[0])
        total_events = len(df)
        share_pct = round((events / total_events) * 100)
        return f"{feature} is the most used feature overall, representing {share_pct}% of all product events."

    return "Please select one of the supported questions."