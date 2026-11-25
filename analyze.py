"""
Customer Churn & Responsible Data Card
Run: python analyze.py
"""
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "customer-churn-training.csv"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
required = {
    "customer_id", "tenure_months", "support_tickets",
    "monthly_spend_inr", "last_login_days", "plan_type", "churned"
}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")
if df.empty:
    raise ValueError("The dataset is empty.")

numeric_cols = ["tenure_months", "support_tickets", "monthly_spend_inr", "last_login_days", "churned"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="raise")

total = int(len(df))
churned = int(df["churned"].sum())
active = total - churned

by_status = df.groupby("churned")[[
    "tenure_months", "support_tickets", "monthly_spend_inr", "last_login_days"
]].mean().round(2)

plan_summary = df.groupby("plan_type").agg(
    customers=("customer_id", "count"),
    churned=("churned", "sum"),
    churn_rate=("churned", "mean")
).reset_index()
plan_summary["churn_rate"] = (plan_summary["churn_rate"] * 100).round(2)

summary = {
    "total_customers": total,
    "churned_customers": churned,
    "active_customers": active,
    "churn_rate_percent": round(churned / total * 100, 2),
    "missing_cells": int(df.isna().sum().sum()),
    "duplicate_customer_ids": int(df["customer_id"].duplicated().sum()),
    "columns": list(df.columns),
    "numeric_means_by_churn": {
        "active": by_status.loc[0].to_dict() if 0 in by_status.index else {},
        "churned": by_status.loc[1].to_dict() if 1 in by_status.index else {}
    },
    "plan_summary": plan_summary.to_dict(orient="records"),
    "limitations": [
        "The dataset contains only 12 customer records.",
        "The dataset is a small training sample and may not represent the wider customer population.",
        "The data supports descriptive comparisons, not proof of causation.",
        "No demographic or sensitive personal attributes are included in the supplied columns."
    ]
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
plan_summary.to_csv(OUT / "plan_summary.csv", index=False)

# Chart 1: active vs churned
plt.figure(figsize=(6, 4))
plt.bar(["Active", "Churned"], [active, churned])
plt.title("Customer Status")
plt.ylabel("Number of customers")
plt.tight_layout()
plt.savefig(OUT / "customer_status.png", dpi=160)
plt.close()

# Chart 2: churn by plan
plt.figure(figsize=(6, 4))
plt.bar(plan_summary["plan_type"], plan_summary["churn_rate"])
plt.title("Churn Rate by Plan")
plt.ylabel("Churn rate (%)")
plt.ylim(0, 100)
plt.tight_layout()
plt.savefig(OUT / "churn_by_plan.png", dpi=160)
plt.close()

# Chart 3: average support tickets by status
ticket_means = df.groupby("churned")["support_tickets"].mean()
plt.figure(figsize=(6, 4))
plt.bar(["Active", "Churned"], [ticket_means.get(0, 0), ticket_means.get(1, 0)])
plt.title("Average Support Tickets by Status")
plt.ylabel("Average tickets")
plt.tight_layout()
plt.savefig(OUT / "support_tickets_by_status.png", dpi=160)
plt.close()

print("Analysis complete. See the output/ folder.")
print(f"Customers: {total} | Churned: {churned} | Churn rate: {summary['churn_rate_percent']}%")
