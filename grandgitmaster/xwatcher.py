"""X.com watcher — never trawl X for repos by hand again.

Three modes, best-available wins:

1. Tweet resolver (NO API key needed): given tweet URLs/IDs (your bookmarks,
   a watchlist file, links you paste to an agent), fetches each tweet via
   X's public syndication endpoint, pulls out every github.com link
   (following t.co redirects), and queues the repos for the Ringer.

2. Search watcher (needs X_BEARER_TOKEN): polls the X API v2 recent-search
   endpoint for tweets matching a query (default: viral tweets linking to
   github.com) and feeds every new repo through the same pipeline.

3. Text ingest: extract repos from ANY text — an exported bookmarks file,
   a newsletter, clipboard soup. `ggm ingest <file>` / stdin.
"""

import json
import math
import os
import re
import urllib.error
import urllib.parse
import urllib.request

from . import db, github

SYNDICATION = "https://cdn.syndication.twimg.com/tweet-result?id={id}&token={token}"
TWEET_ID_RE = re.compile(r"(?:twitter\.com|x\.com)/[^/\s]+/status/(\d+)|^(\d{8,25})$")
TCO_RE = re.compile(r"https://t\.co/[A-Za-z0-9]+")


def _syndication_token(tweet_id):
    """Reimplementation of X's client-side token: (id/1e15*PI) in base36,
    zeros and dots stripped."""
    n = (int(tweet_id) / 1e15) * math.pi
    ip = int(n)
    digits = ""
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    x = ip
    while x:
        digits = alphabet[x % 36] + digits
        x //= 36
    digits = digits or "0"
    frac = n - ip
    fdigits = ""
    for _ in range(11):
        frac *= 36
        d = int(frac)
        fdigits += alphabet[d]
        frac -= d
    token = (digits + "." + fdigits).replace(".", "")
    return re.sub(r"0+", "", token) or "a"


def _http_json(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers=dict(
        {"User-Agent": "Mozilla/5.0 (GrandGitMaster)"}, **(headers or {})))
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def parse_tweet_ref(ref):
    """Accepts a tweet URL or bare ID, returns the ID or None."""
    m = TWEET_ID_RE.search(ref.strip())
    if m:
        return m.group(1) or m.group(2)
    return None


def fetch_tweet(tweet_id):
    """Fetch tweet JSON via the public syndication endpoint. None if gone."""
    for token in (_syndication_token(tweet_id), "a"):
        try:
            d = _http_json(SYNDICATION.format(id=tweet_id, token=token))
            if d:
                return d
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError):
            continue
    return None


def resolve_tco(url, timeout=15):
    """Follow a t.co redirect to its destination without downloading bodies."""
    req = urllib.request.Request(url, method="HEAD",
                                 headers={"User-Agent": "Mozilla/5.0 (GrandGitMaster)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.geturl()
    except urllib.error.HTTPError as e:
        return e.geturl() or url
    except Exception:
        return url


def repos_from_tweet(tweet):
    """Extract github repo slugs from tweet text + expanded/t.co urls."""
    chunks = [tweet.get("text") or ""]
    entities = tweet.get("entities") or {}
    tco_links = []
    for u in entities.get("urls") or []:
        expanded = u.get("expanded_url") or ""
        chunks.append(expanded)
        if not expanded and u.get("url"):
            tco_links.append(u["url"])
    # quoted / self-thread tweets carry links too
    if tweet.get("quoted_tweet"):
        chunks.append((tweet["quoted_tweet"].get("text")) or "")
        for u in (tweet["quoted_tweet"].get("entities") or {}).get("urls") or []:
            chunks.append(u.get("expanded_url") or "")
    text = " ".join(chunks)
    tco_links += [l for l in TCO_RE.findall(text)]
    for link in dict.fromkeys(tco_links):
        final = resolve_tco(link)
        if "github.com" in final:
            text += " " + final
    return github.extract_repos(text)


def process_tweet_refs(refs, con=None, progress=None):
    """Resolve tweet refs → repos → DB. Returns summary dict."""
    con = con or db.connect()
    added, found, skipped, failed = [], [], 0, []
    for ref in refs:
        tid = parse_tweet_ref(ref)
        if not tid:
            continue
        if con.execute("SELECT 1 FROM seen_tweets WHERE tweet_id = ?", (tid,)).fetchone():
            skipped += 1
            continue
        tweet = fetch_tweet(tid)
        if not tweet:
            failed.append(tid)
            if progress:
                progress("  ! tweet %s: could not fetch" % tid)
            continue
        slugs = repos_from_tweet(tweet)
        author = ((tweet.get("user") or {}).get("screen_name")) or "?"
        for slug in slugs:
            found.append(slug)
            if db.add_repo(con, slug, source="x", source_ref=tid):
                added.append(slug)
        con.execute(
            "INSERT OR REPLACE INTO seen_tweets (tweet_id, author, text, repos_found, processed_at) "
            "VALUES (?,?,?,?, strftime('%s','now'))",
            (tid, author, (tweet.get("text") or "")[:2000], json.dumps(slugs)))
        con.commit()
        if progress:
            progress("  ✓ @%-18s → %s" % (author, ", ".join(slugs) or "no repos in tweet"))
    return {"tweets": len(refs), "repos_found": found, "new_repos": added,
            "already_seen": skipped, "failed": failed}


# "Alibaba open-sourced PageAgent" — announcement verbs followed by a name,
# plus bare CamelCase tokens, are candidate project names for sleuth mode.
NAME_HINT_RE = re.compile(
    r"(?:open[- ]?sourced?|released?|launche[sd]|introducing|announcing|meet|"
    r"drops?|built|created|check out)\s+([A-Za-z][A-Za-z0-9._-]{2,30})", re.I)
CAMEL_RE = re.compile(r"\b([A-Z][a-z0-9]+(?:[A-Z][A-Za-z0-9]+)+)\b")
SLEUTH_STOPWORDS = {
    "github", "twitter", "the", "this", "their", "his", "her", "its", "a", "an",
    "javascript", "typescript", "python", "chatgpt", "openai", "chinese", "china",
}


def name_candidates(text):
    """Likely project names mentioned (but not linked) in tweet text."""
    cands = []
    for m in NAME_HINT_RE.findall(text or ""):
        cands.append(m.strip(".,:;!?"))
    cands += CAMEL_RE.findall(text or "")
    out, seen = [], set()
    for c in cands:
        k = c.lower()
        if k in SLEUTH_STOPWORDS or k in seen or len(k) < 4:
            continue
        seen.add(k)
        out.append(c)
    return out[:3]


def sleuth(con=None, progress=None):
    """Second pass over stored tweets that yielded no repo link: extract
    candidate project names and hunt them down via GitHub search.
    Needs GitHub API access; a GITHUB_TOKEN raises the search rate limit."""
    con = con or db.connect()
    rows = con.execute(
        "SELECT tweet_id, text FROM seen_tweets WHERE repos_found = '[]'").fetchall()
    added, checked = [], 0
    for row in rows:
        for cand in name_candidates(row["text"]):
            checked += 1
            slug = github.search_repo_by_name(cand)
            if slug and db.add_repo(con, slug, source="x-sleuth", source_ref=row["tweet_id"]):
                added.append(slug)
                con.execute("UPDATE seen_tweets SET repos_found = ? WHERE tweet_id = ?",
                            (json.dumps([slug]), row["tweet_id"]))
                con.commit()
                if progress:
                    progress("  🕵️ '%s' → %s" % (cand, slug))
                break
    return {"tweets_without_links": len(rows), "names_checked": checked, "new_repos": added}


def search_x(query=None, max_results=50):
    """X API v2 recent search (requires X_BEARER_TOKEN). Returns tweet dicts
    shaped like the syndication payload (text + entities.urls.expanded_url)."""
    bearer = os.environ.get("X_BEARER_TOKEN")
    if not bearer:
        raise RuntimeError("X_BEARER_TOKEN not set — search mode needs an X API v2 bearer token. "
                           "Tweet-link mode (`ggm x pull <links>`) works without one.")
    query = query or '"github.com" (min_faves:100 OR min_retweets:50) -is:retweet lang:en'
    params = urllib.parse.urlencode({
        "query": query, "max_results": min(max_results, 100),
        "tweet.fields": "entities,author_id,public_metrics",
    })
    d = _http_json("https://api.twitter.com/2/tweets/search/recent?" + params,
                   headers={"Authorization": "Bearer " + bearer})
    out = []
    for t in d.get("data") or []:
        out.append({"id_str": t["id"], "text": t.get("text", ""),
                    "entities": t.get("entities") or {}, "user": {"screen_name": "?"}})
    return out


def watch_once(query=None, con=None, progress=None):
    """One polling pass of search mode: search → extract → queue."""
    con = con or db.connect()
    tweets = search_x(query)
    added, found = [], []
    for t in tweets:
        tid = t["id_str"]
        if con.execute("SELECT 1 FROM seen_tweets WHERE tweet_id = ?", (tid,)).fetchone():
            continue
        slugs = repos_from_tweet(t)
        for slug in slugs:
            found.append(slug)
            if db.add_repo(con, slug, source="x", source_ref=tid):
                added.append(slug)
        con.execute(
            "INSERT OR REPLACE INTO seen_tweets (tweet_id, author, text, repos_found, processed_at) "
            "VALUES (?,?,?,?, strftime('%s','now'))",
            (tid, "?", t.get("text", "")[:2000], json.dumps(slugs)))
        con.commit()
        if progress and slugs:
            progress("  ✓ tweet %s → %s" % (tid, ", ".join(slugs)))
    return {"tweets": len(tweets), "repos_found": found, "new_repos": added}
