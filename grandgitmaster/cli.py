"""GrandGitMaster CLI — everything one command away.

  ggm add <repo|url>...        add repos to the catalogue
  ggm ingest <file|->          extract repos from any text (bookmarks, notes)
  ggm x pull [links|file]      resolve X links -> repos (no API key needed)
  ggm x watch [--query Q]      poll X search for new repos (X_BEARER_TOKEN)
  ggm ringer [--pending]       enrich + score + crown (the Ringer)
  ggm top [category]           champions / category leaderboard
  ggm best <query>             THE repo for a need
  ggm search <query>           search the catalogue
  ggm serve [--port N]         mobile PWA + JSON API
  ggm mcp                      MCP stdio server for agents
  ggm export                   write data/champions.json + LEADERBOARD.md
  ggm star                     GitHub-star all current champions (GITHUB_TOKEN)
  ggm stats                    quick numbers
"""

import argparse
import os
import sys

from . import __version__, db, export, github, ringer, xwatcher


def _p(msg=""):
    print(msg)


def _print_repo(r, rank=None, crowned=False):
    head = ("%2d. " % rank) if rank else ""
    crown = "👑 " if crowned else ""
    score = "%.1f" % r["score"] if r["status"] == "scored" else "  ⏳"
    print("%s%s%s  [%s]  %s" % (head, crown, r["full_name"], score, r.get("verdict") or "pending"))
    if r.get("description"):
        print("     %s" % r["description"][:110])
    extras = []
    if r.get("stars"):
        extras.append("⭐ %s" % format(r["stars"], ","))
    if r.get("language"):
        extras.append(r["language"])
    extras.append("📂 " + (r.get("category") or "?"))
    print("     %s" % "  ·  ".join(extras))
    if r.get("flags"):
        print("     %s" % "  ".join(r["flags"]))


def cmd_add(args):
    con = db.connect()
    added = 0
    for item in args.repos:
        slugs = github.extract_repos(item) or ([item.lower()] if "/" in item else [])
        if not slugs:
            _p("  ? not a repo: %s" % item)
            continue
        for s in slugs:
            if db.add_repo(con, s, source="manual"):
                _p("  + %s" % s)
                added += 1
            else:
                _p("  = %s (already known)" % s)
    _p("%d new repo(s). Run `ggm ringer` to rank them." % added)


def cmd_ingest(args):
    text = sys.stdin.read() if args.source == "-" else open(args.source).read()
    con = db.connect()
    slugs = github.extract_repos(text)
    added = [s for s in slugs if db.add_repo(con, s, source="ingest", source_ref=args.source)]
    _p("Found %d repo(s), %d new. Run `ggm ringer` to rank them." % (len(slugs), len(added)))
    for s in added:
        _p("  + %s" % s)


def _watchlist_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "seeds", "x_watchlist.txt")


def cmd_x(args):
    con = db.connect()
    if args.xcmd == "pull":
        refs = list(args.links)
        src = args.file or (None if refs else _watchlist_path())
        if src and os.path.exists(src):
            refs += [l.strip() for l in open(src) if l.strip() and not l.startswith("#")]
        if not refs:
            _p("Nothing to pull. Pass tweet links, or add them to seeds/x_watchlist.txt")
            return
        _p("Pulling %d tweet link(s) from X…" % len(refs))
        out = xwatcher.process_tweet_refs(refs, con=con, progress=_p)
        _p("Done: %d repo(s) found, %d new, %d tweet(s) already seen, %d failed."
           % (len(out["repos_found"]), len(out["new_repos"]), out["already_seen"],
              len(out["failed"])))
        if out["new_repos"]:
            _p("Run `ggm ringer` to put them through the Ringer.")
    elif args.xcmd == "sleuth":
        _p("🕵️ Sleuthing project names from tweets with no direct repo link…")
        out = xwatcher.sleuth(con=con, progress=_p)
        _p("Checked %d name(s) across %d tweet(s): %d repo(s) hunted down."
           % (out["names_checked"], out["tweets_without_links"], len(out["new_repos"])))
        if out["new_repos"]:
            _p("Run `ggm ringer` to rank them.")
    elif args.xcmd == "watch":
        out = xwatcher.watch_once(query=args.query, con=con, progress=_p)
        _p("Scanned %d tweet(s): %d repo(s) found, %d new."
           % (out["tweets"], len(out["repos_found"]), len(out["new_repos"])))


def cmd_ringer(args):
    con = db.connect()
    _p("🥊 The Ringer is open. Scoring…")
    out = ringer.run(con, deep=not args.fast, only_pending=args.pending, progress=_p)
    _p("")
    _p("Scored %d/%d (%d errors)." % (out["scored"], out["total"], out["errors"]))
    if out["new_crowns"]:
        _p("")
        _p("👑 NEW KINGS CROWNED:")
        for c in out["new_crowns"]:
            _p("   %s → %s (%.1f)" % (c["category"], c["full_name"], c["score"]))
    export.export(con)
    _p("Exported data/champions.json + data/LEADERBOARD.md")


def cmd_top(args):
    con = db.connect()
    if args.category:
        rows = db.all_repos(con, category=args.category)[:args.limit]
        _p("🏆 Top of %s:" % args.category)
        for i, r in enumerate(rows, 1):
            _print_repo(r, rank=i, crowned=(i == 1 and r["status"] == "scored"))
    else:
        _p("👑 CATEGORY KINGS:")
        for r in db.champions(con):
            _print_repo(r, crowned=True)
        if not db.champions(con):
            _p("  (no scored repos yet — `ggm ringer` first)")


def cmd_best(args):
    con = db.connect()
    hits = db.search(con, " ".join(args.query), limit=3)
    if not hits:
        _p("No match. Try `ggm search` with broader words, or `ggm add` a repo.")
        return
    _p("👑 THE repo for '%s':" % " ".join(args.query))
    _print_repo(hits[0], crowned=True)
    if hits[1:]:
        _p("\nAlso strong:")
        for i, r in enumerate(hits[1:], 2):
            _print_repo(r, rank=i)


def cmd_search(args):
    con = db.connect()
    hits = db.search(con, " ".join(args.query), category=args.category, limit=args.limit)
    for i, r in enumerate(hits, 1):
        _print_repo(r, rank=i)
    if not hits:
        _p("No results.")


def cmd_serve(args):
    from . import server
    server.serve(port=args.port)


def cmd_mcp(_args):
    from . import mcp_server
    mcp_server.serve()


def cmd_export(_args):
    paths = export.export()
    _p("Wrote:\n  %s\n  %s" % paths)


def cmd_star(_args):
    con = db.connect()
    champs = db.champions(con)
    if not champs:
        _p("No champions yet — run `ggm ringer` first.")
        return
    for c in champs:
        ok, err = github.star_repo(c["full_name"])
        _p("  %s %s (%s)" % ("⭐" if ok else "✗", c["full_name"], err or "starred"))


def cmd_stats(_args):
    con = db.connect()
    s = db.stats(con)
    _p("📊 %s repos · %s ranked · %s pending · %s caught from X"
       % (s["total"] or 0, s["scored"] or 0, s["pending"] or 0, s["from_x"] or 0))
    for c in db.categories(con):
        _p("   %-16s %3d repos" % (c["category"], c["n"]))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="ggm", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version", version="GrandGitMaster " + __version__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add", help="add repos"); p.add_argument("repos", nargs="+"); p.set_defaults(fn=cmd_add)
    p = sub.add_parser("ingest", help="extract repos from a file or stdin (-)")
    p.add_argument("source"); p.set_defaults(fn=cmd_ingest)

    px = sub.add_parser("x", help="X.com watcher")
    xsub = px.add_subparsers(dest="xcmd", required=True)
    p = xsub.add_parser("pull", help="resolve tweet links → repos (no API key)")
    p.add_argument("links", nargs="*"); p.add_argument("--file"); p.set_defaults(fn=cmd_x)
    p = xsub.add_parser("sleuth", help="hunt down repos merely *named* in tweets")
    p.set_defaults(fn=cmd_x)
    p = xsub.add_parser("watch", help="poll X search (X_BEARER_TOKEN)")
    p.add_argument("--query"); p.set_defaults(fn=cmd_x)

    p = sub.add_parser("ringer", help="enrich + score + crown")
    p.add_argument("--pending", action="store_true", help="only new repos")
    p.add_argument("--fast", action="store_true", help="skip root-file scan")
    p.set_defaults(fn=cmd_ringer)

    p = sub.add_parser("top", help="leaderboard"); p.add_argument("category", nargs="?")
    p.add_argument("--limit", type=int, default=10); p.set_defaults(fn=cmd_top)
    p = sub.add_parser("best", help="THE repo for a need"); p.add_argument("query", nargs="+"); p.set_defaults(fn=cmd_best)
    p = sub.add_parser("search", help="search catalogue"); p.add_argument("query", nargs="+")
    p.add_argument("--category"); p.add_argument("--limit", type=int, default=10); p.set_defaults(fn=cmd_search)

    p = sub.add_parser("serve", help="mobile PWA + API")
    p.add_argument("--port", type=int, default=8477); p.set_defaults(fn=cmd_serve)
    p = sub.add_parser("mcp", help="MCP stdio server for agents"); p.set_defaults(fn=cmd_mcp)
    p = sub.add_parser("export", help="write champions.json + LEADERBOARD.md"); p.set_defaults(fn=cmd_export)
    p = sub.add_parser("star", help="GitHub-star all champions"); p.set_defaults(fn=cmd_star)
    p = sub.add_parser("stats", help="quick numbers"); p.set_defaults(fn=cmd_stats)

    args = ap.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
