"""Load the Netflix dataset and compute every number used in the report.

Sheet 1 -> user segments, pain-point themes, purchase motivations
Sheet 2 -> journey stages per segment
Sheet 3 -> RICE and WSJF feature scores
"""
from collections import Counter
from pathlib import Path

import pandas as pd

DEFAULT_DATA = Path(__file__).resolve().parent.parent / "data" / "Netflix_Dataset.xlsx"

# Pain points and motivations grouped into themes (analyst judgement, see report section 3).
PAIN_THEMES = {
    "Limited Exclusive Content": "Content and language gaps",
    "Not Enough Regional Music": "Content and language gaps",
    "Limited Language Options": "Content and language gaps",
    "Difficult UI Navigation": "Discovery and personalization",
    "No Mood-Based Playlists": "Discovery and personalization",
    "Hard to Discover New Podcasts": "Discovery and personalization",
    "Not Enough Personalized Recommendations": "Discovery and personalization",
    "Limited Offline Access": "Access and continuity",
    "No Multi-Device Sync": "Access and continuity",
    "Too Many Ads": "Ads",
}

MOTIVATION_THEMES = {
    "Access to Exclusive Netflix Content": "Exclusive or curated content",
    "Curated Global Music": "Exclusive or curated content",
    "Access to Local Music": "Exclusive or curated content",
    "More Language Support": "Exclusive or curated content",
    "Ad-Free Experience": "Better listening experience",
    "Best Audio Quality": "Better listening experience",
    "Seamless Offline Mode": "Better listening experience",
    "Relaxing Music for Work": "Better listening experience",
    "Better Discovery Features": "Smarter features",
    "Interactive Music Features": "Smarter features",
}


def load(path=DEFAULT_DATA):
    """Return the three sheets as DataFrames: users, journey, features."""
    xl = pd.read_excel(path, sheet_name=None)
    users = xl["Sheet 1"].dropna(how="all")
    journey = xl["Sheet 2"].dropna(how="all")
    features = xl["Sheet 3"].dropna(how="all")
    return users, journey, features


def segment_summary(users):
    """One row per segment: size, age stats, gender split and tech comfort."""
    rows = []
    for seg, g in users.groupby("Segment", sort=False):
        tech = Counter(g["Tech Comfort Level"])
        rows.append({
            "Segment": seg,
            "Users": len(g),
            "AvgAge": round(g["Age"].mean(), 1),
            "MinAge": int(g["Age"].min()),
            "MaxAge": int(g["Age"].max()),
            "Female": int((g["Gender"] == "Female").sum()),
            "Male": int((g["Gender"] == "Male").sum()),
            "TechHigh": tech.get("High", 0),
            "TechMedium": tech.get("Medium", 0),
            "TechLow": tech.get("Low", 0),
        })
    return pd.DataFrame(rows)


def theme_counts(users):
    """Count users per pain-point theme and per purchase-motivation theme."""
    pain = users["Pain Points"].map(PAIN_THEMES).value_counts()
    motive = users["Purchase Motivation"].map(MOTIVATION_THEMES).value_counts()
    return pain, motive


def score_features(features):
    """Add RICE, cost of delay and WSJF columns, sorted by RICE (highest first)."""
    f = features.rename(columns={
        "Reach (R)": "Reach", "Impact (I)": "Impact", "Confidence (C)": "Confidence",
        "Effort (E)": "Effort", "Business Value (BV)": "BusinessValue",
        "Time Criticality (TC)": "TimeCriticality", "Risk Reduction (RR)": "RiskReduction",
    }).copy()
    f["RICE"] = (f["Reach"] * f["Impact"] * f["Confidence"] / f["Effort"]).round(0).astype(int)
    f["CostOfDelay"] = f["BusinessValue"] + f["TimeCriticality"] + f["RiskReduction"]
    f["WSJF"] = (f["CostOfDelay"] / f["Effort"]).round(2)
    f["RICE_rank"] = f["RICE"].rank(ascending=False, method="min").astype(int)
    f["WSJF_rank"] = f["WSJF"].rank(ascending=False, method="min").astype(int)
    return f.sort_values("RICE", ascending=False).reset_index(drop=True)


def export_tables(out_dir, path=DEFAULT_DATA):
    """Write the computed tables as CSV files and return them."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    users, journey, features = load(path)
    seg = segment_summary(users)
    scores = score_features(features)
    pain, motive = theme_counts(users)
    seg.to_csv(out_dir / "user_segments.csv", index=False)
    scores.to_csv(out_dir / "feature_scores.csv", index=False)
    pain.rename_axis("Theme").rename("Users").to_csv(out_dir / "pain_point_themes.csv")
    motive.rename_axis("Theme").rename("Users").to_csv(out_dir / "purchase_motivation_themes.csv")
    return users, journey, seg, scores, pain, motive


if __name__ == "__main__":
    u, j, f = load()
    print(segment_summary(u).to_string(index=False))
    print(score_features(f)[["Feature", "RICE", "WSJF", "RICE_rank", "WSJF_rank"]].to_string(index=False))
    p, m = theme_counts(u)
    print(p, m, sep="\n")
