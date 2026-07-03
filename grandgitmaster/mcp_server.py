"""MCP (Model Context Protocol) server over stdio — plug GrandGitMaster into
Claude Code, Codex, Cursor, or any MCP-capable agent as a second brain.

Zero dependencies: speaks JSON-RPC 2.0 over stdin/stdout directly.

Claude Code:   claude mcp add grandgitmaster -- python -m grandgitmaster mcp
Codex CLI:     [mcp_servers.grandgitmaster]
               command = "python"
               args = ["-m", "grandgitmaster", "mcp"]
"""

import json
import sys

from . import __version__, categorize, db, github, ringer, xwatcher

TOOLS = [
    {
        "name": "best_repo",
        "description": "Find the single best Git repository for a need, e.g. "
                       "'web scraping', 'llm agents', 'free apis'. Returns the top-ranked "
                       "repo with its GrandScore, verdict and plain-language flags.",
        "inputSchema": {"type": "object", "properties": {
            "query": {"type": "string", "description": "what you need a repo for"}},
            "required": ["query"]},
    },
    {
        "name": "search_repos",
        "description": "Search the GrandGitMaster catalogue of ranked repos by keyword, "
                       "optionally within a category. Results are ordered by GrandScore.",
        "inputSchema": {"type": "object", "properties": {
            "query": {"type": "string"},
            "category": {"type": "string", "description": "optional category filter"},
            "limit": {"type": "integer", "default": 10}},
            "required": ["query"]},
    },
    {
        "name": "top_repos",
        "description": "Leaderboard: the champions (best repo per category), or the "
                       "top N repos of one category.",
        "inputSchema": {"type": "object", "properties": {
            "category": {"type": "string"},
            "limit": {"type": "integer", "default": 10}}},
    },
    {
        "name": "add_repo",
        "description": "Add a GitHub repo (owner/name or URL) to the catalogue so it gets "
                       "ranked by the Ringer.",
        "inputSchema": {"type": "object", "properties": {
            "repo": {"type": "string"}}, "required": ["repo"]},
    },
    {
        "name": "ingest_text",
        "description": "Extract every GitHub repo mentioned in a blob of text (tweet, "
                       "newsletter, README, chat log) and queue them all for ranking.",
        "inputSchema": {"type": "object", "properties": {
            "text": {"type": "string"}}, "required": ["text"]},
    },
    {
        "name": "pull_tweets",
        "description": "Given X/Twitter status links or tweet IDs, fetch each tweet, "
                       "extract GitHub repos, and queue them for ranking. No X API key needed.",
        "inputSchema": {"type": "object", "properties": {
            "tweets": {"type": "array", "items": {"type": "string"}}},
            "required": ["tweets"]},
    },
    {
        "name": "run_ringer",
        "description": "Run the Ringer: enrich all catalogued repos from the GitHub API, "
                       "compute GrandScores, and crown category champions. Needs GitHub API "
                       "access (GITHUB_TOKEN recommended).",
        "inputSchema": {"type": "object", "properties": {
            "only_pending": {"type": "boolean", "default": False}}},
    },
    {
        "name": "list_categories",
        "description": "List all categories with repo counts and top scores.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def _repo_brief(r):
    return {k: r.get(k) for k in (
        "full_name", "url", "description", "category", "score", "verdict",
        "flags", "stars", "language", "status")}


def call_tool(name, args):
    con = db.connect()
    if name == "best_repo":
        hits = db.search(con, args["query"], limit=1)
        if not hits:
            return {"result": None, "hint": "nothing matched — try add_repo or a broader query",
                    "categories": [c["category"] for c in db.categories(con)]}
        return {"best": _repo_brief(hits[0]),
                "runners_up": [_repo_brief(r) for r in db.search(con, args["query"], limit=4)[1:]]}
    if name == "search_repos":
        hits = db.search(con, args["query"], category=args.get("category"),
                         limit=args.get("limit", 10))
        return {"count": len(hits), "results": [_repo_brief(r) for r in hits]}
    if name == "top_repos":
        if args.get("category"):
            rows = db.all_repos(con, category=args["category"])[: args.get("limit", 10)]
            return {"category": args["category"], "top": [_repo_brief(r) for r in rows]}
        return {"champions": [_repo_brief(r) for r in db.champions(con)]}
    if name == "add_repo":
        slugs = github.extract_repos(args["repo"]) or (
            [args["repo"].strip().lower()] if "/" in args["repo"] else [])
        added = [s for s in slugs if db.add_repo(con, s, source="agent")]
        return {"added": added, "already_known": [s for s in slugs if s not in added],
                "note": "run_ringer will score them"}
    if name == "ingest_text":
        slugs = github.extract_repos(args["text"])
        added = [s for s in slugs if db.add_repo(con, s, source="agent")]
        return {"found": slugs, "new": added}
    if name == "pull_tweets":
        return xwatcher.process_tweet_refs(args["tweets"], con=con)
    if name == "run_ringer":
        out = ringer.run(con, only_pending=args.get("only_pending", False))
        out["champions"] = [_repo_brief(r) for r in out["champions"]]
        out["new_crowns"] = [_repo_brief(r) for r in out["new_crowns"]]
        return out
    if name == "list_categories":
        return {"categories": db.categories(con), "stats": db.stats(con),
                "known_category_names": categorize.CATEGORY_NAMES}
    raise ValueError("unknown tool: " + name)


def _reply(msg_id, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": msg_id}
    if error is not None:
        msg["error"] = error
    else:
        msg["result"] = result
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def serve():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except ValueError:
            continue
        method, msg_id = req.get("method"), req.get("id")
        try:
            if method == "initialize":
                _reply(msg_id, {
                    "protocolVersion": req.get("params", {}).get("protocolVersion", "2024-11-05"),
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "grandgitmaster", "version": __version__},
                })
            elif method == "notifications/initialized":
                continue
            elif method == "tools/list":
                _reply(msg_id, {"tools": TOOLS})
            elif method == "tools/call":
                params = req.get("params", {})
                out = call_tool(params.get("name"), params.get("arguments") or {})
                _reply(msg_id, {"content": [
                    {"type": "text", "text": json.dumps(out, indent=2, default=str)}]})
            elif method == "ping":
                _reply(msg_id, {})
            elif msg_id is not None:
                _reply(msg_id, error={"code": -32601, "message": "method not found: %s" % method})
        except Exception as e:
            if msg_id is not None:
                _reply(msg_id, error={"code": -32000, "message": str(e)})


if __name__ == "__main__":
    serve()
