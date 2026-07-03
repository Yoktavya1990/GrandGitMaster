"""GrandGitMaster test suite — stdlib unittest, no network needed.

    python3 -m unittest discover tests -v
"""

import json
import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grandgitmaster import categorize, db, export, github, ringer, scouts, xwatcher  # noqa: E402


def fresh_con():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    return db.connect(path), path


class TestExtract(unittest.TestCase):
    def test_extract_repos(self):
        text = """Check https://github.com/public-apis/public-apis and
        github.com/Ollama/ollama.git, but not github.com/topics/ai or
        https://github.com/features/copilot. Also https://github.com/a/b#readme"""
        self.assertEqual(
            github.extract_repos(text),
            ["public-apis/public-apis", "ollama/ollama", "a/b"])

    def test_tweet_ref_parsing(self):
        self.assertEqual(xwatcher.parse_tweet_ref(
            "https://x.com/i/status/2072606006971081213"), "2072606006971081213")
        self.assertEqual(xwatcher.parse_tweet_ref(
            "https://twitter.com/user/status/123456789?s=20"), "123456789")
        self.assertEqual(xwatcher.parse_tweet_ref("2072606006971081213"),
                         "2072606006971081213")
        self.assertIsNone(xwatcher.parse_tweet_ref("https://example.com"))

    def test_name_candidates(self):
        cands = xwatcher.name_candidates(
            "Alibaba open-sourced PageAgent. Meet LangChain, forget ChatGPT.")
        self.assertIn("PageAgent", cands)
        self.assertNotIn("ChatGPT", cands)  # stopword


class TestCategorise(unittest.TestCase):
    def test_categories(self):
        self.assertEqual(categorize.categorise({
            "full_name": "x/crawler", "topics": ["scraper", "crawler"],
            "description": "web scraping framework"}), "scraping-data")
        self.assertEqual(categorize.categorise({
            "full_name": "public-apis/public-apis", "topics": ["api", "apis"],
            "description": "A collective list of free APIs"}), "apis")
        self.assertEqual(categorize.categorise({
            "full_name": "a/b", "topics": [], "description": "quantum stuff"}), "other")


class TestRinger(unittest.TestCase):
    GOOD = {
        "stars": 120000, "forks": 20000, "open_issues": 200, "archived": 0,
        "description": "Great tool", "license": "MIT", "homepage": "https://x.dev",
        "topics": ["cli", "productivity"], "pushed_at": "2099-01-01T00:00:00Z",
    }

    def test_score_good_repo(self):
        score, b, verdict, flags = ringer.score_repo(
            self.GOOD, root_files=["Dockerfile", "docker-compose.yml", "Makefile"])
        self.assertGreaterEqual(score, 85)
        self.assertEqual(verdict, "👑 Legendary")
        self.assertIn("🚀 One-click ready", flags)
        self.assertEqual(b["popularity"], 25.0)

    def test_score_abandoned_repo(self):
        meta = dict(self.GOOD, stars=50, forks=2, pushed_at="2019-01-01T00:00:00Z",
                    license=None, homepage=None, topics=[], description=None)
        score, b, verdict, flags = ringer.score_repo(meta)
        self.assertLess(score, 40)
        self.assertIn("⚠️ Might be abandoned", flags)
        self.assertIn("🚫 No license — careful using this commercially", flags)

    def test_archived_zero_maintenance(self):
        _, b, _, flags = ringer.score_repo(dict(self.GOOD, archived=1))
        self.assertEqual(b["maintenance"], 0.0)
        self.assertIn("🪦 Archived — read only", flags)


class TestPipeline(unittest.TestCase):
    """End-to-end with a mocked GitHub API: add → ringer → crown → export."""

    def test_full_run(self):
        con, path = fresh_con()
        db.add_repo(con, "scrapy/scrapy", source="x", source_ref="111")
        db.add_repo(con, "tiny/scraper", source="manual")
        db.add_repo(con, "public-apis/public-apis", source="seed")

        metas = {
            "scrapy/scrapy": {"display_name": "scrapy/scrapy",
                              "url": "https://github.com/scrapy/scrapy",
                              "description": "web scraping framework", "language": "Python",
                              "topics": ["scraping", "crawler"], "stars": 52000,
                              "forks": 10000, "open_issues": 400, "license": "BSD-3-Clause",
                              "homepage": "https://scrapy.org", "archived": 0,
                              "created_at": "2010-01-01T00:00:00Z",
                              "pushed_at": "2099-01-01T00:00:00Z"},
            "tiny/scraper": {"display_name": "tiny/scraper", "url": "u",
                             "description": "toy scraper", "language": "Python",
                             "topics": ["scraping"], "stars": 3, "forks": 0,
                             "open_issues": 1, "license": None, "homepage": None,
                             "archived": 0, "created_at": "2024-01-01T00:00:00Z",
                             "pushed_at": "2024-02-01T00:00:00Z"},
            "public-apis/public-apis": {"display_name": "public-apis/public-apis", "url": "u",
                                        "description": "A collective list of free APIs",
                                        "language": "Python", "topics": ["api", "apis"],
                                        "stars": 300000, "forks": 30000, "open_issues": 10,
                                        "license": "MIT", "homepage": None, "archived": 0,
                                        "created_at": "2016-01-01T00:00:00Z",
                                        "pushed_at": "2099-01-01T00:00:00Z"},
        }
        with mock.patch.object(github, "fetch_repo", lambda n: (metas[n], None)), \
             mock.patch.object(github, "fetch_root_files",
                               lambda n: ["Dockerfile", "setup.py"]):
            out = ringer.run(con)

        self.assertEqual(out["scored"], 3)
        champs = {c["category"]: c["full_name"] for c in out["champions"]}
        self.assertEqual(champs["scraping-data"], "scrapy/scrapy")
        self.assertEqual(champs["apis"], "public-apis/public-apis")
        self.assertEqual(len(out["new_crowns"]), 2)

        # crowns are sticky: second run with same data crowns nobody new
        with mock.patch.object(github, "fetch_repo", lambda n: (metas[n], None)), \
             mock.patch.object(github, "fetch_root_files", lambda n: []):
            out2 = ringer.run(con)
        self.assertEqual(out2["new_crowns"], [])

        # search finds by keyword ordered by score
        hits = db.search(con, "scraping")
        self.assertEqual(hits[0]["full_name"], "scrapy/scrapy")

        # export produces valid JSON with champions
        with tempfile.TemporaryDirectory() as d:
            champ_path, board_path = export.export(con, out_dir=d)
            data = json.load(open(champ_path))
            self.assertEqual(len(data["champions"]), 2)
            self.assertIn("scrapy/scrapy", open(board_path).read())
        os.unlink(path)

    def test_gone_repo_marked(self):
        con, path = fresh_con()
        db.add_repo(con, "no/where")
        with mock.patch.object(github, "fetch_repo", lambda n: (None, "gone")):
            ringer.run(con)
        r = db.all_repos(con)[0]
        self.assertEqual(r["status"], "gone")
        os.unlink(path)


class TestScouts(unittest.TestCase):
    TRENDING_HTML = """
    <article class="Box-row">
      <h2 class="h3 lh-condensed">
        <a href="/cool-org/hot-repo" data-hydro-click="x">cool-org / hot-repo</a>
      </h2>
    </article>
    <article class="Box-row">
      <h2 class="h3 lh-condensed"><a href="/dev/another.tool">dev / another.tool</a></h2>
    </article>
    <a href="/login?return_to=x">login</a>
    """

    def test_parse_trending(self):
        self.assertEqual(scouts.parse_trending(self.TRENDING_HTML),
                         ["cool-org/hot-repo", "dev/another.tool"])

    def test_parse_hn_filters(self):
        now = 1_000_000_000
        payload = {"hits": [
            {"points": 120, "created_at_i": now - 86400,
             "url": "https://github.com/fresh/winner", "title": "Show HN"},
            {"points": 3, "created_at_i": now - 86400,
             "url": "https://github.com/too/quiet", "title": ""},
            {"points": 500, "created_at_i": now - 90 * 86400,
             "url": "https://github.com/way/old", "title": ""},
            {"points": 80, "created_at_i": now - 3600, "url": "",
             "title": "New tool", "story_text": "code at github.com/inline/mention"},
        ]}
        self.assertEqual(scouts.parse_hn(payload, min_points=10, now=now),
                         ["fresh/winner", "inline/mention"])

    def test_run_queues_new(self):
        con, path = fresh_con()
        with mock.patch.object(scouts, "SCOUTS",
                               [("fake", lambda progress=None: ["a/b", "c/d", "a/b"])]):
            out = scouts.run(con=con)
        self.assertEqual(out["new_repos"], ["a/b", "c/d"])
        self.assertEqual(db.all_repos(con)[0]["source"], "scout")
        os.unlink(path)


class TestTweetProcessing(unittest.TestCase):
    def test_process_tweet_refs_mocked(self):
        con, path = fresh_con()
        tweet = {"text": "insane repo https://github.com/foo/bar go star it",
                 "entities": {"urls": []}, "user": {"screen_name": "dev"}}
        with mock.patch.object(xwatcher, "fetch_tweet", lambda tid: tweet):
            out = xwatcher.process_tweet_refs(
                ["https://x.com/i/status/99912345678"], con=con)
        self.assertEqual(out["new_repos"], ["foo/bar"])
        # second pass: already seen
        with mock.patch.object(xwatcher, "fetch_tweet", lambda tid: tweet):
            out2 = xwatcher.process_tweet_refs(["99912345678"], con=con)
        self.assertEqual(out2["already_seen"], 1)
        os.unlink(path)


if __name__ == "__main__":
    unittest.main()
