# Customer Churn & Responsible Data Card

## Files
- `customer-churn-training.csv` — supplied training dataset.
- `index.html` — responsive Responsible Data Card with charts.
- `analyze.py` — Python analysis script that validates the columns and generates summary metrics and charts.
- `requirements.txt` — Python dependencies.
- `output/` — generated after running the analysis script.

## Run the Python analysis
1. Install Python 3.9 or later.
2. Open a terminal in this project folder.
3. Run: `pip install -r requirements.txt`
4. Run: `python analyze.py`
5. Open `output/summary.json` and the generated PNG charts.

## View the Data Card
Open `index.html` in a modern browser. An internet connection is needed for the Chart.js CDN charts.

## Key findings from the supplied sample
- 12 customers: 5 churned and 7 active.
- Observed churn rate: 41.67%.
- Average support tickets: 3.80 for churned customers and 1.14 for active customers.
- Average tenure: 4.20 months for churned customers and 17.86 months for active customers.
- All 5 Basic-plan customers in this small sample are marked churned; no Standard or Pro customers are marked churned.

## Important limitation
This is a very small training sample. Findings are descriptive only and must not be treated as reliable population estimates, causal explanations, or a basis for automated decisions about individual customers.
