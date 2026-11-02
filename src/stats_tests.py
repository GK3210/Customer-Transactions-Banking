"""Statistical validation: are the observed differences in spend real or noise?"""
from pathlib import Path
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data/processed/cleaned_transactions.csv", parse_dates=["date"])

known = df[df.gender != "Unknown"]
f, m = (known[known.gender == g].amount for g in ("F", "M"))
rows = [
    ("Gender (Welch t-test, F vs M)", stats.ttest_ind(f, m, equal_var=False).pvalue),
    ("Age group (one-way ANOVA)", stats.f_oneway(*[x.amount for _, x in df.groupby("age_group", observed=True)]).pvalue),
    ("Weekday (one-way ANOVA)", stats.f_oneway(*[x.amount for _, x in df.groupby("weekday")]).pvalue),
    ("Month, Jan-Sep (one-way ANOVA)", stats.f_oneway(*[x.amount for _, x in df[df.month != "2023-10"].groupby("month")]).pvalue),
]
out = pd.DataFrame(rows, columns=["test", "p_value"]).round(3)
out["significant_at_5pct"] = out.p_value < 0.05
print(out.to_string(index=False))
print("Correlation age vs amount:", round(df.age.corr(df.amount), 4))
out.to_csv(ROOT / "outputs/statistical_tests.csv", index=False)
