#!/usr/bin/env python3
"""Render the GitHub stats artwork from the API, in our own colours.

Why this exists: the profile used to embed github-readme-stats' public
instance, which is heavily rate-limited and silently serves a broken image
when it trips. These cards are generated in CI instead, so nothing outside
this repository can break them.

    python3 assets/stats.py <out_dir>          # needs GITHUB_TOKEN
    python3 assets/stats.py <out_dir> --demo   # sample data, for layout work
"""
import json
import os
import sys
import urllib.error
import urllib.request

from generate import MONO, R, SANS, T, card, esc

API = "https://api.github.com/graphql"

QUERY = """
query($login:String!, $after:String) {
  user(login:$login) {
    followers { totalCount }
    pullRequests { totalCount }
    contributionsCollection {
      totalCommitContributions
      contributionCalendar {
        weeks { contributionDays { date weekday contributionCount } }
      }
    }
    repositories(first:100, after:$after, ownerAffiliations:OWNER, isFork:false) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes {
        stargazerCount
        languages(first:12, orderBy:{field:SIZE, direction:DESC}) {
          edges { size node { name } }
        }
      }
    }
  }
}
"""

def _demo_calendar():
    """A year of plausible daily counts: quieter at weekends, a summer dip."""
    import math
    days = []
    for i in range(365):
        weekday = (i + 2) % 7
        season = 1.0 + 0.45 * math.sin(i / 58.0)
        base = 1.4 if weekday in (0, 6) else 5.2
        month = 9 + i // 30          # a window starting in October, as a real one would
        days.append({"weekday": weekday,
                     "ym": f"{2025 + month // 12}-{month % 12 + 1:02d}",
                     "count": max(0, round(base * season + (i % 5) - 2))})
    return days


DEMO = {
    "repos": 34, "stars": 218, "commits": 1247, "prs": 96, "followers": 57,
    "calendar": _demo_calendar(),
    "languages": [("C#", 512000), ("TypeScript", 244000), ("HTML", 131000),
                  ("CSS", 96000), ("JavaScript", 74000), ("Python", 41000),
                  ("Dockerfile", 12000), ("Shell", 8000)],
}


def fetch(login, token):
    """Walk every owned, non-fork repository and fold it into one summary."""
    totals = {"repos": 0, "stars": 0, "commits": 0, "prs": 0, "followers": 0}
    langs, calendar, after = {}, [], None

    while True:
        req = urllib.request.Request(
            API,
            data=json.dumps({"query": QUERY,
                             "variables": {"login": login, "after": after}}).encode(),
            headers={"Authorization": f"bearer {token}",
                     "Content-Type": "application/json",
                     "User-Agent": "phuongfullstack-profile"},
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            payload = json.load(r)

        if payload.get("errors"):
            raise RuntimeError(f"GraphQL: {payload['errors']}")
        user = (payload.get("data") or {}).get("user")
        if not user:
            raise RuntimeError(f"no such user: {login}")

        totals["followers"] = user["followers"]["totalCount"]
        totals["prs"] = user["pullRequests"]["totalCount"]
        contrib = user["contributionsCollection"]
        totals["commits"] = contrib["totalCommitContributions"]
        if not calendar:
            for week in contrib["contributionCalendar"]["weeks"]:
                for day in week["contributionDays"]:
                    calendar.append({
                        "weekday": day["weekday"],
                        "ym": day["date"][:7],
                        "count": day["contributionCount"],
                    })
        repos = user["repositories"]
        totals["repos"] = repos["totalCount"]

        for node in repos["nodes"]:
            totals["stars"] += node["stargazerCount"]
            for edge in node["languages"]["edges"]:
                langs[edge["node"]["name"]] = langs.get(edge["node"]["name"], 0) + edge["size"]

        if not repos["pageInfo"]["hasNextPage"]:
            break
        after = repos["pageInfo"]["endCursor"]

    ranked = sorted(langs.items(), key=lambda kv: kv[1], reverse=True)
    return {**totals, "languages": ranked[:8], "calendar": calendar}


def compact(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M".replace(".0M", "M")
    if n >= 10_000:
        return f"{n/1000:.0f}k"
    if n >= 1000:
        return f"{n/1000:.1f}k".replace(".0k", "k")
    return str(n)


def render_stats(data, out):
    """A KPI row — five headline numbers. Not a chart: five magnitudes with no
    shared scale have nothing to compare against each other."""
    W, PAD = 1280, 56
    tiles = [(compact(data["repos"]), "REPOSITORIES"),
             (compact(data["stars"]), "TOTAL STARS"),
             (compact(data["commits"]), "COMMITS / YEAR"),
             (compact(data["prs"]), "PULL REQUESTS"),
             (compact(data["followers"]), "FOLLOWERS")]
    col = (W - PAD * 2) / len(tiles)
    H = 176
    parts = [f'    <text x="{PAD}" y="{PAD + 4}" font-family="{MONO}" font-size="11.5"'
             f' font-weight="600" fill="{T["text-faint"]}" letter-spacing="2.6">GITHUB</text>']
    for i, (value, label) in enumerate(tiles):
        x = PAD + col * i
        parts.append(
            f'    <text x="{x:.0f}" y="{H - 62}" font-family="{SANS}" font-size="40"'
            f' font-weight="700" fill="{T["text"]}" letter-spacing="-1.4">{esc(value)}</text>'
            f'<text x="{x:.0f}" y="{H - 38}" font-family="{MONO}" font-size="11"'
            f' font-weight="600" fill="{T["text-faint"]}" letter-spacing="1.8">{esc(label)}</text>')
        if i:
            parts.append(f'    <rect x="{x - 24:.0f}" y="{H - 104}" width="1" height="56"'
                         f' fill="{T["border"]}"/>')
    alt = "GitHub statistics: " + ", ".join(f"{v} {l.lower()}" for v, l in tiles)
    out.write_text(card(W, H, "\n".join(parts), label=alt))


def render_languages(data, out):
    """Ranked horizontal bars off one baseline. The reader's job here is to
    compare magnitudes, which a common baseline does far better than a stacked
    bar; one series carries its identity in the row label, so a single accent
    is correct and no legend is needed. Colouring by rank would repaint every
    bar whenever the ranking shifts."""
    W, PAD = 1280, 56
    rows = data["languages"]
    total = sum(size for _, size in rows) or 1
    label_w, pct_w, pitch, bar_h = 168, 62, 34, 14
    base_x = PAD + label_w
    track = W - PAD - pct_w - base_x
    top = PAD + 34
    H = top + len(rows) * pitch + PAD - (pitch - bar_h) + 6

    parts = [f'    <text x="{PAD}" y="{PAD + 4}" font-family="{MONO}" font-size="11.5"'
             f' font-weight="600" fill="{T["text-faint"]}" letter-spacing="2.6">MOST USED LANGUAGES</text>']
    biggest = rows[0][1] if rows else 1
    for i, (name, size) in enumerate(rows):
        y = top + i * pitch
        pct = size / total * 100
        w = max(4.0, track * (size / biggest))
        r = min(4.0, w)
        # square where it meets the baseline, rounded at the data end
        path = (f"M{base_x} {y} H{base_x + w - r:.1f} A{r} {r} 0 0 1 {base_x + w:.1f} {y + r:.1f}"
                f" V{y + bar_h - r:.1f} A{r} {r} 0 0 1 {base_x + w - r:.1f} {y + bar_h}"
                f" H{base_x} Z")
        parts.append(
            f'    <text x="{PAD}" y="{y + bar_h - 2}" font-family="{SANS}" font-size="13.5"'
            f' font-weight="500" fill="{T["text"]}">{esc(name)}</text>'
            f'<path d="{path}" fill="{T["accent"]}"/>'
            f'<text x="{base_x + w + 12:.1f}" y="{y + bar_h - 2}" font-family="{MONO}"'
            f' font-size="12" font-weight="500" fill="{T["text-muted"]}">{pct:.1f}%</text>')

    alt = "Most used languages: " + ", ".join(
        f"{n} {s / total * 100:.1f}%" for n, s in rows)
    out.write_text(card(W, round(H), "\n".join(parts), label=alt))



MONTHS = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
WEEKDAYS = ["S", "M", "T", "W", "T", "F", "S"]


def render_activity(data, out):
    """Two panels on one card.

    Left: contributions over the last twelve months. The job is a trend over
    time, so it is a line with a wash of area underneath — one series, so no
    legend, and only the peak is labelled rather than every point.

    Right: the same year folded onto the weekdays. That job is comparing
    magnitudes, so it is columns off a common baseline."""
    W, PAD = 1280, 56
    H = 300
    days = data.get("calendar") or []
    if not days:
        out.write_text(card(W, 120,
            f'    <text x="{PAD}" y="70" font-family="{SANS}" font-size="15"'
            f' fill="{T["text-faint"]}">No contribution data available.</text>',
            label="No contribution data available"))
        return

    buckets, by_weekday = {}, [0] * 7
    for d in days:
        buckets[d["ym"]] = buckets.get(d["ym"], 0) + d["count"]
        by_weekday[d["weekday"]] += d["count"]
    ordered = sorted(buckets.items())[-12:]
    months = [ym for ym, _ in ordered]
    by_month = [v for _, v in ordered]

    split = 760
    plot_top, plot_bottom = PAD + 52, H - PAD - 26
    plot_h = plot_bottom - plot_top

    parts = [
        f'    <text x="{PAD}" y="{PAD + 4}" font-family="{MONO}" font-size="11.5"'
        f' font-weight="600" fill="{T["text-faint"]}" letter-spacing="2.6">CONTRIBUTIONS / LAST 12 MONTHS</text>',
        f'    <text x="{split + 40}" y="{PAD + 4}" font-family="{MONO}" font-size="11.5"'
        f' font-weight="600" fill="{T["text-faint"]}" letter-spacing="2.6">BY WEEKDAY</text>',
    ]

    # ── left panel: trend ────────────────────────────────────────────────
    peak = max(by_month) or 1
    left, right = PAD, split - 40
    step = (right - left) / max(1, len(by_month) - 1)
    pts = [(left + i * step, plot_bottom - (v / peak) * plot_h) for i, v in enumerate(by_month)]
    line = " ".join(("M" if i == 0 else "L") + f"{x:.1f} {y:.1f}" for i, (x, y) in enumerate(pts))
    area = line + f" L{pts[-1][0]:.1f} {plot_bottom} L{pts[0][0]:.1f} {plot_bottom} Z"

    parts.append(f'    <path d="{area}" fill="{T["accent"]}" fill-opacity="0.10"/>')
    parts.append(f'    <line x1="{left}" y1="{plot_bottom}" x2="{right:.1f}" y2="{plot_bottom}"'
                 f' stroke="{T["border"]}" stroke-width="1"/>')
    parts.append(f'    <path d="{line}" fill="none" stroke="{T["accent"]}" stroke-width="2"'
                 f' stroke-linejoin="round" stroke-linecap="round"/>')

    hi = by_month.index(peak)
    hx, hy = pts[hi]
    parts.append(f'    <circle cx="{hx:.1f}" cy="{hy:.1f}" r="4.5" fill="{T["accent"]}"'
                 f' stroke="{T["bg"]}" stroke-width="2"/>')
    parts.append(f'    <text x="{hx:.1f}" y="{hy - 14:.1f}" text-anchor="middle"'
                 f' font-family="{MONO}" font-size="12" font-weight="600"'
                 f' fill="{T["text"]}">{peak}</text>')
    for i, (x, _) in enumerate(pts):
        initial = MONTHS[int(months[i][5:7]) - 1]
        parts.append(f'    <text x="{x:.1f}" y="{plot_bottom + 20}" text-anchor="middle"'
                     f' font-family="{MONO}" font-size="11" fill="{T["text-faint"]}">{initial}</text>')

    # ── right panel: weekday columns ─────────────────────────────────────
    wmax = max(by_weekday) or 1
    wleft, wright = split + 40, W - PAD
    slot = (wright - wleft) / 7
    bar_w = min(24.0, slot - 14)
    for i, v in enumerate(by_weekday):
        h = max(3.0, (v / wmax) * plot_h)
        x = wleft + slot * i + (slot - bar_w) / 2
        y = plot_bottom - h
        r = min(4.0, h)
        path = (f"M{x:.1f} {plot_bottom} V{y + r:.1f} A{r} {r} 0 0 1 {x + r:.1f} {y:.1f}"
                f" H{x + bar_w - r:.1f} A{r} {r} 0 0 1 {x + bar_w:.1f} {y + r:.1f}"
                f" V{plot_bottom} Z")
        peak_day = v == wmax
        parts.append(f'    <path d="{path}" fill="{T["accent"]}"'
                     f' fill-opacity="{1 if peak_day else 0.42}"/>')
        parts.append(f'    <text x="{x + bar_w/2:.1f}" y="{plot_bottom + 20}" text-anchor="middle"'
                     f' font-family="{MONO}" font-size="11" fill="{T["text-faint"]}">{WEEKDAYS[i]}</text>')
    parts.append(f'    <line x1="{wleft:.1f}" y1="{plot_bottom}" x2="{wright}" y2="{plot_bottom}"'
                 f' stroke="{T["border"]}" stroke-width="1"/>')

    alt = ("Contributions by month: "
           + ", ".join(f"{months[i]} {v}" for i, v in enumerate(by_month))
           + ". By weekday: "
           + ", ".join(f"{WEEKDAYS[i]} {v}" for i, v in enumerate(by_weekday)))
    out.write_text(card(W, H, "\n".join(parts), label=alt))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out_dir = args[0] if args else "dist"
    demo = "--demo" in sys.argv

    if demo:
        data = DEMO
    else:
        token = os.environ.get("GITHUB_TOKEN")
        login = os.environ.get("GITHUB_LOGIN")
        if not token or not login:
            sys.exit("GITHUB_TOKEN and GITHUB_LOGIN must be set (or pass --demo)")
        try:
            data = fetch(login, token)
        except (urllib.error.URLError, RuntimeError, KeyError) as exc:
            sys.exit(f"could not read GitHub stats: {exc}")

    from pathlib import Path
    d = Path(out_dir)
    d.mkdir(parents=True, exist_ok=True)
    render_stats(data, d / "stats.svg")
    render_languages(data, d / "languages.svg")
    render_activity(data, d / "activity.svg")
    for f in ("stats.svg", "languages.svg", "activity.svg"):
        print(f"{f:16} {(d / f).stat().st_size:>6} bytes")


if __name__ == "__main__":
    main()
