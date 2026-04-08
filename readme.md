# Ask Your Dashboard

This prototype demonstrates how developers can turn dashboards into answer-driven product experiences.

Instead of forcing users to interpret charts manually, the interface allows them to ask simple questions about product analytics and receive clear answers.

## Problem

Many SaaS products embed dashboards for analytics, but end users still need to interpret charts by themselves.

This creates friction and slows down decision-making.

## Solution

This prototype adds a lightweight "Ask Your Dashboard" layer on top of product analytics.

Users can ask questions like:

- Which feature is trending this week?
- Which region uses the product the most?
- Which feature has the lowest adoption?
- Which plan uses analytics the most?
- What is the most used feature overall?

and receive immediate, answer-oriented responses.

## What this prototype demonstrates

- How Sisense-powered analytics can support answer-driven interfaces
- How dashboards can evolve into lightweight analytics experiences
- How developers can build a simple question-to-answer layer on top of product usage data

## Audience

This prototype is aimed at SaaS developers, technical product builders, and startup teams that want to embed analytics inside their products without forcing users to decode charts manually.

## Positioning
This prototype shows how developers can turn Sisense dashboards into answer-driven product experiences.

## Demo Flow

1. Sisense provides the analytics layer and dashboard foundation
2. A lightweight app surfaces key KPIs, charts, and insights
3. Users ask predefined product questions
4. The system returns clear, concise answers based on the data

## Architecture

- Synthetic SaaS product usage dataset
- Sisense dashboard as the analytics foundation
- Streamlit app for the answer-oriented interface
- Pandas for KPI, insight, and question logic
- Plotly for charts

## Project Files

- `generate_dataset.py` - creates a synthetic product usage dataset
- `data_prep.py` - computes KPIs, chart data, insights, and answers
- `app.py` - Streamlit app
- `product_usage.csv` - generated dataset
- `requirements.txt` - dependencies

## How to Run

```bash
python generate_dataset.py
pip install -r requirements.txt
streamlit run app.py