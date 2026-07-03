"""HTTP server: JSON API + the mobile PWA. Standard library only.

    ggm serve            # http://localhost:8477
    ggm serve --port 80  # anywhere Python runs: laptop, VPS, Raspberry Pi
"""

import json
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import db, github, webapp, xwatcher

DEFAULT_PORT = 8477  # GGM on a phone keypad-ish


class Handler(BaseHTTPRequestHandler):
    def _send(self, body, ctype="application/json", code=200):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def _json(self, obj, code=200):
        self._send(json.dumps(obj, default=str), code=code)

    def log_message(self, fmt, *args):  # quiet
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path, qs = parsed.path, urllib.parse.parse_qs(parsed.query)
        q = lambda k, d=None: (qs.get(k) or [d])[0]
        con = db.connect()
        try:
            if path == "/":
                return self._send(webapp.HTML, "text/html")
            if path == "/manifest.json":
                return self._json(webapp.MANIFEST)
            if path == "/sw.js":
                return self._send(webapp.SERVICE_WORKER, "text/javascript")
            if path == "/api/stats":
                return self._json(db.stats(con))
            if path == "/api/categories":
                return self._json({"categories": db.categories(con)})
            if path == "/api/search":
                return self._json({"results": db.search(
                    con, q("q", ""), category=q("category"), limit=int(q("limit", "25")))})
            if path == "/api/top":
                if q("category"):
                    return self._json({"top": db.all_repos(con, category=q("category"))[:25]})
                return self._json({"champions": db.champions(con)})
            if path == "/api/repos":
                return self._json({"repos": db.all_repos(con)})
            return self._json({"error": "not found"}, 404)
        finally:
            con.close()

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except ValueError:
            return self._json({"error": "bad json"}, 400)
        con = db.connect()
        try:
            if self.path == "/api/ingest":
                text = body.get("text", "")
                tweet_refs = [w for w in text.split()
                              if xwatcher.parse_tweet_ref(w) and "github.com" not in w]
                slugs = github.extract_repos(text)
                added = [s for s in slugs if db.add_repo(con, s, source="ingest")]
                msg_bits = []
                if tweet_refs:
                    tw = xwatcher.process_tweet_refs(tweet_refs, con=con)
                    added += tw["new_repos"]
                    msg_bits.append("%d tweet(s) processed" % tw["tweets"])
                msg_bits.append("%d new repo(s) queued" % len(added))
                return self._json({"added": added,
                                   "message": ", ".join(msg_bits) +
                                   ". Run `ggm ringer` to rank them."})
            if self.path == "/api/add":
                slug = (body.get("repo") or "").strip()
                new = db.add_repo(con, slug, source="agent") if "/" in slug else False
                return self._json({"added": new})
            return self._json({"error": "not found"}, 404)
        finally:
            con.close()


def serve(port=DEFAULT_PORT, host="0.0.0.0"):
    httpd = ThreadingHTTPServer((host, port), Handler)
    print("👑 GrandGitMaster serving on http://localhost:%d  (Ctrl+C to stop)" % port)
    print("   On your phone: open http://<this-machine's-ip>:%d and 'Add to Home Screen'" % port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
