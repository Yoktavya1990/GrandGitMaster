# ♛ GrandGitMaster

*Like a chess Grandmaster — but for free tools. You wish it. We rank it. You click it.*

**📱 Just want the app? → https://raw.githack.com/Yoktavya1990/GrandGitMaster/gh-pages/index.html** — open on your phone, "Add to Home Screen", done. No account, no install, no code.

**The king of Git.** A second brain that collects Git repositories from anywhere — X.com, agents, files, you — runs every one of them through **the Ringer** (a transparent scoring pipeline), categorises them so rivals fight in the same ring, and **crowns the best repo per category**. The crowns update automatically as repos rise and fall.

Built for **non-coders and vibe coders**: instead of jargon you get a **GrandScore (0–100)**, a medal verdict, and plain-language flags like *🚀 One-click ready* and *⚠️ Might be abandoned*.

Built for **agents**: Claude Code, Codex, Cursor — anything that speaks MCP gets the whole kingdom as tools, one config line away.

**Zero dependencies.** Pure Python 3.9+ standard library. If you have Python, you have GrandGitMaster — laptop, phone (PWA), VPS, Docker, GitHub Actions.

---

## Quickstart (under a minute)

```bash
git clone https://github.com/Yoktavya1990/GrandGitMaster && cd GrandGitMaster

./ggm ingest seeds/repos.txt     # load the seed catalogue
./ggm x pull                     # pull every repo mentioned in seeds/x_watchlist.txt (no X API key!)
./ggm ringer                     # 🥊 enrich, score, categorise, crown
./ggm top                        # 👑 meet your category kings
./ggm serve                      # 📱 mobile app at http://localhost:8477
```

> Tip: `export GITHUB_TOKEN=ghp_...` raises the GitHub API limit from 60 to 5000 req/h. Any classic or fine-grained token works, no special scopes needed for public repos.

## The mobile app 📱

**Hosted, nothing to run:** 👉 **https://raw.githack.com/Yoktavya1990/GrandGitMaster/gh-pages/index.html** — open it on your phone, **Add to Home Screen**, done.

*(Prefer the cleaner `https://yoktavya1990.github.io/GrandGitMaster/` URL? One tap enables it: repo **Settings → Pages → Source: Deploy from a branch → `gh-pages`**. The deploy workflow keeps that branch fresh either way.)* It reads the leaderboard the cloud Ringer refreshes every 6 hours, and its ＋ buttons open GitHub's mobile editor on the seed files — saving an edit there re-triggers the Ringer automatically. Fully handheld: find a repo link on X, paste it into the watchlist from your phone, and the kingdom re-ranks itself.

### Self-hosted mode (optional)

`./ggm serve`, open `http://<machine-ip>:8477` on your phone, hit **Add to Home Screen**. You now have a full-screen installable app: search "scraping" or "agents", see champions with crowns, score meters, medals, and one-tap ingest — paste any GitHub or X link into the bottom bar and it enters the pipeline. Runs identically on a $5 VPS for access from anywhere.

## Your agents' second brain 🧠 (MCP)

This repo ships a zero-dependency MCP server. Hook it into every project:

**Claude Code** — from any project directory:
```bash
claude mcp add grandgitmaster -- python3 -m grandgitmaster mcp
```
(or copy this repo's `.mcp.json` into a project; set `PYTHONPATH` or `pip install -e .` so the module resolves).

**Codex CLI** — in `~/.codex/config.toml`:
```toml
[mcp_servers.grandgitmaster]
command = "python3"
args = ["-m", "grandgitmaster", "mcp"]
```

Tools your agents get: `best_repo`, `search_repos`, `top_repos`, `add_repo`, `ingest_text`, `pull_tweets`, `run_ringer`, `list_categories`. So mid-task an agent can ask *"what's our crowned repo for web scraping?"* and get the answer in one call — or feed a tweet it just saw straight into the Ringer.

All your projects share one brain: the database lives at `data/ggm.db` (override with `GGM_DB=/path/to/ggm.db` to point every project and agent at the same file).

## The X.com watcher 🐦

Never trawl X for repos again. Three ways in, zero to full automation:

1. **Tweet links, no API key** — the killer feature. Drop any `x.com/.../status/...` link into `seeds/x_watchlist.txt` (or pass it directly) and:
   ```bash
   ./ggm x pull https://x.com/i/status/2072671669278195775
   ```
   GrandGitMaster fetches the tweet through X's public syndication endpoint, follows every `t.co` link, extracts each GitHub repo, and queues it for the Ringer. Works today, costs nothing.

2. **Sleuth mode** — most viral tweets *name* a project ("Alibaba open-sourced PageAgent") without linking it. `./ggm x sleuth` takes every stored tweet that had no direct link, extracts candidate project names, and hunts down the exact-name repo via GitHub search. Only exact name matches are accepted, so precision stays high.

3. **Full auto-search** — with an [X API v2 bearer token](https://developer.x.com):
   ```bash
   export X_BEARER_TOKEN=...
   ./ggm x watch          # finds viral tweets linking github.com, all repos → the Ringer
   ```

4. **Anything else** — `./ggm ingest bookmarks.txt` (or pipe to `./ggm ingest -`) rips every GitHub URL out of any text: exported bookmarks, newsletters, chat logs.

## The Ringer 🥊

Every repo gets a **GrandScore (0–100)** from six transparent components:

| Component | Max | Question it answers |
|---|---:|---|
| Popularity | 25 | Do people love it? (stars, log scale) |
| Freshness | 20 | Is it alive? (days since last push) |
| Maintenance | 15 | Is it looked after? (not archived, issue load sane) |
| Community | 10 | Do people build on it? (forks) |
| Docs | 15 | Will a human understand it? (description, license, topics, homepage) |
| One-click | 15 | Can you run it NOW? (Dockerfile, compose, lockfiles, installers) |

Verdicts: **👑 Legendary (85+) · 🥇 Excellent (70+) · 🥈 Solid (55+) · 🥉 Decent (40+) · 🧪 Experimental**

Repos are auto-categorised (ai-agents, llm-tools, scraping-data, apis, devtools, web-dev, mobile, automation, security, self-hosted, learning…) and the top scorer of each category is **crowned**. Crown changes are tracked in history — you can watch kings rise and fall. `./ggm star` even GitHub-stars all current champions for you (needs `GITHUB_TOKEN` with starring permission).

## Cloud mode ☁️

Two options, both included:

- **GitHub Actions (free)** — `.github/workflows/ringer.yml` runs every 6 hours: pulls the X watchlist, runs the Ringer, and commits `data/champions.json` + `data/LEADERBOARD.md`. The repo becomes a living leaderboard, and every project you own can consume it with one GET:
  ```
  https://raw.githubusercontent.com/Yoktavya1990/GrandGitMaster/main/data/champions.json
  ```
- **Docker** — `docker compose up -d` gives you the mobile app plus an hourly watcher/ringer loop on any box.

## CLI cheat sheet

```
./ggm add <repo|url>...      add repos            ./ggm best <query>   THE repo for a need
./ggm ingest <file|->        rip repos from text  ./ggm top [category] leaderboards
./ggm x pull [links]         X links → repos      ./ggm search <query> search catalogue
./ggm x sleuth               hunt named repos     ./ggm serve          mobile app + API
./ggm x watch                auto X search        
./ggm ringer [--pending]     score + crown        ./ggm mcp            agent brain (MCP)
./ggm export                 champions.json + MD  ./ggm star           star champions
```

## Design notes

- **Local-first**: one SQLite file, `data/ggm.db`. Copy it anywhere, back it up with `cp`.
- **Zero deps**: stdlib only — nothing to install, nothing to break, runs on any Python 3.9+.
- **Honest scores**: every score ships its breakdown (`breakdown` in the API/JSON) so you can see exactly why a repo ranks where it does.
- **Graceful offline**: no GitHub API? Repos queue as ⏳ pending and rank on the next Ringer run.

MIT licensed. Long live the king. 👑
