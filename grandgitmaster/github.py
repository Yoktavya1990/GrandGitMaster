"""Minimal GitHub API client (standard library only).

Works unauthenticated (60 req/h) or with GITHUB_TOKEN / GH_TOKEN (5000 req/h).
"""

import json
import os
import re
import urllib.error
import urllib.request

API = "https://api.github.com"

GITHUB_URL_RE = re.compile(
    r"(?:https?://)?(?:www\.)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)"
)

# Paths that are not repos: github.com/<reserved>/...
RESERVED_OWNERS = {
    "topics", "search", "features", "trending", "collections", "sponsors",
    "orgs", "settings", "marketplace", "apps", "about", "pricing", "login",
    "signup", "explore", "issues", "pulls", "notifications", "new", "site",
    "contact", "customer-stories", "readme", "team", "enterprise", "events",
}


def _token():
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def _get(url, timeout=20):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "GrandGitMaster/0.1",
    })
    tok = _token()
    if tok:
        req.add_header("Authorization", "Bearer " + tok)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def extract_repos(text):
    """Extract owner/name repo slugs from arbitrary text. Lowercased, deduped."""
    out, seen = [], set()
    for owner, name in GITHUB_URL_RE.findall(text or ""):
        if owner.lower() in RESERVED_OWNERS:
            continue
        name = re.sub(r"\.git$", "", name).rstrip(".")
        if not name:
            continue
        slug = (owner + "/" + name).lower()
        if slug not in seen:
            seen.add(slug)
            out.append(slug)
    return out


def fetch_repo(full_name):
    """Fetch repo metadata. Returns (meta_dict, error_string)."""
    try:
        d = _get("%s/repos/%s" % (API, full_name))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, "gone"
        if e.code in (403, 429):
            return None, "rate-limited (set GITHUB_TOKEN for 5000 req/h)"
        return None, "http %d" % e.code
    except Exception as e:  # network, proxy, timeout
        return None, str(e)

    lic = d.get("license") or {}
    return {
        "display_name": d.get("full_name") or full_name,
        "url": d.get("html_url") or "https://github.com/" + full_name,
        "description": d.get("description"),
        "language": d.get("language"),
        "topics": d.get("topics") or [],
        "stars": d.get("stargazers_count") or 0,
        "forks": d.get("forks_count") or 0,
        "open_issues": d.get("open_issues_count") or 0,
        "license": lic.get("spdx_id") if lic.get("spdx_id") != "NOASSERTION" else lic.get("name"),
        "homepage": d.get("homepage"),
        "archived": 1 if d.get("archived") else 0,
        "created_at": d.get("created_at"),
        "pushed_at": d.get("pushed_at"),
    }, None


def fetch_root_files(full_name):
    """List of filenames at repo root (for one-click-readiness signals).
    Returns [] on any failure — this signal is best-effort."""
    try:
        items = _get("%s/repos/%s/contents/" % (API, full_name))
        return [i.get("name", "") for i in items if isinstance(i, dict)]
    except Exception:
        return []


def search_repo_by_name(name):
    """Find the GitHub repo for a project *name* dropped in a tweet
    ('Alibaba open-sourced PageAgent' → alibaba/pageagent). Only returns a hit
    whose repo name matches exactly (case-insensitive), so precision stays high."""
    import urllib.parse
    try:
        d = _get("%s/search/repositories?q=%s+in:name&sort=stars&order=desc&per_page=5"
                 % (API, urllib.parse.quote(name)))
    except Exception:
        return None
    for item in d.get("items") or []:
        if item.get("name", "").lower() == name.lower():
            return item["full_name"].lower()
    return None


def star_repo(full_name):
    """Star a repo as the authenticated user. Requires GITHUB_TOKEN."""
    tok = _token()
    if not tok:
        return False, "GITHUB_TOKEN not set"
    req = urllib.request.Request(
        "%s/user/starred/%s" % (API, full_name), method="PUT",
        headers={"Authorization": "Bearer " + tok,
                 "User-Agent": "GrandGitMaster/0.1",
                 "Content-Length": "0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status in (204, 304), None
    except Exception as e:
        return False, str(e)
