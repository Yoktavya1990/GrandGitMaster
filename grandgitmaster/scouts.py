"""The Grandmaster's scouts — they roam the internet so you don't have to.

Every scout is free and needs NO account or API key:

  trending   GitHub's own Trending pages (daily + weekly): what the whole
             world is starring right now.
  hackernews Hacker News front-page stories that link to GitHub: where the
             sharpest tool-finders on the internet post their discoveries.

`ggm scout` runs them all and queues every new repo for the Ringer.
The cloud runs this automatically before every ranking pass, so new
worthwhile repos walk into the Ring on their own.
"""

import json
import re
import time
import urllib.parse
import urllib.request

from . import db, github

TRENDING_PAGES = [
    "https://github.com/trending?since=daily",
    "https://github.com/trending?since=weekly",
]
# first repo link inside each trending list entry: <h2 ...><a href="/owner/repo"
TRENDING_RE = re.compile(r'<h2[^>]*>\s*<a[^>]*href="/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)"', re.S)

HN_API = "https://hn.algolia.com/api/v1/"
HN_MIN_POINTS_FRESH = 10    # newest stories: small but real traction
HN_MIN_POINTS_TOP = 50      # relevance results: only clear hits
HN_MAX_AGE_DAYS = 14


def _fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (GrandGitMaster scout)",
        "Accept-Language": "en",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "replace")


def parse_trending(html):
    """Repo slugs from a GitHub Trending page, in page order."""
    text = " ".join("github.com/" + m for m in TRENDING_RE.findall(html or ""))
    return github.extract_repos(text)


def scout_trending(progress=None):
    slugs = []
    for url in TRENDING_PAGES:
        try:
            found = parse_trending(_fetch(url))
            slugs += found
            if progress:
                progress("  🔭 trending (%s): %d repos" % (url.split("=")[-1], len(found)))
        except Exception as e:
            if progress:
                progress("  ! trending scout: %s" % e)
    return list(dict.fromkeys(slugs))


def parse_hn(payload, min_points, max_age_days=HN_MAX_AGE_DAYS, now=None):
    """Repo slugs from an Algolia HN response, filtered by points + age."""
    now = now or time.time()
    chunks = []
    for hit in (payload.get("hits") or []):
        if (hit.get("points") or 0) < min_points:
            continue
        if now - (hit.get("created_at_i") or 0) > max_age_days * 86400:
            continue
        chunks.append(hit.get("url") or "")
        chunks.append(hit.get("title") or "")
        chunks.append(hit.get("story_text") or "")
    return github.extract_repos(" ".join(chunks))


def scout_hackernews(progress=None):
    queries = [
        ("search_by_date?query=github.com&tags=story&hitsPerPage=100", HN_MIN_POINTS_FRESH),
        ("search_by_date?query=%s&tags=story&hitsPerPage=100"
         % urllib.parse.quote("Show HN github"), HN_MIN_POINTS_FRESH),
        ("search?query=github.com&tags=story&hitsPerPage=100", HN_MIN_POINTS_TOP),
    ]
    slugs = []
    for path, min_points in queries:
        try:
            payload = json.loads(_fetch(HN_API + path))
            found = parse_hn(payload, min_points)
            slugs += found
            if progress:
                progress("  🗞️ hackernews (%s…): %d repos" % (path[:24], len(found)))
        except Exception as e:
            if progress:
                progress("  ! hackernews scout: %s" % e)
    return list(dict.fromkeys(slugs))


SCOUTS = [
    ("trending", scout_trending),
    ("hackernews", scout_hackernews),
]


def run(con=None, progress=None):
    """Run every scout, queue new repos. Returns summary dict."""
    con = con or db.connect()
    found, added = [], []
    for name, fn in SCOUTS:
        for slug in fn(progress=progress):
            found.append(slug)
            if db.add_repo(con, slug, source="scout", source_ref=name):
                added.append(slug)
    if progress:
        progress("Scouts report: %d sightings, %d new recruits for the Ring."
                 % (len(found), len(added)))
    return {"found": found, "new_repos": added}
