"""Every chart and framework visual in the report, drawn with matplotlib.

Each function returns a 16:9 Figure so the same image works as a PDF page and a slide.
Colour rule: grey for data, Netflix red as the one accent; segments keep one fixed
hue each (validated for colour-blind separation) and are always direct-labelled.
"""
from datetime import date

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle

from . import content as C

# ---- style -------------------------------------------------------------------
RED = "#E50914"
INK = "#1A1A1A"
INK2 = "#5F5F5F"
MUTED = "#9A9A9A"
GRID = "#E6E6E6"
BAR = "#B8B8B8"
PANEL = "#F5F5F4"
SEGMENT_COLORS = {"Binge-Watcher": RED, "Casual Listener": "#1F77B4", "Regional Listener": "#C98500"}

_FONT = "Inter" if any("Inter" in f.name for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
plt.rcParams.update({
    "font.family": _FONT, "font.size": 12, "text.color": INK, "axes.labelcolor": INK2,
    "axes.edgecolor": MUTED, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": "white",
    "axes.facecolor": "white", "savefig.facecolor": "white",
})
W, H = 13.333, 7.5


def _fig(title, subtitle=None, source="Source: Netflix_Dataset.xlsx"):
    fig = plt.figure(figsize=(W, H))
    fig.text(0.05, 0.93, title, fontsize=22, fontweight="bold", color=INK, va="top")
    if subtitle:
        fig.text(0.05, 0.865, subtitle, fontsize=13.5, color=INK2, va="top")
    if source:
        fig.text(0.05, 0.03, source, fontsize=9.5, color=MUTED)
    fig.add_artist(Rectangle((0, 0.985), 1, 0.015, transform=fig.transFigure, color=RED))
    return fig


def _canvas(fig, rect=(0.05, 0.08, 0.9, 0.74)):
    ax = fig.add_axes(rect)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return ax


def _box(ax, x, y, w, h, fc="white", ec=MUTED, lw=1.2, r=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw))


def _wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    lines.append(cur)
    return "\n".join(lines)


def cover_page():
    """Dark title page with author, program and date; matches slide 1 of the deck."""
    dark, soft = "#141414", "#C8C8C8"
    fig = plt.figure(figsize=(W, H), facecolor=dark)
    fig.add_artist(Rectangle((0, 0.985), 1, 0.015, transform=fig.transFigure, color=RED))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(6, 88, C.COVER["label"], fontsize=15, color=RED, fontweight="bold", va="center")
    ax.text(6, 79, C.COVER["title"], fontsize=50, color="white", fontweight="bold", va="center")
    ax.text(6, 69, C.COVER["subtitle"], fontsize=20, color=soft, va="center")
    ax.plot([6, 94], [58, 58], color="#404040", lw=1)
    for k, (lab, val) in enumerate(C.COVER["details"]):
        y = 50 - k * 9.5
        ax.text(6, y, lab, fontsize=11.5, color=RED, fontweight="bold", va="center")
        ax.text(24, y, val, fontsize=19 if k == 0 else 16, color="white" if k == 0 else "#E0E0E0",
                fontweight="bold" if k == 0 else "normal", va="center")
    return fig


# ---- customer research (Sheet 1) ----------------------------------------------
def segment_overview(seg):
    fig = _fig("Binge-Watchers are the largest and most tech-comfortable segment",
               "Users per segment and their tech comfort level (Sheet 1, 10 users)")
    ax = fig.add_axes([0.16, 0.14, 0.32, 0.62])
    segs = list(seg["Segment"])
    ax.barh(segs[::-1], seg["Users"][::-1], color=[SEGMENT_COLORS[s] for s in segs[::-1]], height=0.5)
    for i, (s, n, a) in enumerate(zip(segs[::-1], seg["Users"][::-1], seg["AvgAge"][::-1])):
        ax.text(n + 0.08, i, f"{n} users  |  avg age {a}", va="center", fontsize=12, color=INK)
    ax.set_xlim(0, 6)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=12.5)
    ax.set_title("Users per segment", loc="left", fontsize=13, color=INK2, pad=12)

    ax2 = fig.add_axes([0.6, 0.14, 0.35, 0.62])
    levels = [("TechHigh", "High", RED), ("TechMedium", "Medium", "#F08A8F"), ("TechLow", "Low", "#D9D9D9")]
    left = [0] * len(seg)
    for col, lab, colr in levels:
        vals = list(seg[col])
        ax2.barh(segs[::-1], vals[::-1], left=left[::-1], color=colr, height=0.5, edgecolor="white", linewidth=2)
        for i, (v, l0) in enumerate(zip(vals[::-1], left[::-1])):
            if v:
                ax2.text(l0 + v / 2, i, f"{lab}\n{v}", ha="center", va="center", fontsize=10.5,
                         color="white" if colr == RED else INK)
        left = [a + b for a, b in zip(left, vals)]
    ax2.set_xticks([])
    ax2.spines["bottom"].set_visible(False)
    ax2.set_yticklabels([])
    ax2.tick_params(axis="y", length=0)
    ax2.set_title("Tech comfort (High / Medium / Low)", loc="left", fontsize=13, color=INK2, pad=12)
    return fig


def age_distribution(users):
    fig = _fig("The core audience is 22 to 45; Regional Listeners are the youngest",
               "Each dot is one user (Sheet 1); short bar = segment average, dashed line = overall average")
    ax = fig.add_axes([0.2, 0.15, 0.74, 0.6])
    segs = list(SEGMENT_COLORS)
    for i, s in enumerate(segs):
        g = users[users["Segment"] == s]
        ax.scatter(g["Age"], [i] * len(g), s=140, color=SEGMENT_COLORS[s], edgecolor="white", linewidth=2, zorder=3)
        for k, (_, r) in enumerate(g.sort_values("Age").iterrows()):
            off = 0.22 if k % 2 == 0 else -0.3
            ax.text(r["Age"], i + off, r["Name"].split()[0], ha="center", va="center", fontsize=9.5, color=INK2)
        ax.plot([g["Age"].mean()] * 2, [i - 0.12, i + 0.12], color=INK, lw=2)
        ax.text(46.5, i, f"avg {g['Age'].mean():.1f}", ha="left", va="center", fontsize=10.5, color=INK)
    mean = users["Age"].mean()
    ax.axvline(mean, color=MUTED, ls="--", lw=1)
    ax.text(mean + 0.3, 2.55, f"overall avg {mean:.1f}", fontsize=10, color=INK2)
    ax.set_yticks(range(3))
    ax.set_yticklabels(segs, fontsize=12.5)
    ax.set_ylim(-0.6, 2.8)
    ax.set_xlim(18, 50)
    ax.set_xlabel("Age (years)")
    ax.grid(axis="x", color=GRID)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    return fig


def _theme_bars(series, title, subtitle):
    fig = _fig(title, subtitle)
    ax = fig.add_axes([0.32, 0.16, 0.6, 0.58])
    s = series.sort_values()
    colors = [BAR] * len(s)
    colors[-1] = RED
    ax.barh(s.index, s.values, color=colors, height=0.55)
    for i, v in enumerate(s.values):
        ax.text(v + 0.06, i, f"{v} of 10 users", va="center", fontsize=12)
    ax.set_xlim(0, max(s.values) + 1.5)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=13)
    return fig


def pain_themes(pain):
    return _theme_bars(pain, "Discovery is the most common pain point (4 of 10 users)",
                       "Users per pain-point theme; each user's pain point from Sheet 1 is assigned to one theme")


def motivation_themes(motive):
    return _theme_bars(motive, "Exclusive content and a better experience drive payment equally",
                       "Users per purchase-motivation theme (Sheet 1); exclusives and experience tie at 4 each")


def persona_card(p, users):
    seg = p["segment"]
    colr = SEGMENT_COLORS[seg]
    fig = _fig(f"Persona: {p['name']}", f"Built from {p['based_on']} (Sheet 1)")
    ax = _canvas(fig)
    _box(ax, 0, 0, 30, 100, fc=PANEL, ec=PANEL)
    from matplotlib.patches import Ellipse
    ax.add_patch(Ellipse((15, 76), 22 * (0.74 * H) / (0.9 * W), 22, color=colr))
    ax.text(15, 76, p["name"].split()[0][0], ha="center", va="center", fontsize=40, color="white", fontweight="bold")
    ax.text(15, 58, p["name"], ha="center", fontsize=14, fontweight="bold")
    ax.text(15, 52, seg, ha="center", fontsize=12, color=colr, fontweight="bold")
    ax.text(15, 45, p["profile"].replace(" | ", "\n"), ha="center", va="top", fontsize=11, color=INK2)
    ax.text(15, 26, _wrap(f"“{p['quote']}”", 30), ha="center", va="top", fontsize=11.5,
            style="italic", color=INK)
    ax.text(15, 4, "Quote is illustrative", ha="center", fontsize=8.5, color=MUTED)
    blocks = [("Listens to", p["listens"]), ("Goals", p["goals"]), ("Features wanted", p["wants"]),
              ("Pain points", p["pains"]), ("Would pay for", p["pays_for"])]
    y = 97
    for head, body in blocks:
        ax.text(34, y, head.upper(), fontsize=10.5, color=colr, fontweight="bold", va="top")
        ax.text(34, y - 4.5, _wrap(body, 95), fontsize=12.5, va="top", color=INK)
        y -= 19.5
    return fig


# ---- journeys (Sheet 2) -------------------------------------------------------
def journey_map(seg, journey_df):
    colr = SEGMENT_COLORS[seg]
    j = C.JOURNEYS[seg]
    persona = next(p for p in C.PERSONAS if p["segment"] == seg)
    fig = _fig(f"Journey map: {persona['name']}",
               "Behaviour from Sheet 2; touchpoints, emotions, pain points and opportunities inferred from Sheets 1 and 2")
    ax = _canvas(fig, (0.03, 0.05, 0.94, 0.76))
    behaviours = list(journey_df[seg])
    rows = [("Behaviour\n(Sheet 2)", behaviours), ("Touchpoint", j["touchpoint"]), ("Emotion", None),
            ("Pain point", j["pain"]), ("Opportunity", j["opportunity"])]
    x0, colw = 13, 21.7
    for k, st in enumerate(C.STAGES):
        _box(ax, x0 + k * colw + 0.3, 93, colw - 0.6, 6.5, fc=colr, ec=colr, r=0.8)
        ax.text(x0 + k * colw + colw / 2, 96.2, st, ha="center", va="center", color="white", fontsize=12.5, fontweight="bold")
    heights = [19, 13, 20, 16, 19]
    y = 92
    for (label, vals), h in zip(rows, heights):
        y -= h
        ax.text(0.5, y + h / 2, label, va="center", fontsize=11.5, fontweight="bold", color=INK)
        ax.plot([0, 100], [y, y], color=GRID, lw=1)
        if label == "Emotion":
            xs = [x0 + k * colw + colw / 2 for k in range(4)]
            ys = [y + 3 + (s - 1) / 4 * (h - 9) for s in j["emotion_score"]]
            ax.plot(xs, ys, color=colr, lw=2)
            for xx, yy, s, word in zip(xs, ys, j["emotion_score"], j["emotion"]):
                ax.scatter([xx], [yy], s=90, color=colr if s >= 3 else "white", edgecolor=colr, lw=2, zorder=3)
                ax.text(xx, yy + 2.2, word, ha="center", fontsize=10, color=INK)
            continue
        for k, v in enumerate(vals):
            fc = "#FDECEC" if label == "Pain point" else ("#EAF6EA" if label == "Opportunity" else "white")
            _box(ax, x0 + k * colw + 0.4, y + 0.8, colw - 0.8, h - 1.6, fc=fc, ec=GRID, r=0.8)
            ax.text(x0 + k * colw + 1.2, y + h - 2, _wrap(v, 30), va="top", fontsize=10.5, color=INK)
    ax.text(0.5, y - 3, "Emotion: filled dot = positive, open dot = negative.", fontsize=9.5, color=MUTED)
    return fig


def journey_insights():
    fig = _fig("Engagement is where all three journeys are at risk",
               "Cross-journey insights from the three journey maps", source=None)
    ax = _canvas(fig)
    for i, t in enumerate(C.JOURNEY_INSIGHTS):
        y = 82 - i * 23
        _box(ax, 0, y - 8, 100, 18, fc=PANEL, ec=PANEL)
        ax.text(4, y + 1, str(i + 1), fontsize=28, color=RED, fontweight="bold", va="center")
        ax.text(10, y + 1, t, fontsize=15, va="center", color=INK)
    return fig


# ---- idea funnel ----------------------------------------------------------------
def idea_funnel():
    fig = _fig("Twenty ideas narrowed to five MVP features",
               "Idea Funnel: screen for user need, merge overlaps, select for the MVP", source="Source: report analysis of Sheets 1 and 2")
    ax = _canvas(fig, (0.05, 0.08, 0.9, 0.74))
    top = C.FUNNEL[0][1]
    y = 92
    for i, (name, n, why) in enumerate(C.FUNNEL):
        w = 60 * n / top
        cx = 32
        colr = RED if i == len(C.FUNNEL) - 1 else ["#D0D0D0", "#BDBDBD", "#A8A8A8"][min(i, 2)]
        ax.add_patch(Rectangle((cx - w / 2, y - 17), w, 15, color=colr))
        ax.text(cx, y - 9.5, str(n), ha="center", va="center", fontsize=22, fontweight="bold",
                color="white" if i == len(C.FUNNEL) - 1 else INK)
        ax.text(65, y - 7, name, fontsize=15, fontweight="bold", va="center")
        ax.text(65, y - 12.5, why, fontsize=12, color=INK2, va="center")
        if i:
            prev = C.FUNNEL[i - 1][1]
            ax.text(cx + 32, y + 0.5, f"{n / prev:.0%} carried on", fontsize=10, color=MUTED, va="center", ha="right")
        y -= 23
    return fig


def idea_table():
    fig = _fig("Every idea traced to a user need, and its outcome",
               "Idea Funnel detail: 5 MVP, 7 later phases, 3 merged, 5 dropped", source="Source: report analysis of Sheets 1 and 2")
    ax = _canvas(fig, (0.04, 0.05, 0.92, 0.76))
    cols = [(0, "Idea"), (42, "Need it addresses"), (82, "Outcome")]
    for x, t in cols:
        ax.text(x, 98, t, fontsize=11.5, fontweight="bold", color=INK2)
    rowh = 4.7
    for i, (idea, need, out) in enumerate(C.IDEAS):
        y = 93 - i * rowh
        if i % 2 == 0:
            ax.add_patch(Rectangle((-0.5, y - rowh / 2 - 0.3), 101, rowh, color=PANEL, lw=0))
        ax.text(0, y, idea, fontsize=10.5, va="center")
        ax.text(42, y, need, fontsize=10.5, va="center", color=INK2)
        colr = RED if out == "MVP" else (MUTED if out in ("Dropped", "Merged") else INK)
        ax.text(82, y, out, fontsize=10.5, va="center", color=colr, fontweight="bold" if out == "MVP" else "normal")
    return fig


# ---- competition --------------------------------------------------------------
def competitor_heatmap():
    fig = _fig("Netflix Music would lead on exclusives but trail on catalogue",
               "Qualitative rating, 1 (weak) to 5 (strong); analyst judgement as of 2026, not dataset values",
               source="Source: report analysis (general market knowledge)")
    ax = fig.add_axes([0.2, 0.1, 0.74, 0.68])
    dims = list(C.BENCHMARK)
    import numpy as np
    m = np.array([C.BENCHMARK[d] for d in dims])
    ax.imshow(m, cmap=matplotlib.colors.LinearSegmentedColormap.from_list("r", ["#FFFFFF", "#F6B3B6", RED]),
              vmin=1, vmax=5, aspect="auto")
    for i in range(m.shape[0]):
        for k in range(m.shape[1]):
            ax.text(k, i, m[i, k], ha="center", va="center", fontsize=15, fontweight="bold",
                    color="white" if m[i, k] >= 4 else INK)
    ax.set_xticks(range(4))
    ax.set_xticklabels(C.COMPETITORS, fontsize=13)
    ax.xaxis.tick_top()
    ax.set_yticks(range(len(dims)))
    ax.set_yticklabels(dims, fontsize=12.5)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([x - 0.5 for x in range(1, 4)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(dims))], minor=True)
    ax.grid(which="minor", color="white", lw=3)
    ax.get_xticklabels()[3].set_fontweight("bold")
    ax.get_xticklabels()[3].set_color(RED)
    return fig


def swot():
    fig = _fig("SWOT: strengths in owned IP and data, weakness in licensing",
               "Strategy: use franchises and viewing data to attack discovery and exclusive-content gaps (SO)",
               source="Source: report analysis")
    ax = _canvas(fig)
    quads = [("Strengths", 0, 51, "#EAF6EA", "#2E7D32"), ("Weaknesses", 51, 51, "#FDECEC", RED),
             ("Opportunities", 0, 0, "#EAF1FA", "#1F5F99"), ("Threats", 51, 0, "#FFF4E0", "#A86A00")]
    for name, x, y, fc, ec in quads:
        _box(ax, x, y, 49, 49, fc=fc, ec=fc)
        ax.text(x + 2.5, y + 44, name.upper(), fontsize=14, fontweight="bold", color=ec, va="center")
        for i, item in enumerate(C.SWOT[name]):
            ax.text(x + 2.5, y + 35 - i * 9, "•  " + item, fontsize=12.5, va="center", color=INK)
    return fig


def bcg_matrix():
    fig = _fig("BCG: Netflix Music starts as a Question Mark; exclusives are the path to Star",
               "Audio streaming market, positions are qualitative (analyst judgement)", source="Source: report analysis")
    ax = fig.add_axes([0.06, 0.1, 0.5, 0.72])
    ax.set_xlim(1, 0)
    ax.set_ylim(0, 1)
    for (x, y, lab) in [(0.75, 0.97, "STARS"), (0.25, 0.97, "QUESTION MARKS"), (0.75, 0.47, "CASH COWS"), (0.25, 0.47, "DOGS")]:
        ax.text(x, y, lab, ha="center", va="top", fontsize=11, color=INK2, fontweight="bold")
    ax.axhline(0.5, color=MUTED, lw=1)
    ax.axvline(0.5, color=MUTED, lw=1)
    for name, sh, gr, _ in C.BCG_MARKET:
        nf = name == "Netflix Music"
        ax.scatter(sh, gr, s=420 if nf else 260, color=RED if nf else BAR, edgecolor="white", lw=2, zorder=3)
        ax.text(sh, gr - 0.075, name, ha="center", fontsize=12, fontweight="bold" if nf else "normal",
                color=RED if nf else INK)
    ax.annotate("", xy=(0.72, 0.82), xytext=(0.2, 0.8),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.6, ls="--"))
    ax.text(0.46, 0.85, "lead with exclusive audio", ha="center", fontsize=10.5, color=RED)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("Relative market share  (high ← → low)", fontsize=11.5)
    ax.set_ylabel("Market growth  (low → high)", fontsize=11.5)
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_color(MUTED)
    ax2 = _canvas(fig, (0.6, 0.1, 0.37, 0.72))
    ax2.text(0, 98, "Inside Netflix's portfolio", fontsize=13.5, fontweight="bold", va="top")
    for i, (biz, pos, strat) in enumerate(C.BCG_PORTFOLIO):
        y = 84 - i * 22
        _box(ax2, 0, y - 16, 100, 19, fc=PANEL, ec=PANEL)
        ax2.text(3, y, biz, fontsize=12.5, fontweight="bold", va="top")
        ax2.text(97, y, pos, fontsize=11, color=RED if "Star" in pos or "Question" in pos else INK2, ha="right", va="top")
        ax2.text(3, y - 6, _wrap(strat, 50), fontsize=10.5, color=INK2, va="top")
    return fig


# ---- prioritization (Sheet 3) -------------------------------------------------
def _short(f):
    return {"AI-Generated Personalized Playlists": "AI-generated playlists",
            "Music Discovery Based on Netflix Watch History": "Watch-history discovery",
            "Mood-Based Music Recommendations": "Mood-based recommendations",
            "Social Sharing and Collaborative Playlists": "Social and collaborative playlists",
            "Podcast + Music Hybrid Experience": "Podcast + music hybrid"}.get(f, f)


def _score_bars(scores, col, title, subtitle, fmt):
    fig = _fig(title, subtitle)
    ax = fig.add_axes([0.3, 0.14, 0.62, 0.62])
    s = scores.sort_values(col)
    top2 = set(scores.nlargest(2, col)["Feature"]) if col == "RICE" else set(scores[scores[col] == scores[col].max()]["Feature"])
    ax.barh([_short(f) for f in s["Feature"]], s[col], color=[RED if f in top2 else BAR for f in s["Feature"]], height=0.55)
    for i, v in enumerate(s[col]):
        ax.text(v * 1.01, i, fmt(v), va="center", fontsize=12.5)
    ax.set_xlim(0, s[col].max() * 1.2)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="y", length=0, labelsize=13)
    return fig


def rice_chart(scores):
    return _score_bars(scores, "RICE", "AI playlists and watch-history discovery lead RICE by about 2x",
                       "RICE = Reach x Impact x Confidence / Effort (Sheet 3)", lambda v: f"{v:,.0f}")


def wsjf_chart(scores):
    return _score_bars(scores, "WSJF", "The same two features tie for first on WSJF (4.8)",
                       "WSJF = (Business Value + Time Criticality + Risk Reduction) / Effort (Sheet 3)", lambda v: f"{v:.2f}")


def value_effort(scores):
    fig = _fig("The MVP features deliver the most value for the least effort",
               "Value vs effort: RICE score against effort (Sheet 3); dot size = reach")
    ax = fig.add_axes([0.1, 0.14, 0.82, 0.62])
    for _, r in scores.iterrows():
        top = r["RICE_rank"] <= 2
        ax.scatter(r["Effort"], r["RICE"], s=r["Reach"] / 150, color=RED if top else BAR, edgecolor="white", lw=2, zorder=3, alpha=0.9)
    labels = {"AI-Generated Personalized Playlists": (0.15, 4000, "left"),
              "Music Discovery Based on Netflix Watch History": (0.15, -14000, "left"),
              "Mood-Based Music Recommendations": (0.2, 9000, "left"),
              "Social Sharing and Collaborative Playlists": (0.2, 9000, "left"),
              "Podcast + Music Hybrid Experience": (0.15, -16000, "left")}
    for _, r in scores.iterrows():
        dx, dy, ha = labels[r["Feature"]]
        ax.text(r["Effort"] + dx, r["RICE"] + dy, f"{_short(r['Feature'])}\nRICE {r['RICE']:,}  |  WSJF {r['WSJF']}",
                fontsize=11, ha=ha, color=INK)
    ax.axvspan(4.2, 5.8, color=PANEL, zorder=0)
    ax.text(5.0, 4000, "Quick wins: high value, low effort", fontsize=10.5, color=INK2, ha="center")
    ax.set_xlim(4, 9)
    ax.set_ylim(0, 170000)
    ax.set_xlabel("Effort (Sheet 3 scale, higher = more work)")
    ax.set_ylabel("RICE score")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v / 1000:.0f}k"))
    ax.grid(color=GRID)
    return fig


def priority_matrix(scores):
    fig = _fig("All four frameworks agree on the launch order",
               "Combined ranking: RICE and WSJF from Sheet 3; Kano and MoSCoW reasoned from personas and journeys")
    ax = _canvas(fig, (0.04, 0.06, 0.92, 0.74))
    heads = [(0, "Rank"), (6, "Feature"), (42, "RICE"), (52, "WSJF"), (61, "Kano"), (78, "MoSCoW"), (91, "Phase")]
    for x, t in heads:
        ax.text(x, 95, t, fontsize=12, fontweight="bold", color=INK2)
    for i, r in scores.iterrows():
        y = 82 - i * 16
        top = r["RICE_rank"] <= 2
        _box(ax, -0.5, y - 6.5, 101, 13, fc="#FDECEC" if top else PANEL, ec="#FDECEC" if top else PANEL)
        f = r["Feature"]
        ax.text(1.5, y, str(i + 1), fontsize=20, fontweight="bold", color=RED if top else INK2, va="center")
        ax.text(6, y, _wrap(f, 36), fontsize=12, va="center")
        ax.text(42, y, f"{r['RICE']:,}\n#{r['RICE_rank']}", fontsize=11.5, va="center")
        ax.text(52, y, f"{r['WSJF']}\n#{r['WSJF_rank']}{' (tie)' if (scores['WSJF'] == r['WSJF']).sum() > 1 else ''}", fontsize=11.5, va="center")
        ax.text(61, y, _wrap(C.KANO[f], 18), fontsize=11.5, va="center")
        ax.text(78, y, C.MOSCOW[f], fontsize=11.5, va="center", fontweight="bold" if top else "normal", color=RED if top else INK)
        ax.text(91, y, _wrap(C.PHASE[f], 10), fontsize=11.5, va="center")
    return fig


def kano_chart():
    fig = _fig("Kano model: watch-history discovery is the delighter",
               "How each feature affects satisfaction; positions are analyst judgement", source="Source: report analysis")
    ax = fig.add_axes([0.08, 0.12, 0.52, 0.7])
    import numpy as np
    x = np.linspace(0, 1, 100)
    ax.plot(x, -1 + 0.95 * (1 - np.exp(-5 * x)), color=INK2, lw=2)
    ax.plot(x, -0.9 + 1.8 * x, color="#1F77B4", lw=2)
    ax.plot(x, 0.05 + 0.95 * (np.exp(3 * x) - 1) / (np.e ** 3 - 1), color=RED, lw=2)
    ax.text(1.01, -0.08, "Must-be", color=INK2, fontsize=11.5, va="center")
    ax.text(1.01, 0.9, "Performance", color="#1F77B4", fontsize=11.5, va="center")
    ax.text(1.01, 1.0 + 0.1, "Attractive", color=RED, fontsize=11.5, va="center")
    ax.axhline(0, color=MUTED, lw=1)
    ax.set_xlim(0, 1.25)
    ax.set_ylim(-1.1, 1.25)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("Feature implemented / works well →")
    ax.set_ylabel("Satisfaction →")
    ax2 = _canvas(fig, (0.64, 0.12, 0.33, 0.7))
    rows = [("Attractive", ["Watch-history discovery", "Podcast + music hybrid (niche)", "Karaoke mode"], RED),
            ("Performance", ["AI-generated playlists", "Mood-based recommendations", "Ad-free, hi-fi audio"], "#1F77B4"),
            ("Must-be", ["Basic sharing", "Offline listening", "Multi-device sync"], INK2)]
    y = 98
    for name, items, colr in rows:
        ax2.text(0, y, name.upper(), fontsize=12.5, color=colr, fontweight="bold", va="top")
        for k, it in enumerate(items):
            ax2.text(3, y - 8 - k * 7, "• " + it, fontsize=12, va="top")
        y -= 34
    return fig


# ---- roadmap ----------------------------------------------------------------------
def roadmap():
    fig = _fig("Roadmap: MVP in mid-2027, monetization at scale by end of 2028",
               "Four phases with deliverables and the gate each must pass; assumes a January 2027 kickoff",
               source="Source: report roadmap (timelines are planning assumptions)")
    ax = _canvas(fig, (0.03, 0.06, 0.94, 0.78))
    t0, t1 = date(2027, 1, 1).toordinal(), date(2029, 1, 1).toordinal()
    X = lambda d: 2 + 96 * (date.fromisoformat(d).toordinal() - t0) / (t1 - t0)
    shades = ["#E50914", "#EE5B62", "#F39A9E", "#F8C9CB"]
    for q in range(9):
        yr, mo = 2027 + q // 4, (q % 4) * 3 + 1
        if q == 8:
            yr, mo = 2029, 1
        xx = X(f"{yr}-{mo:02d}-01")
        ax.plot([xx, xx], [0, 92], color=GRID, lw=1, zorder=0)
        if q < 8:
            ax.text(xx + 12 / 2, 95, f"Q{q % 4 + 1} {yr}", ha="center", fontsize=10.5, color=INK2)
    for i, ph in enumerate(C.ROADMAP):
        x0, x1 = X(ph["start"]), X(ph["end"])
        _box(ax, x0 + 0.3, 80, x1 - x0 - 0.6, 9, fc=shades[i], ec=shades[i], r=0.8)
        ax.text(x0 + 1.2, 84.5, ph["phase"], fontsize=11.5, fontweight="bold", va="center",
                color="white" if i < 2 else INK)
        for k, d in enumerate(ph["deliverables"]):
            ax.text(x0 + 1.2, 75 - k * 10.5, _wrap("• " + d, 28), fontsize=9.5, va="top", color=INK, linespacing=1.15)
        ax.add_patch(Polygon([(x1, 14), (x1 + 1.3, 11), (x1, 8), (x1 - 1.3, 11)], color=INK))
        ax.text(x1 - 1.8, 11, _wrap("Gate: " + ph["gate"], 26), fontsize=9.5, ha="right", va="center", color=INK2)
    ax.text(X("2027-07-01"), 2, "Launch (Jul 2027)", ha="center", fontsize=10.5, color=RED, fontweight="bold")
    return fig


def kpi_board():
    fig = _fig("Success metrics and the year-one targets",
               "Targets are planning assumptions, to be validated in the closed beta", source="Source: report analysis")
    ax = _canvas(fig)
    for i, (goal, metric, target) in enumerate(C.KPIS):
        x = (i % 5) * 20
        _box(ax, x + 0.5, 30, 19, 60, fc=PANEL, ec=PANEL)
        ax.text(x + 10, 80, goal.upper(), ha="center", fontsize=11.5, color=INK2, fontweight="bold")
        ax.text(x + 10, 62, target, ha="center", fontsize=30 if len(target) < 5 else 22, color=RED, fontweight="bold")
        ax.text(x + 10, 50, _wrap(metric, 20), ha="center", va="top", fontsize=11.5)
    ax.text(0.5, 18, "Illustrative sizing: 5% of 300M+ members = ~15M users; 25% on a $4.99 add-on = ~3.75M subscribers,",
            fontsize=12, color=INK)
    ax.text(0.5, 11, "about $225M a year before ad revenue and churn savings. All inputs are assumptions.", fontsize=12, color=INK)
    return fig


# ---- product sense ---------------------------------------------------------------
def five_whys():
    fig = _fig("The art of why: five questions lead to Netflix's one unfair advantage",
               "Asking 'why' until the answer is something only Netflix can do", source="Source: report analysis of Sheets 1 and 2")
    ax = _canvas(fig, (0.05, 0.06, 0.9, 0.75))
    n = len(C.FIVE_WHYS)
    for i, (q, a) in enumerate(C.FIVE_WHYS):
        y = 100 - (i + 1) * 19.5
        last = i == n - 1
        _box(ax, 0, y, 100, 16.5, fc="#FDECEC" if last else PANEL, ec=RED if last else PANEL, lw=1.5 if last else 1)
        ax.text(2.5, y + 8.25, f"WHY {i + 1}", fontsize=12, fontweight="bold", color=RED, va="center")
        ax.text(11, y + 11.2, q, fontsize=14, fontweight="bold", va="center")
        ax.text(11, y + 4.8, a, fontsize=12.5, color=INK2 if not last else INK, va="center")
        if i < n - 1:
            ax.annotate("", xy=(5.5, y - 2.8), xytext=(5.5, y + 0.2), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2))
    return fig


def problem_definition():
    fig = _fig("Problem definition: no app connects what people watch with what they hear",
               "Problem statement built from the customer research", source="Source: Netflix_Dataset.xlsx, Sheets 1 and 2")
    ax = _canvas(fig, (0.05, 0.06, 0.9, 0.75))
    keys = ["Who", "Problem", "Evidence", "Why it matters (user)", "Why it matters (Netflix)"]
    y = 100
    for k in keys:
        h = 17 if k in ("Problem", "Evidence") else 12
        y -= h
        ax.text(0, y + h - 3, k.upper(), fontsize=11, fontweight="bold", color=RED, va="top")
        ax.text(24, y + h - 3, _wrap(C.PROBLEM[k], 105), fontsize=13, va="top", linespacing=1.35)
        ax.plot([0, 100], [y, y], color=GRID, lw=1)
    _box(ax, 0, 0, 100, y - 3, fc=RED, ec=RED)
    ax.text(3, (y - 3) / 2, "HOW MIGHT WE", fontsize=12, fontweight="bold", color="white", va="center")
    ax.text(21, (y - 3) / 2, C.PROBLEM["How might we"],
            fontsize=17, fontweight="bold", color="white", va="center")
    return fig


def jtbd_chart():
    fig = _fig("Jobs to be done: each segment hires the app for a different job",
               "When I ... I want to ... so I can ...  (from Sheet 1 motivations and Sheet 2 journeys)",
               source="Source: report analysis of Sheets 1 and 2")
    ax = _canvas(fig, (0.05, 0.08, 0.9, 0.74))
    for i, (seg, when, want, so) in enumerate(C.JTBD):
        x = i * 34
        colr = SEGMENT_COLORS[seg]
        _box(ax, x, 0, 32, 100, fc=PANEL, ec=PANEL)
        ax.add_patch(Rectangle((x, 94), 32, 6, color=colr))
        ax.text(x + 16, 97, seg, ha="center", va="center", fontsize=13.5, fontweight="bold", color="white")
        for j, (lab, txt) in enumerate([("WHEN I", when), ("I WANT TO", want), ("SO I CAN", so)]):
            yy = 84 - j * 28
            ax.text(x + 2.5, yy, lab, fontsize=11, fontweight="bold", color=colr, va="top")
            ax.text(x + 2.5, yy - 5, _wrap(txt, 30), fontsize=13.5, va="top", linespacing=1.3)
    return fig


def mvp_definition():
    fig = _fig("MVP: every feature answers a defined problem and tests one hypothesis",
               "Problem \u2192 MVP feature \u2192 hypothesis \u2192 success metric", source="Source: report analysis")
    ax = _canvas(fig, (0.04, 0.06, 0.92, 0.75))
    cols = [(0, 22, "Problem"), (25, 25, "MVP feature"), (53, 30, "Hypothesis to test"), (86, 14, "Success metric")]
    for x, w, t in cols:
        ax.text(x + 1, 97, t.upper(), fontsize=11, fontweight="bold", color=INK2)
    for i, row in enumerate(C.MVP_MAP):
        y = 72 - i * 23
        for k, ((x, w, _), txt) in enumerate(zip(cols, row)):
            fc = ["#FDECEC", RED, PANEL, PANEL][k]
            _box(ax, x, y, w, 19, fc=fc, ec=fc)
            ax.text(x + 1.2, y + 9.5, _wrap(txt, int(w * 1.15)), fontsize=12, va="center",
                    color="white" if k == 1 else INK, fontweight="bold" if k in (1, 3) else "normal")
            if k < 3:
                ax.annotate("", xy=(cols[k + 1][0] - 0.2, y + 9.5), xytext=(x + w + 0.2, y + 9.5),
                            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2))
    return fig


def mvp_scope():
    fig = _fig("MVP scope: build the core advantage first, defer the rest on purpose",
               "What is in the MVP, what waits, and why", source="Source: report analysis (RICE/WSJF from Sheet 3)")
    ax = _canvas(fig, (0.05, 0.06, 0.9, 0.75))
    _box(ax, 0, 0, 48, 100, fc="#FDECEC", ec="#FDECEC")
    _box(ax, 52, 0, 48, 100, fc=PANEL, ec=PANEL)
    ax.text(3, 93, "IN THE MVP", fontsize=14, fontweight="bold", color=RED, va="center")
    ax.text(55, 93, "NOT YET, AND WHY", fontsize=14, fontweight="bold", color=INK2, va="center")
    ins = [i[0] for i in C.IDEAS if i[2] == "MVP"]
    for k, t in enumerate(ins):
        ax.text(3, 80 - k * 15, "\u2713  " + t, fontsize=14, va="center")
    for k, (t, why) in enumerate(C.MVP_OUT):
        ax.text(55, 82 - k * 15, t, fontsize=13.5, fontweight="bold", va="center")
        ax.text(55, 76.5 - k * 15, why, fontsize=11.5, color=INK2, va="center")
    return fig


def all_figures(users, journey, seg, scores, pain, motive):
    """Ordered (name, caption, figure-builder) list shared by the PDF and the deck."""
    jdf = journey.set_index("Stage")
    items = [
        ("five_whys", "The art of why", five_whys),
        ("problem_definition", "Problem definition", problem_definition),
        ("segment_overview", "Customer segments and tech comfort", lambda: segment_overview(seg)),
        ("age_distribution", "Age distribution by segment", lambda: age_distribution(users)),
        ("pain_point_themes", "Pain-point themes", lambda: pain_themes(pain)),
        ("purchase_motivations", "Purchase motivations", lambda: motivation_themes(motive)),
    ]
    for p in C.PERSONAS:
        items.append((f"persona_{p['segment'].split()[0].lower()}", f"Persona: {p['name']}",
                      lambda p=p: persona_card(p, users)))
    items.append(("jobs_to_be_done", "Jobs to be done", jtbd_chart))
    for s_ in C.JOURNEYS:
        items.append((f"journey_{s_.split()[0].lower()}", f"Journey map: {s_}", lambda s_=s_: journey_map(s_, jdf)))
    items += [
        ("journey_insights", "Cross-journey insights", journey_insights),
        ("idea_funnel", "Idea Funnel", idea_funnel),
        ("idea_list", "Idea Funnel detail", idea_table),
        ("competitor_benchmark", "Competitor benchmark", competitor_heatmap),
        ("swot", "SWOT analysis", swot),
        ("bcg_matrix", "BCG matrix", bcg_matrix),
        ("rice", "RICE scores", lambda: rice_chart(scores)),
        ("wsjf", "WSJF scores", lambda: wsjf_chart(scores)),
        ("value_effort", "Value vs effort", lambda: value_effort(scores)),
        ("kano", "Kano model", kano_chart),
        ("combined_ranking", "Combined prioritization (RICE, WSJF, Kano, MoSCoW)", lambda: priority_matrix(scores)),
        ("mvp_definition", "MVP definition: problem to metric", mvp_definition),
        ("mvp_scope", "MVP scope: in and out", mvp_scope),
        ("roadmap", "Strategic roadmap", roadmap),
        ("kpis", "Success metrics", kpi_board),
    ]
    return [(f"{i + 1:02d}_{n}", c, b) for i, (n, c, b) in enumerate(items)]
