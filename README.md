https://ecommerce-sales-analysis-sagar-jam.streamlit.app/

# 🛒 E-Commerce Sales Analysis

An end-to-end data analysis project on e-commerce transaction data: revenue
trends, category and regional performance, discount/return-rate relationship,
customer value concentration, and a written business-insights report with
actionable recommendations.

Built to demonstrate: data wrangling, exploratory data analysis (EDA),
business-oriented insight generation, and data visualization — the core
day-to-day work of a data analyst.

## ✨ Features
- Synthetic but realistic 15,000-row transactional dataset (2 years,
  5 categories, 5 regions, 3 sales channels, seasonality built in) — mirrors
  the structure of real retail datasets like Kaggle's "Online Retail" dataset
- 7 analysis charts covering revenue trend, category/region performance,
  channel & payment mix, discount vs. return rate, and customer spend
  distribution
- Auto-generated `insights.md` — a written executive summary + recommendations,
  the kind of deliverable a real data analyst produces for stakeholders
- Fully reproducible from a single command — no manual data cleaning needed

## 🛠️ Tech Stack
| Layer | Tool |
|---|---|
| Language | Python 3.10+ |
| Data handling | pandas, numpy |
| Visualization | matplotlib, seaborn |

## 📦 Project Structure
```
project3-ecommerce-sales-analysis/
├── app.py                # Streamlit dashboard — deploy this to Streamlit Cloud
├── generate_data.py      # Generates the synthetic transactions dataset
├── analysis.py           # Static-script version: saves charts + insights.md to disk
├── requirements.txt
├── data/                 # Generated CSV lands here
├── outputs/              # Generated charts land here (analysis.py only)
└── README.md
```

## ⚙️ Setup & Run
```bash
git clone https://github.com/<your-username>/ecommerce-sales-analysis.git
cd ecommerce-sales-analysis
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Option A — Interactive dashboard (recommended, deployable)
```bash
streamlit run app.py
```
This is the file to deploy on [Streamlit Cloud](https://share.streamlit.io) —
it auto-generates the dataset on first load if `data/` doesn't exist yet,
so it works out of the box with zero manual steps. Includes region/category
filters and every chart rendered inline.

### Option B — Static script (saves PNGs + a markdown report to disk)
```bash
python generate_data.py   # creates data/ecommerce_transactions.csv
python analysis.py        # creates outputs/*.png + insights.md
```
Useful if you want static image files to embed elsewhere (e.g. a portfolio
site) rather than a live interactive app.

## 📊 Sample Findings (from the generated dataset)
- **Total Net Revenue:** ~$750K across 15,000 orders
- **Clear seasonality:** revenue spikes in Nov–Dec (holiday shopping)
- **Discount tiers above 10% correlate with a higher return rate** — a
  common real-world retail pattern worth A/B testing
- **Top 20% of customers drive a disproportionate share of revenue** —
  classic Pareto pattern, motivating a loyalty-program recommendation

## 🔁 Using Real Data Instead
This project is designed so you can drop in a real dataset with zero code
changes to `analysis.py` — just replace `data/ecommerce_transactions.csv`
with a real one (e.g., Kaggle's ["Online Retail II"](https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci)
or ["Brazilian E-Commerce (Olist)"](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
datasets), matching the column names, or adjust the `load_data()` function's
column mapping.

## 📊 What This Project Demonstrates (for your resume/interview)
- End-to-end analysis pipeline: raw data → cleaning → EDA → visualization → report
- Business-first framing: every chart is tied to a specific decision
  (inventory, marketing spend, discount policy, loyalty programs)
- Proficiency with pandas `groupby`/aggregation, seaborn/matplotlib
  visualization, and translating numbers into stakeholder-ready narrative
- Reproducible, scriptable analysis (not just notebook exploration)

## 🔮 Possible Extensions
- Convert `analysis.py` into a Jupyter notebook with narrative markdown cells
  for a more portfolio-friendly walkthrough
- Add a Power BI / Tableau dashboard on top of the same dataset
- Add cohort/retention analysis (customers by signup month)
- Add basic forecasting (e.g., Prophet or simple linear trend) for next
  quarter's revenue

## 📝 Resume Bullet (copy/adapt this)
> Conducted end-to-end exploratory data analysis on 15,000+ e-commerce
> transactions in Python (pandas, seaborn), identifying revenue drivers,
> a discount-vs-return-rate risk pattern, and customer concentration
> insights; delivered findings as a stakeholder-ready report with
> data-backed recommendations.

## 📄 License
MIT — free to use and adapt.
