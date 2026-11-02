"""Customer Transaction Analysis - cleaning, EDA, charts, summary tables."""
from pathlib import Path
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data/raw/sample_dataset.csv", parse_dates=["Birthdate", "Date"])

# ---------- 1. CLEANING ----------
df.columns = ["customer_id","first_name","surname","gender","birthdate","amount","date","merchant","category"]
df["gender"] = df["gender"].fillna("Unknown")
for c in ["first_name","surname","merchant","category"]:
    df[c] = df[c].str.strip()
assert df.duplicated().sum() == 0 and (df.amount > 0).all()

# ---------- 2. FEATURE ENGINEERING ----------
df["age"] = ((df.date - df.birthdate).dt.days // 365.25).astype(int)
df["age_group"] = pd.cut(df.age, [16,24,34,44,54,64,100],
                         labels=["17-24","25-34","35-44","45-54","55-64","65+"])
df["month"] = df.date.dt.to_period("M").astype(str)
df["weekday"] = df.date.dt.day_name()
df["is_weekend"] = df.date.dt.dayofweek >= 5
df["amount_band"] = pd.cut(df.amount, [0,100,500,1500,5000],
                           labels=["Low (<100)","Medium (100-500)","High (500-1500)","Premium (1500+)"])
df.to_csv(ROOT / "data/processed/cleaned_transactions.csv", index=False)

# ---------- 3. SUMMARY TABLES ----------
def agg(g):
    t = df.groupby(g, observed=True).amount.agg(transactions="count", revenue="sum", avg_ticket="mean").round(2)
    t["revenue_share_%"] = (t.revenue / df.amount.sum() * 100).round(1)
    return t
tables = {
 "by_category": agg("category").sort_values("revenue", ascending=False),
 "by_gender": agg("gender"),
 "by_age_group": agg("age_group"),
 "by_month": agg("month"),
 "by_weekday": agg("weekday").reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]),
 "by_amount_band": agg("amount_band"),
}
top_merch = (df.groupby("merchant").amount.agg(transactions="count", revenue="sum").round(2)
             .sort_values("revenue", ascending=False).head(10))
cat_age = df.pivot_table(index="age_group", columns="category", values="amount", aggfunc="sum", observed=True).round(0)
cat_gender = df.pivot_table(index="category", columns="gender", values="amount", aggfunc="mean").round(2)
with pd.ExcelWriter(ROOT / "outputs/summary_tables.xlsx") as w:
    for k,v in tables.items(): v.to_excel(w, sheet_name=k)
    top_merch.to_excel(w, sheet_name="top_merchants")
    cat_age.to_excel(w, sheet_name="category_x_age")
    cat_gender.to_excel(w, sheet_name="category_x_gender")

# ---------- 4. CHARTS ----------
plt.rcParams.update({"figure.figsize":(8,4.5),"axes.spines.top":False,"axes.spines.right":False,"font.size":10})
c1, c2 = "#1f77b4", "#ff7f0e"
def save(n): plt.tight_layout(); plt.savefig(ROOT / f"images/{n}.png", dpi=140); plt.close()

t = tables["by_category"]
ax = t.revenue.div(1e6).plot.bar(color=c1); ax.set_title("Revenue by Category (millions)"); ax.set_ylabel("Revenue ($M)"); plt.xticks(rotation=0); save("01_revenue_by_category")

ax = t.avg_ticket.plot.bar(color=c2); ax.set_title("Average Transaction Value by Category"); ax.set_ylabel("$"); plt.xticks(rotation=0); save("02_avg_ticket_by_category")

m = tables["by_month"].iloc[:-1]  # Oct is partial (to 14 Oct)
ax = m.revenue.div(1e6).plot(marker="o", color=c1); ax.set_title("Monthly Revenue, Jan-Sep 2023 (Oct excluded: partial)"); ax.set_ylabel("$M"); ax.set_ylim(0); save("03_monthly_revenue")

ax = tables["by_age_group"].revenue.div(1e6).plot.bar(color=c1); ax.set_title("Revenue by Age Group"); ax.set_ylabel("$M"); plt.xticks(rotation=0); save("04_revenue_by_age_group")

ax = cat_age.div(1e6).plot.bar(stacked=True, figsize=(9,5)); ax.set_title("Category Mix by Age Group ($M)"); plt.xticks(rotation=0); ax.legend(fontsize=8, ncol=3); save("05_category_mix_by_age")

ax = tables["by_weekday"].transactions.plot.bar(color=c2); ax.set_title("Transactions by Weekday"); plt.xticks(rotation=30); save("06_transactions_by_weekday")

fig, ax = plt.subplots(); ax.hist(df.amount, bins=60, color=c1); ax.set_title("Distribution of Transaction Amount (right-skewed)"); ax.set_xlabel("$"); save("07_amount_distribution")

df.boxplot(column="amount", by="category", grid=False); plt.suptitle(""); plt.title("Transaction Amount Spread by Category"); plt.xlabel(""); save("08_boxplot_by_category")

# ---------- 5. PRINT KEY NUMBERS ----------
pd.set_option("display.width",200)
print("TOTAL", df.amount.sum().round(0), "AVG", df.amount.mean().round(2), "MEDIAN", df.amount.median())
for k,v in tables.items(): print("\n",k); print(v)
print(top_merch.head(5)); print(cat_gender)
print(cat_age)
print("weekend share txn", df.is_weekend.mean().round(3), "rev", (df[df.is_weekend].amount.sum()/df.amount.sum()).round(3))
top10 = df.nlargest(int(len(df)*0.1),"amount").amount.sum()/df.amount.sum(); print("top10% txns share of revenue", top10.round(3))
print("merchants", df.merchant.nunique(), "max merchant txns", df.merchant.value_counts().max())
print("travel>1500 txns", (df[df.category=="Travel"].amount>1500).sum())
