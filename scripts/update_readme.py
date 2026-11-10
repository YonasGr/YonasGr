#!/usr/bin/env python3
"""Refreshes the auto-generated blocks of README.md from the GitHub API.

Blocks (replace everything between the markers):
  <!--REPOS:START--> ... <!--REPOS:END-->        latest active repositories
  <!--ACTIVITY:START--> ... <!--ACTIVITY:END-->  recent public activity
  <!--UPDATED:START--> ... <!--UPDATED:END-->    "last refreshed" stamp

Pure stdlib. Uses GITHUB_TOKEN if present (higher rate limit).
"""
import json, os, re, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

USER = os.environ.get("GH_USER", "YonasGr")
README = Path(__file__).resolve().parent.parent / "README.md"
MAX_REPOS, MAX_EVENTS = 6, 6
LANG_EMOJI = {"Python": "🐍", "TypeScript": "🔷", "JavaScript": "🟨", "Java": "☕", "Kotlin": "🟣",
              "C++": "⚙️", "HTML": "🌐", "CSS": "🎨", "Shell": "🐚", "Dart": "🎯", "Go": "🐹", "Rust": "🦀"}


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}", headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-readme-bot"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def ago(iso):
    d = datetime.now(timezone.utc) - datetime.fromisoformat(iso.replace("Z", "+00:00"))
    s = int(d.total_seconds())
    for n, unit in ((86400 * 30, "mo"), (86400, "d"), (3600, "h"), (60, "m")):
        if s >= n:
            return f"{s // n}{unit} ago"
    return "just now"


def clip(text, n=70):
    text = " ".join((text or "").split())
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def md_escape(t):
    return t.replace("|", "\\|").replace("\n", " ")


def render_repos(repos):
    own = [r for r in repos if not r["fork"] and r["name"].lower() != USER.lower() and not r["archived"]]
    own.sort(key=lambda r: r["pushed_at"], reverse=True)
    rows = ["| Repository | About | Lang | ⭐ | Updated |", "|:--|:--|:--|:-:|:--|"]
    for r in own[:MAX_REPOS]:
        lang = r["language"] or "-"
        rows.append(f"| [**{r['name']}**]({r['html_url']}) | {md_escape(clip(r['description'] or 'No description yet'))} | "
                    f"{LANG_EMOJI.get(lang, '📦')} {lang} | {r['stargazers_count']} | {ago(r['pushed_at'])} |")
    return "\n".join(rows) if len(rows) > 2 else "_No public repositories yet._"


def render_events(events):
    items = []
    for e in events:
        repo = e["repo"]["name"]
        link = f"[{repo.split('/')[-1]}](https://github.com/{repo})"
        t, p = e["type"], e.get("payload", {})
        if t == "PushEvent":
            commits = p.get("commits") or []
            n = p.get("size") or len(commits) or 1
            msg = f" — `{clip(commits[-1]['message'].splitlines()[0], 60)}`" if commits else ""
            line = f"⬆️ Pushed **{n}** commit{'s' if n != 1 else ''} to {link}{msg}"
        elif t == "CreateEvent" and p.get("ref_type") == "repository":
            line = f"🆕 Created repository {link}"
        elif t == "PullRequestEvent":
            line = f"🔀 {p.get('action', 'updated').capitalize()} a pull request in {link}"
        elif t == "IssuesEvent":
            line = f"🐛 {p.get('action', 'updated').capitalize()} an issue in {link}"
        elif t == "WatchEvent":
            line = f"⭐ Starred {link}"
        elif t == "ReleaseEvent":
            line = f"🚀 Published a release in {link}"
        else:
            continue
        if any(line == i[0] for i in items):
            continue
        items.append((line, ago(e["created_at"])))
        if len(items) >= MAX_EVENTS:
            break
    return "\n".join(f"- {l} · <sub>{t}</sub>" for l, t in items) or "_Nothing public to show yet._"


def replace_block(text, name, body):
    pat = re.compile(rf"(<!--{name}:START-->)(.*?)(<!--{name}:END-->)", re.S)
    if not pat.search(text):
        sys.exit(f"marker {name} not found in README")
    return pat.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(3)}", text)


def main():
    text = README.read_text(encoding="utf-8")
    text = replace_block(text, "REPOS", render_repos(api(f"/users/{USER}/repos?per_page=100&sort=pushed")))
    text = replace_block(text, "ACTIVITY", render_events(api(f"/users/{USER}/events/public?per_page=50")))
    stamp = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")
    text = replace_block(text, "UPDATED", f"<sub>🔄 Auto-refreshed on {stamp} by GitHub Actions</sub>")
    README.write_text(text, encoding="utf-8")
    print("README updated")


if __name__ == "__main__":
    main()
