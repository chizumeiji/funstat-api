import json
import os
import sys
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

DATA_FILE = Path(".github/traffic/data.json")
CHART_FILE = Path(".github/traffic/chart.png")

BG_PAGE = "#0d1117"
BG_PANEL = "#161b22"
BORDER = "#30363d"
TEXT_DIM = "#8b949e"
TEXT_MAIN = "#e6edf3"

COLOR_VIEWS = "#58a6ff"
COLOR_UNIQUE = "#3fb950"
COLOR_CLONES = "#bc8cff"
COLOR_CUNIQ = "#ffa657"


def load_existing() -> dict:
    if DATA_FILE.exists():
        with open(DATA_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"views": {}, "clones": {}}


def merge(existing: dict, new_views: list, new_clones: list) -> dict:
    for item in new_views:
        date = item["timestamp"][:10]
        existing["views"][date] = {
            "count": item["count"],
            "uniques": item["uniques"],
        }
    for item in new_clones:
        date = item["timestamp"][:10]
        existing["clones"][date] = {
            "count": item["count"],
            "uniques": item["uniques"],
        }
    return existing


def style_ax(ax) -> None:
    ax.set_facecolor(BG_PANEL)
    for spine in ax.spines.values():
        spine.set_color(BORDER)
    ax.tick_params(colors=TEXT_DIM, labelsize=9)
    ax.xaxis.label.set_color(TEXT_DIM)
    ax.yaxis.label.set_color(TEXT_DIM)
    ax.grid(axis="y", color=BORDER, linestyle="--", linewidth=0.5, alpha=0.6)
    ax.set_axisbelow(True)


def generate_chart(data: dict) -> None:
    all_dates = sorted(set(data["views"]) | set(data["clones"]))
    if not all_dates:
        return

    dates = [datetime.strptime(d, "%Y-%m-%d") for d in all_dates]
    views = [data["views"].get(d, {}).get("count", 0) for d in all_dates]
    v_uniq = [data["views"].get(d, {}).get("uniques", 0) for d in all_dates]
    clones = [data["clones"].get(d, {}).get("count", 0) for d in all_dates]
    c_uniq = [data["clones"].get(d, {}).get("uniques", 0) for d in all_dates]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 6), facecolor=BG_PAGE)
    fig.subplots_adjust(hspace=0.45)

    style_ax(ax1)
    ax1.fill_between(dates, views, alpha=0.2, color=COLOR_VIEWS)
    ax1.plot(dates, views, color=COLOR_VIEWS, linewidth=2, label="Views", marker="o", markersize=4)
    ax1.fill_between(dates, v_uniq, alpha=0.2, color=COLOR_UNIQUE)
    ax1.plot(dates, v_uniq, color=COLOR_UNIQUE, linewidth=2, label="Unique visitors", marker="o", markersize=4)
    ax1.set_title("Repository Views", color=TEXT_MAIN, fontsize=13, pad=10, fontweight="bold")
    ax1.legend(facecolor=BG_PANEL, labelcolor=TEXT_MAIN, framealpha=0.9, fontsize=9)
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    fig.autofmt_xdate(rotation=30, ha="right")

    style_ax(ax2)
    ax2.fill_between(dates, clones, alpha=0.2, color=COLOR_CLONES)
    ax2.plot(dates, clones, color=COLOR_CLONES, linewidth=2, label="Clones", marker="o", markersize=4)
    ax2.fill_between(dates, c_uniq, alpha=0.2, color=COLOR_CUNIQ)
    ax2.plot(dates, c_uniq, color=COLOR_CUNIQ, linewidth=2, label="Unique cloners", marker="o", markersize=4)
    ax2.set_title("Repository Clones", color=TEXT_MAIN, fontsize=13, pad=10, fontweight="bold")
    ax2.legend(facecolor=BG_PANEL, labelcolor=TEXT_MAIN, framealpha=0.9, fontsize=9)
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    fig.autofmt_xdate(rotation=30, ha="right")

    CHART_FILE.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(CHART_FILE, dpi=150, bbox_inches="tight", facecolor=BG_PAGE)
    plt.close()
    print(f"Chart saved → {CHART_FILE}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            incoming = json.load(f)
    else:
        incoming = json.loads(os.environ.get("TRAFFIC_DATA", "{}"))

    new_views = incoming.get("views", [])
    new_clones = incoming.get("clones", [])

    existing = load_existing()
    merged = merge(existing, new_views, new_clones)

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)

    generate_chart(merged)
