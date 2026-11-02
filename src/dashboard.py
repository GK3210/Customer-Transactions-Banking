"""Builds a one-page dashboard image (KPI cards + 6 charts) from the cleaned data."""
from pathlib import Path
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data/processed/cleaned_transactions.csv", parse_dates=["date"])
NAVY, BLUE, ORANGE, GREY = "#1f3a5f", "#2a7de1", "#f28c28", "#6b7280"

fig = plt.figure(figsize=(16, 10), facecolor="#f4f6fa")
fig.text(0.03, 0.955, "Customer Transaction Dashboard", fontsize=22, fontweight="bold", color=NAVY)
fig.text(0.03, 0.925, "50,000 transactions | 1 Jan - 14 Oct 2023", fontsize=11, color=GREY)

# KPI cards
kpis = [("Total Revenue", f"${df.amount.sum()/1e6:.2f}M"), ("Transactions", f"{len(df):,}"),
        ("Avg Transaction", f"${df.amount.mean():,.0f}"), ("Median Transaction", f"${df.amount.median():,.0f}"),
        ("Travel Share", f"{df[df.category=='Travel'].amount.sum()/df.amount.sum()*100:.0f}%")]
for i, (lab, val) in enumerate(kpis):
    ax = fig.add_axes([0.03 + i*0.1925, 0.80, 0.18, 0.10]); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.08", fc="white", ec="#dfe4ee", transform=ax.transAxes))
    ax.text(0.5, 0.62, val, ha="center", va="center", fontsize=22, fontweight="bold", color=BLUE, transform=ax.transAxes)
    ax.text(0.5, 0.22, lab, ha="center", va="center", fontsize=10, color=GREY, transform=ax.transAxes)

def panel(pos, title):
    ax = fig.add_axes(pos, facecolor="white")
    ax.set_title(title, loc="left", fontsize=11, fontweight="bold", color=NAVY)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    return ax

cat = df.groupby("category").amount.agg(["sum", "mean"]).sort_values("sum")
ax = panel([0.09, 0.43, 0.25, 0.29], "Revenue by Category ($M)")
ax.barh(cat.index, cat["sum"]/1e6, color=BLUE)
for y, v in enumerate(cat["sum"]/1e6): ax.text(v + 0.15, y, f"{v:.1f}", va="center", fontsize=9)

ax = panel([0.39, 0.43, 0.27, 0.29], "Monthly Revenue ($M, Jan-Sep)")
m = (df.groupby(df.date.dt.to_period("M")).amount.sum()/1e6).iloc[:-1]  # Oct is partial
ax.plot(range(len(m)), m.values, marker="o", color=ORANGE)
ax.set_xticks(range(len(m))); ax.set_xticklabels([p.strftime("%b") for p in m.index], fontsize=9); ax.set_ylim(0, 3)

ax = panel([0.73, 0.43, 0.24, 0.29], "Revenue by Amount Band")
bands = df.groupby("amount_band").amount.sum().reindex(["Low (<100)", "Medium (100-500)", "High (500-1500)", "Premium (1500+)"])
ax.pie(bands, labels=["Low", "Medium", "High", "Premium"], autopct="%1.0f%%", startangle=90,
       colors=["#c9d8f0", "#8fb4ea", "#2a7de1", NAVY], textprops={"fontsize": 9}, wedgeprops={"width": 0.45})

ax = panel([0.05, 0.07, 0.27, 0.27], "Revenue by Age Group ($M)")
a = df.groupby("age_group").amount.sum()/1e6
ax.bar(a.index, a.values, color=BLUE); ax.tick_params(axis="x", labelsize=9)

ax = panel([0.39, 0.07, 0.27, 0.27], "Revenue Share by Gender")
g = df.groupby("gender").amount.sum()
ax.bar(g.index, g/g.sum()*100, color=[ORANGE, BLUE, "#9aa5b8"]); ax.set_ylabel("% of revenue")

ax = panel([0.73, 0.07, 0.24, 0.27], "Avg Ticket by Category ($)")
ax.bar(cat.index, cat["mean"], color=ORANGE); plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=8)

fig.savefig(ROOT / "images/dashboard.png", dpi=130, facecolor=fig.get_facecolor())
