Customer Transaction Analysis
An end-to-end data analytics project on 50,000 customer card transactions ($22.1M, Jan to Oct 2023). It takes a raw transaction file through cleaning, feature engineering, exploratory analysis, SQL, statistical testing, visualisation and business recommendations, and documents the results in a full written report.

Tools: Python (Pandas, NumPy, Matplotlib, SciPy) | SQL | Excel | Power BI

Table of contents
Project overview
Business questions
Dataset
Approach
Key findings
Statistical validation
Recommendations
Report and dashboard
Project structure
How to run
Limitations
Skills demonstrated
Future work
Project overview
A retail or payments business needs to know which categories and customer groups drive revenue so that marketing, product and risk teams can focus their effort. This project turns a raw transaction table into answers: where the money comes from, who spends how much, whether time or demographics matter, and how much of the revenue sits in a small number of large purchases.

Business questions
How much revenue is generated, and which categories drive it?
Do spending patterns differ by gender or age group?
Is there a monthly or weekday pattern?
How concentrated is revenue in large transactions and merchants?
Are the differences statistically significant, or just noise?
How clean is the data, and what can it not tell us?
Dataset
50,000 rows, 9 columns, no duplicates.

Column	Description
Customer ID	Customer identifier (50,000 unique values)
Name, Surname	Customer name
Gender	F or M (5,047 missing)
Birthdate	1948-11-02 to 2005-10-19
Transaction Amount	$5.01 to $2,999.88
Date	2023-01-01 to 2023-10-14 (287 days)
Merchant Name	36,939 distinct merchants
Category	Restaurant, Market, Travel, Electronics, Clothing, Cosmetic
Approach
Understand the data: types, ranges, missing values.
Clean: standardise column names, trim text, treat missing gender as Unknown (rows kept so revenue totals stay complete), check duplicates and invalid amounts (none found).
Engineer features: age at transaction, age group, month, weekday, weekend flag, and amount band (Low, Medium, High, Premium).
Summarise revenue, transaction count and average ticket by category, gender, age group, month, weekday and amount band.
Visualise: eight charts plus a one-page dashboard, and an interactive Power BI dashboard.
Validate differences with t-tests and ANOVA.
Interpret findings into recommendations and state limitations.
Key findings
Area	Result
Overall	$22.11M revenue, 50,000 transactions, average $442, median $182 (right-skewed)
Categories	Travel 58.4% and Electronics 19.9% of revenue, together 78%
Revenue driver	Ticket size, not volume: about 8,300 transactions per category, but Travel averages $1,540 versus $55 for Restaurant
Concentration	Top 10% of transactions = 47.8% of revenue; all 4,304 transactions above $1,500 are Travel and produce 43.6% of revenue
Gender and age	Average ticket only $434 to $451 across all groups
Time	Monthly revenue stays at $2.1M to $2.5M; no weekday effect
Merchants	89% of merchants appear once; top 10 merchants = 1.3% of revenue, so merchant rankings are not meaningful
Statistical validation
Differences between groups were tested at the 5% level (src/stats_tests.py).

Test	Method	p-value	Significant?
Spend by gender	Welch t-test	0.392	No
Spend by age group	One-way ANOVA	0.721	No
Spend by weekday	One-way ANOVA	0.219	No
Spend by month (Jan to Sep)	One-way ANOVA	0.515	No
The correlation between age and transaction amount is 0.003. Visible gaps, such as Monday having a higher average ticket than Tuesday, are within normal variation.

Recommendations
Prioritise Travel and Electronics in promotions, partnerships and fraud monitoring (78% of value).
Test cross-selling from Travel buyers into Electronics, and bundle low-ticket categories to raise basket size.
Avoid gender or age-targeted campaigns on this evidence, since spend is statistically identical across groups.
Add review rules for Premium transactions (over $1,500), the highest value-at-risk segment.
Capture gender at sign-up to cut the 10% missing rate.
Collect repeat-customer identifiers so retention and lifetime value can be measured.
Report and dashboard
Full written report: reports/Customer_Transaction_Analysis_Report.pdf (13 pages, Word version alongside). It covers methodology, data quality assessment, all findings with tables and charts, statistical validation, recommendations and SQL appendix.
Power BI dashboard: powerbi/Customer Transactions, Banking dashboard.pbix. Download and open in Power BI Desktop.
Summary tables: outputs/summary_tables.xlsx (one sheet per breakdown).
Project structure
customer-transaction-analysis/
├── data/
│   ├── raw/sample_dataset.csv            # original data
│   └── processed/cleaned_transactions.csv
├── src/
│   ├── analysis.py                       # cleaning, features, tables, charts
│   ├── dashboard.py                      # builds the one-page dashboard
│   └── stats_tests.py                    # t-test and ANOVA validation
├── sql/queries.sql                       # 7 SQL queries
├── powerbi/                              # Power BI dashboard (.pbix)
├── outputs/                              # summary tables (xlsx), test results (csv)
├── reports/                              # full report (DOCX and PDF)
├── requirements.txt
├── .gitignore
├── .gitattributes
└── LICENSE
How to run
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/analysis.py           # clean data, write tables and charts
python src/dashboard.py          # build the dashboard
python src/stats_tests.py        # run significance tests
SQL queries in sql/queries.sql use MySQL syntax; load data/processed/cleaned_transactions.csv into a transactions table to run them.

Limitations
Every Customer ID appears exactly once, so retention, RFM and lifetime value analysis are not possible.
Amounts in each category fall within fixed ranges and patterns are very uniform, with randomly generated names. The data appears synthetic, so results demonstrate method rather than real business behaviour.
No time of day, location, payment method or product detail.
October 2023 is a partial month (to 14 Oct) and is excluded from trend views.
Skills demonstrated
Data cleaning and quality checks | feature engineering | exploratory data analysis | KPI reporting | SQL (aggregations, window functions, CTEs) | hypothesis testing (t-test, ANOVA) | data visualisation and dashboard design | business storytelling | reproducible project structure and documentation

Future work
Repeat the analysis on data with repeat customers (RFM segmentation, churn, lifetime value).
Add anomaly detection to flag unusual high-value transactions.
Automate the pipeline for new monthly files.
Author
Gautam Kurpatwar | github.com/GK3210

Licensed under the MIT License.
