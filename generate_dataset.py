import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

rows = []

features = ["analytics_dashboard", "ai_insights", "cohort_analysis"]
regions = ["US", "EU", "APAC"]
plans = ["starter", "pro", "enterprise"]

feature_event_weights = {
    "analytics_dashboard": {"view": 0.65, "click": 0.20, "run": 0.10, "export": 0.05},
    "ai_insights": {"view": 0.20, "click": 0.35, "run": 0.35, "export": 0.10},
    "cohort_analysis": {"view": 0.25, "click": 0.20, "run": 0.45, "export": 0.10},
}

start_date = datetime(2026, 3, 1)
num_days = 31
num_rows = 340

company_ids = list(range(100, 161))
user_ids = list(range(9000, 9501))

for _ in range(num_rows):
    day_offset = random.randint(0, num_days - 1)
    event_date = start_date + timedelta(days=day_offset)

    is_last_week = day_offset >= 24

    if is_last_week:
        feature = random.choices(
            population=features,
            weights=[0.42, 0.43, 0.15],
            k=1,
        )[0]
    else:
        feature = random.choices(
            population=features,
            weights=[0.55, 0.28, 0.17],
            k=1,
        )[0]

    if is_last_week:
        region = random.choices(
            population=regions,
            weights=[0.35, 0.43, 0.22],
            k=1,
        )[0]
    else:
        region = random.choices(
            population=regions,
            weights=[0.42, 0.36, 0.22],
            k=1,
        )[0]

    if feature == "ai_insights":
        plan = random.choices(
            population=plans,
            weights=[0.18, 0.37, 0.45],
            k=1,
        )[0]
    elif feature == "cohort_analysis":
        plan = random.choices(
            population=plans,
            weights=[0.28, 0.32, 0.40],
            k=1,
        )[0]
    else:
        plan = random.choices(
            population=plans,
            weights=[0.42, 0.36, 0.22],
            k=1,
        )[0]

    event_types = list(feature_event_weights[feature].keys())
    event_weights = list(feature_event_weights[feature].values())
    event_type = random.choices(event_types, weights=event_weights, k=1)[0]

    company_id = random.choice(company_ids)
    user_id = random.choice(user_ids)

    rows.append(
        [
            event_date.strftime("%Y-%m-%d"),
            company_id,
            user_id,
            feature,
            event_type,
            plan,
            region,
        ]
    )

df = pd.DataFrame(
    rows,
    columns=[
        "date",
        "company_id",
        "user_id",
        "feature",
        "event_type",
        "plan",
        "region",
    ],
)

df.to_csv("product_usage.csv", index=False)
print(f"product_usage.csv created with {len(df)} rows")