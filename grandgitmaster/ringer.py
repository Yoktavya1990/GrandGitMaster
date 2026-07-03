"""The Ringer — every repo goes through it, the best come out crowned.

GrandScore: 0-100, built from six transparent components. Designed so that
non-coders and vibe coders can trust the number without reading the code:

  popularity   0-25  do people love it? (stars, log scale)
  freshness    0-20  is it alive? (days since last push)
  maintenance  0-15  is it looked after? (not archived, issue load sane)
  community    0-10  do people build on it? (forks, log scale)
  docs         0-15  will a human understand it? (description, license,
                     topics, homepage)
  one-click    0-15  can you run it NOW? (Dockerfile, compose, lockfiles,
                     installers found at repo root)

Verdicts translate the number into plain language, and flags call out what
matters ("One-click ready", "Might be abandoned", ...).
"""

import datetime
import math
import time

from . import categorize, db, github

ONE_CLICK_FILES = {
    "dockerfile": 5, "docker-compose.yml": 5, "docker-compose.yaml": 5,
    "compose.yml": 5, "compose.yaml": 5,
    "package.json": 3, "pyproject.toml": 3, "setup.py": 2, "requirements.txt": 2,
    "cargo.toml": 3, "go.mod": 3, "makefile": 2, "justfile": 2,
    "install.sh": 3, "setup.sh": 2, "flake.nix": 2, "devcontainer.json": 2,
    ".devcontainer": 2, "vercel.json": 2, "netlify.toml": 2, "render.yaml": 2,
    "app.json": 2, "railway.json": 2,
}


def _days_since(iso):
    if not iso:
        return None
    try:
        dt = datetime.datetime.strptime(iso[:19], "%Y-%m-%dT%H:%M:%S")
        return max(0.0, (datetime.datetime.utcnow() - dt).total_seconds() / 86400.0)
    except ValueError:
        return None


def score_repo(meta, root_files=None):
    """Return (score, breakdown, verdict, flags)."""
    b = {}
    flags = []

    stars = meta.get("stars") or 0
    b["popularity"] = round(min(25.0, 25.0 * math.log10(stars + 1) / 5.0), 1)  # 100k stars = max

    days = _days_since(meta.get("pushed_at"))
    if days is None:
        b["freshness"] = 5.0
    elif days <= 7:
        b["freshness"] = 20.0
    elif days <= 30:
        b["freshness"] = 17.0
    elif days <= 90:
        b["freshness"] = 13.0
    elif days <= 365:
        b["freshness"] = 8.0
    else:
        b["freshness"] = 2.0

    maint = 15.0
    if meta.get("archived"):
        maint = 0.0
        flags.append("🪦 Archived — read only")
    else:
        issues, s = meta.get("open_issues") or 0, max(stars, 1)
        if issues > 0 and issues / s > 0.15 and issues > 100:
            maint -= 5.0
        if days is not None and days > 365:
            maint -= 7.0
    b["maintenance"] = round(max(0.0, maint), 1)

    forks = meta.get("forks") or 0
    b["community"] = round(min(10.0, 10.0 * math.log10(forks + 1) / 4.0), 1)  # 10k forks = max

    docs = 0.0
    if meta.get("description"):
        docs += 5.0
    if meta.get("license"):
        docs += 4.0
    if meta.get("topics"):
        docs += min(3.0, len(meta["topics"]))
    if meta.get("homepage"):
        docs += 3.0
    b["docs"] = round(min(15.0, docs), 1)

    oneclick = 0.0
    if root_files:
        lower = {f.lower() for f in root_files}
        for f, pts in ONE_CLICK_FILES.items():
            if f in lower:
                oneclick += pts
    b["one_click"] = round(min(15.0, oneclick), 1)

    score = round(sum(b.values()), 1)

    if b["one_click"] >= 8:
        flags.append("🚀 One-click ready")
    if days is not None and days <= 14 and not meta.get("archived"):
        flags.append("✅ Actively maintained")
    if days is not None and days > 365 and not meta.get("archived"):
        flags.append("⚠️ Might be abandoned")
    if meta.get("license"):
        flags.append("📜 %s licensed" % meta["license"])
    else:
        flags.append("🚫 No license — careful using this commercially")
    if b["docs"] >= 12 and b["one_click"] >= 6:
        flags.append("🌱 Beginner friendly")

    if score >= 85:
        verdict = "👑 Legendary"
    elif score >= 70:
        verdict = "🥇 Excellent"
    elif score >= 55:
        verdict = "🥈 Solid"
    elif score >= 40:
        verdict = "🥉 Decent"
    else:
        verdict = "🧪 Experimental"

    return score, b, verdict, flags


def run(con=None, deep=True, only_pending=False, progress=None):
    """Enrich + score every repo, then crown champions.

    Returns dict with counts and any champion changes.
    """
    con = con or db.connect()
    status = "pending" if only_pending else None
    repos = db.all_repos(con, status=status)
    scored = errors = 0

    for r in repos:
        name = r["full_name"]
        meta, err = github.fetch_repo(name)
        if err == "gone":
            db.upsert_metadata(con, name, {"status": "gone", "error": "repo not found"})
            errors += 1
            continue
        if err:
            db.upsert_metadata(con, name, {"status": r["status"], "error": err})
            errors += 1
            if progress:
                progress("  ! %s: %s" % (name, err))
            if "rate-limited" in err:
                break  # no point hammering
            continue

        root_files = github.fetch_root_files(name) if deep else []
        meta["category"] = categorize.categorise(dict(meta, full_name=name))
        score, breakdown, verdict, flags = score_repo(meta, root_files)
        meta.update({
            "score": score, "breakdown": breakdown, "verdict": verdict,
            "flags": flags, "status": "scored", "error": None,
            "enriched_at": time.time(),
        })
        db.upsert_metadata(con, name, meta)
        scored += 1
        if progress:
            progress("  ✓ %-45s %5.1f  %s" % (name, score, verdict))

    champs = db.champions(con)
    changed = db.record_crowns(con, champs)
    return {
        "scored": scored, "errors": errors, "total": len(repos),
        "champions": champs, "new_crowns": changed,
    }
