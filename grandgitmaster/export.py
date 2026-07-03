"""Export the kingdom: machine-readable champions.json + human LEADERBOARD.md.

The GitHub Action commits these, so the repo itself is the always-fresh
leaderboard any project or agent can consume with one HTTP GET:

  https://raw.githubusercontent.com/<you>/GrandGitMaster/main/data/champions.json
"""

import datetime
import json
import os

from . import db


def export(con=None, out_dir=None):
    con = con or db.connect()
    out_dir = out_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(out_dir, exist_ok=True)

    champs = db.champions(con)
    cats = db.categories(con)
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    payload = {
        "generated_at": now,
        "stats": db.stats(con),
        "champions": champs,
        "categories": {c["category"]: [
            {k: r.get(k) for k in ("full_name", "url", "description", "score",
                                   "verdict", "flags", "stars", "language", "status")}
            for r in db.all_repos(con, category=c["category"])[:10]
        ] for c in cats},
    }
    champ_path = os.path.join(out_dir, "champions.json")
    with open(champ_path, "w") as f:
        json.dump(payload, f, indent=2, default=str)

    lines = [
        "# 👑 GrandGitMaster Leaderboard",
        "",
        "*The best Git repo for anything — auto-ranked by [the Ringer](../README.md#the-ringer). "
        "Updated %s.*" % now,
        "",
        "## Category Kings",
        "",
        "| 👑 | Category | Repo | GrandScore | Verdict | Why |",
        "|----|----------|------|-----------:|---------|-----|",
    ]
    for c in champs:
        flags = " · ".join(c.get("flags") or [])
        lines.append("| 👑 | %s | [%s](%s) | **%.1f** | %s | %s |" % (
            c["category"], c["full_name"], c["url"], c["score"], c["verdict"], flags))
    lines += ["", "## Full rankings by category", ""]
    for c in cats:
        rows = db.all_repos(con, category=c["category"])[:10]
        if not rows:
            continue
        lines += ["<details><summary><b>%s</b> (%d repos)</summary>" % (c["category"], c["n"]), ""]
        lines += ["| # | Repo | Score | Verdict | ⭐ |", "|---|------|------:|---------|---:|"]
        for i, r in enumerate(rows, 1):
            score = "%.1f" % r["score"] if r["status"] == "scored" else "⏳"
            lines.append("| %d | [%s](%s) | %s | %s | %s |" % (
                i, r["full_name"], r["url"], score, r.get("verdict") or "pending",
                r.get("stars") or ""))
        lines += ["", "</details>", ""]

    board_path = os.path.join(out_dir, "LEADERBOARD.md")
    with open(board_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return champ_path, board_path
