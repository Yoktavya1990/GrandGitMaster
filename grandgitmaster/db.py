"""SQLite storage for GrandGitMaster. Local-first, single file, zero deps."""

import json
import os
import sqlite3
import time

DEFAULT_DB = os.environ.get(
    "GGM_DB", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ggm.db")
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS repos (
    full_name     TEXT PRIMARY KEY,           -- owner/name (lowercase)
    display_name  TEXT,                        -- owner/name as GitHub shows it
    url           TEXT,
    description   TEXT,
    language      TEXT,
    topics        TEXT DEFAULT '[]',           -- JSON list
    stars         INTEGER DEFAULT 0,
    forks         INTEGER DEFAULT 0,
    open_issues   INTEGER DEFAULT 0,
    license       TEXT,
    homepage      TEXT,
    archived      INTEGER DEFAULT 0,
    created_at    TEXT,
    pushed_at     TEXT,
    category      TEXT DEFAULT 'uncategorised',
    score         REAL DEFAULT 0,
    breakdown     TEXT DEFAULT '{}',           -- JSON dict of score components
    verdict       TEXT DEFAULT '',             -- plain-language tier
    flags         TEXT DEFAULT '[]',           -- JSON list of plain-language flags
    status        TEXT DEFAULT 'pending',      -- pending | scored | error | gone
    source        TEXT DEFAULT 'manual',       -- manual | x | seed | agent | ingest
    source_ref    TEXT,                        -- e.g. tweet id / file
    first_seen    REAL,
    enriched_at   REAL,
    error         TEXT
);
CREATE TABLE IF NOT EXISTS seen_tweets (
    tweet_id     TEXT PRIMARY KEY,
    author       TEXT,
    text         TEXT,
    repos_found  TEXT DEFAULT '[]',
    processed_at REAL
);
CREATE TABLE IF NOT EXISTS crown_history (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    category   TEXT,
    full_name  TEXT,
    score      REAL,
    crowned_at REAL
);
CREATE INDEX IF NOT EXISTS idx_repos_category ON repos(category);
CREATE INDEX IF NOT EXISTS idx_repos_score ON repos(score DESC);
"""


def connect(path=None):
    path = path or DEFAULT_DB
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con


def add_repo(con, full_name, source="manual", source_ref=None):
    """Register a repo (idempotent). Returns True if it was new."""
    full_name = full_name.strip().strip("/").lower()
    cur = con.execute(
        """INSERT INTO repos (full_name, display_name, url, source, source_ref, first_seen)
           VALUES (?, ?, ?, ?, ?, ?)
           ON CONFLICT(full_name) DO NOTHING""",
        (full_name, full_name, "https://github.com/" + full_name, source, source_ref, time.time()),
    )
    con.commit()
    return cur.rowcount > 0


def upsert_metadata(con, full_name, meta):
    """Store enrichment metadata (dict of column -> value)."""
    cols, vals = [], []
    for k, v in meta.items():
        if isinstance(v, (list, dict)):
            v = json.dumps(v)
        cols.append("%s = ?" % k)
        vals.append(v)
    vals.append(full_name.lower())
    con.execute("UPDATE repos SET %s WHERE full_name = ?" % ", ".join(cols), vals)
    con.commit()


def row_to_dict(row):
    d = dict(row)
    for k in ("topics", "flags"):
        if isinstance(d.get(k), str):
            try:
                d[k] = json.loads(d[k])
            except ValueError:
                pass
    if isinstance(d.get("breakdown"), str):
        try:
            d["breakdown"] = json.loads(d["breakdown"])
        except ValueError:
            pass
    return d


def all_repos(con, category=None, status=None):
    q, args = "SELECT * FROM repos", []
    where = []
    if category:
        where.append("category = ?")
        args.append(category)
    if status:
        where.append("status = ?")
        args.append(status)
    if where:
        q += " WHERE " + " AND ".join(where)
    q += " ORDER BY score DESC, stars DESC"
    return [row_to_dict(r) for r in con.execute(q, args)]


def search(con, query, category=None, limit=20):
    like = "%" + query.lower() + "%"
    q = """SELECT * FROM repos
           WHERE (full_name LIKE ? OR lower(coalesce(description,'')) LIKE ?
                  OR lower(coalesce(topics,'')) LIKE ? OR lower(coalesce(language,'')) LIKE ?)"""
    args = [like, like, like, like]
    if category:
        q += " AND category = ?"
        args.append(category)
    q += " ORDER BY score DESC, stars DESC LIMIT ?"
    args.append(limit)
    return [row_to_dict(r) for r in con.execute(q, args)]


def champions(con):
    """Best (crowned) repo per category."""
    q = """SELECT r.* FROM repos r
           JOIN (SELECT category, MAX(score) AS s FROM repos
                 WHERE status = 'scored' GROUP BY category) m
             ON r.category = m.category AND r.score = m.s
           WHERE r.status = 'scored'
           GROUP BY r.category ORDER BY r.score DESC"""
    return [row_to_dict(r) for r in con.execute(q)]


def record_crowns(con, champs):
    """Append to crown history only when the champion of a category changed."""
    changed = []
    for c in champs:
        last = con.execute(
            "SELECT full_name FROM crown_history WHERE category = ? ORDER BY crowned_at DESC LIMIT 1",
            (c["category"],),
        ).fetchone()
        if not last or last["full_name"] != c["full_name"]:
            con.execute(
                "INSERT INTO crown_history (category, full_name, score, crowned_at) VALUES (?,?,?,?)",
                (c["category"], c["full_name"], c["score"], time.time()),
            )
            changed.append(c)
    con.commit()
    return changed


def categories(con):
    rows = con.execute(
        """SELECT category, COUNT(*) AS n, MAX(score) AS top_score
           FROM repos GROUP BY category ORDER BY n DESC"""
    )
    return [dict(r) for r in rows]


def stats(con):
    r = con.execute(
        """SELECT COUNT(*) AS total,
                  SUM(status = 'scored') AS scored,
                  SUM(status = 'pending') AS pending,
                  SUM(source = 'x') AS from_x
           FROM repos"""
    ).fetchone()
    return dict(r)
