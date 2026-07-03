"""Assign every repo to a category so rivals compete in the same ring.

Keyword-based and transparent: topics count double, then description,
name and language. First category to score wins; ties break by list order
(most specific first).
"""

CATEGORIES = [
    ("ai-agents",     ["agent", "agents", "agentic", "autonomous", "multi-agent",
                       "browser-use", "computer-use", "crew", "swarm", "copilot"]),
    ("llm-tools",     ["llm", "gpt", "claude", "openai", "anthropic", "gemini", "llama",
                       "rag", "prompt", "fine-tune", "finetune", "inference", "embedding",
                       "transformer", "chatbot", "langchain", "ollama"]),
    ("ai-media",      ["diffusion", "stable-diffusion", "image-generation", "text-to-image",
                       "text-to-video", "text-to-speech", "tts", "speech", "voice", "whisper",
                       "comfyui", "genai-media"]),
    ("scraping-data", ["scraper", "scraping", "crawler", "crawl", "spider", "parser",
                       "extraction", "playwright", "puppeteer", "selenium"]),
    ("apis",          ["api", "apis", "rest", "graphql", "openapi", "webhook", "sdk"]),
    ("devtools",      ["cli", "developer-tools", "devtools", "productivity", "terminal",
                       "editor", "vscode", "debugger", "linter", "formatter", "git",
                       "dotfiles", "shell"]),
    ("web-dev",       ["react", "nextjs", "next.js", "vue", "svelte", "frontend", "css",
                       "tailwind", "ui", "component", "website", "web-app", "javascript",
                       "typescript", "node"]),
    ("mobile",        ["android", "ios", "flutter", "react-native", "swift", "kotlin",
                       "mobile", "app-store", "expo"]),
    ("automation",    ["automation", "workflow", "n8n", "zapier", "cron", "bot", "pipeline",
                       "orchestration", "no-code", "low-code"]),
    ("data-ml",       ["machine-learning", "deep-learning", "data-science", "pytorch",
                       "tensorflow", "pandas", "notebook", "jupyter", "dataset",
                       "analytics", "visualization", "sql", "database", "vector"]),
    ("security",      ["security", "pentest", "pentesting", "vulnerability", "ctf", "osint",
                       "encryption", "privacy", "auth", "authentication", "password"]),
    ("self-hosted",   ["self-hosted", "selfhosted", "docker", "kubernetes", "homelab",
                       "server", "backup", "sync", "nas", "proxy", "vpn"]),
    ("learning",      ["awesome", "list", "curated", "roadmap", "interview", "tutorial",
                       "course", "learning", "handbook", "cheatsheet", "examples",
                       "resources", "collection"]),
    ("games",         ["game", "games", "gamedev", "unity", "godot", "minecraft", "emulator"]),
]

CATEGORY_NAMES = [c for c, _ in CATEGORIES] + ["other", "uncategorised"]


def categorise(repo):
    """repo: dict with topics (list), description, full_name, language."""
    topics = [str(t).lower() for t in (repo.get("topics") or [])]
    desc = (repo.get("description") or "").lower()
    name = (repo.get("full_name") or "").lower()
    lang = (repo.get("language") or "").lower()

    best, best_score = "other", 0
    for cat, keywords in CATEGORIES:
        score = 0
        for kw in keywords:
            if kw in topics:
                score += 2
            if kw in desc:
                score += 1
            if kw in name:
                score += 1
            if kw == lang:
                score += 1
        if score > best_score:
            best, best_score = cat, score
    return best
