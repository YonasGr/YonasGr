#!/usr/bin/env python3
"""Generates the animated SVG assets used by the profile README.

Run:  python3 scripts/build_assets.py
Pure stdlib. Output goes to ./assets. Edit the DATA blocks below to customise.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

FONT = "'JetBrains Mono','SF Mono','Fira Code',Consolas,'DejaVu Sans Mono',monospace"
SANS = "'Segoe UI',Inter,-apple-system,'Helvetica Neue',Arial,sans-serif"
BLUE, VIOLET, CYAN, GREEN, AMBER, PINK = "#4F8EF7", "#8B5CF6", "#22D3EE", "#10B981", "#F59E0B", "#F472B6"
BG1, BG2 = "#0B1020", "#111A3A"


def write(name, body, w, h, title):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{escape(title)}">\n<title>{escape(title)}</title>\n{body}\n</svg>\n'
    )
    (OUT / name).write_text(svg, encoding="utf-8")
    print("wrote", name, len(svg) // 1024, "KB")


def defs_common(uid=""):
    return f"""<defs>
  <linearGradient id="bg{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>
  <linearGradient id="brand{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}"/><stop offset=".55" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
  <filter id="blur{uid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="40"/></filter>
  <filter id="glow{uid}" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>"""


# ───────────────────────────── HERO ─────────────────────────────
def hero():
    W, H = 1000, 340
    taglines = [
        "Full Stack Software Engineer",
        "React Native &amp; Expo Developer",
        "FastAPI · TypeScript · PostgreSQL",
        "Cloud &amp; DevOps · Azure + Docker",
        "Building systems that thrive in production",
    ]
    n = len(taglines)
    lines = ""
    for i, t in enumerate(taglines):
        s, e = i / n, (i + 1) / n
        fade = 0.025
        kt = f"0;{max(s - 0.0001, 0):.4f};{s + fade:.4f};{e - fade:.4f};{e:.4f};1"
        lines += (
            f'<text x="500" y="232" text-anchor="middle" font-family="{FONT}" font-size="25" fill="#C7D2FE" opacity="{1 if i == 0 else 0}">'
            f'{t}<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="{n * 3.2}s" repeatCount="indefinite"/></text>\n'
        )
    tokens = [
        ("{ }", 70, 70, BLUE, 7), ("&lt;/&gt;", 880, 80, VIOLET, 9), ("async", 150, 290, CYAN, 8),
        ("await", 820, 290, PINK, 10), ("docker", 40, 190, GREEN, 11), ("=&gt;", 940, 190, AMBER, 6),
        ("git", 260, 60, CYAN, 12), ("API", 740, 50, BLUE, 8), ("0x1F", 600, 305, VIOLET, 9), ("npm", 400, 310, GREEN, 7),
    ]
    tk = ""
    for txt, x, y, c, d in tokens:
        tk += (
            f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="18" fill="{c}" opacity=".35" text-anchor="middle">{txt}'
            f'<animate attributeName="y" values="{y};{y - 14};{y}" dur="{d}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values=".15;.5;.15" dur="{d}s" repeatCount="indefinite"/></text>\n'
        )
    body = f"""{defs_common()}
<clipPath id="clip"><rect width="{W}" height="{H}" rx="22"/></clipPath>
<g clip-path="url(#clip)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <circle cx="200" cy="90" r="150" fill="{BLUE}" opacity=".35" filter="url(#blur)"><animate attributeName="cx" values="200;420;200" dur="14s" repeatCount="indefinite"/><animate attributeName="cy" values="90;200;90" dur="11s" repeatCount="indefinite"/></circle>
  <circle cx="820" cy="260" r="160" fill="{VIOLET}" opacity=".32" filter="url(#blur)"><animate attributeName="cx" values="820;600;820" dur="16s" repeatCount="indefinite"/><animate attributeName="cy" values="260;120;260" dur="12s" repeatCount="indefinite"/></circle>
  <circle cx="520" cy="320" r="110" fill="{CYAN}" opacity=".18" filter="url(#blur)"><animate attributeName="cx" values="520;300;520" dur="18s" repeatCount="indefinite"/></circle>
  <g stroke="#6B7FD7" stroke-opacity=".12" stroke-width="1">
    {''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H + 40}"/>' for x in range(0, W + 1, 50))}
    {''.join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(0, H + 1, 50))}
    <animateTransform attributeName="transform" type="translate" values="0 0;0 50" dur="4s" repeatCount="indefinite"/>
  </g>
  {tk}
  <text x="500" y="46" text-anchor="middle" font-family="{FONT}" font-size="14" fill="{CYAN}" letter-spacing="6">HELLO WORLD, I'M</text>
  <text x="500" y="150" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="86" fill="url(#brand)" filter="url(#glow)" letter-spacing="2">YONAS GIRMA
    <animate attributeName="opacity" values="0;1" dur="1.2s" fill="freeze"/></text>
  <rect x="380" y="172" width="240" height="3" rx="1.5" fill="url(#brand)"><animate attributeName="width" values="0;240;240" keyTimes="0;.3;1" dur="3s" fill="freeze"/><animate attributeName="x" values="500;380;380" keyTimes="0;.3;1" dur="3s" fill="freeze"/></rect>
  <text x="500" y="205" text-anchor="middle" font-family="{FONT}" font-size="14" fill="#64748B">&gt;_ currently:</text>
  {lines}
  <g transform="translate(40 306)">
    <circle cx="6" cy="0" r="6" fill="{GREEN}"><animate attributeName="r" values="5;8;5" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;.4;1" dur="2s" repeatCount="indefinite"/></circle>
    <text x="22" y="5" font-family="{FONT}" font-size="13" fill="#94A3B8">building in public · Ethiopia</text>
  </g>
  <text x="960" y="311" text-anchor="end" font-family="{FONT}" font-size="13" fill="#475569">student × engineer × builder</text>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="22" fill="none" stroke="url(#brand)" stroke-opacity=".6"/>"""
    write("hero.svg", body, W, H, "Yonas Girma: full stack software engineer")


# ─────────────────────────── TERMINAL ───────────────────────────
def terminal():
    W, H = 900, 400
    CW, FS = 9.6, 16  # char width at 16px monospace
    script = [
        ("whoami", "yonas girma · full stack software engineer", "#E2E8F0"),
        ("cat stack.txt", "TypeScript · Python · React Native · FastAPI · PostgreSQL · Docker · Azure", CYAN),
        ("ls ~/projects", "logos-path/   safari-game-zone/   binance-p2p-bot/", AMBER),
        ("cat now.txt", "learning → system design · security · networking · cloud", GREEN),
        ("echo $GOAL", '"engineer software that doesn\'t just work, it thrives in production"', PINK),
    ]
    SLOT, TOTAL = 0.1, 26.0
    N = int(TOTAL / SLOT)
    x0, y0, lh = 34, 84, 58
    clips, texts, cursors = "", "", ""
    t = 1.0
    for i, (cmd, out, col) in enumerate(script):
        y = y0 + i * lh
        cmd_full = "$ " + cmd
        cmd_start = t
        cmd_slots = len(cmd_full)
        cmd_end = cmd_start + cmd_slots * 0.07
        out_start = cmd_end + 0.35
        out_slots = max(8, len(out) // 2)
        out_end = out_start + out_slots * 0.05
        t = out_end + 0.55

        def widths(start, end, chars):
            vals = []
            for s in range(N):
                ts = s * SLOT
                if ts < start:
                    v = 0
                elif ts >= end:
                    v = chars * CW
                else:
                    frac = (ts - start) / (end - start)
                    v = int(frac * chars + 1) * CW
                vals.append(f"{min(v, chars * CW):.1f}")
            return ";".join(vals)

        def curs(start, end, x_base, chars):
            xs, ops = [], []
            for s in range(N):
                ts = s * SLOT
                if start <= ts < end:
                    frac = (ts - start) / (end - start)
                    xs.append(f"{x_base + int(frac * chars + 1) * CW:.1f}")
                    ops.append("1")
                else:
                    xs.append(f"{x_base:.1f}")
                    ops.append("0")
            return ";".join(xs), ";".join(ops)

        clips += (
            f'<clipPath id="c{i}a"><rect x="{x0}" y="{y - 20}" height="26" width="0"><animate attributeName="width" values="{widths(cmd_start, cmd_end, cmd_slots)}" dur="{TOTAL}s" calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>\n'
            f'<clipPath id="c{i}b"><rect x="{x0}" y="{y + 4}" height="26" width="0"><animate attributeName="width" values="{widths(out_start, out_end, len(out))}" dur="{TOTAL}s" calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>\n'
        )
        texts += (
            f'<text x="{x0}" y="{y}" font-family="{FONT}" font-size="{FS}" clip-path="url(#c{i}a)" xml:space="preserve"><tspan fill="{GREEN}">$ </tspan><tspan fill="#E2E8F0">{escape(cmd)}</tspan></text>\n'
            f'<text x="{x0}" y="{y + 26}" font-family="{FONT}" font-size="{FS}" fill="{col}" clip-path="url(#c{i}b)" xml:space="preserve">{escape(out)}</text>\n'
        )
        cx, co = curs(cmd_start, out_start, x0, cmd_slots)
        ox, oo = curs(out_start, out_end + 0.3, x0, len(out))
        cursors += (
            f'<rect y="{y - 15}" width="9" height="18" fill="{CYAN}" x="{x0}" opacity="0"><animate attributeName="x" values="{cx}" dur="{TOTAL}s" calcMode="discrete" repeatCount="indefinite"/><animate attributeName="opacity" values="{co}" dur="{TOTAL}s" calcMode="discrete" repeatCount="indefinite"/></rect>\n'
            f'<rect y="{y + 11}" width="9" height="18" fill="{col}" x="{x0}" opacity="0"><animate attributeName="x" values="{ox}" dur="{TOTAL}s" calcMode="discrete" repeatCount="indefinite"/><animate attributeName="opacity" values="{oo}" dur="{TOTAL}s" calcMode="discrete" repeatCount="indefinite"/></rect>\n'
        )
    last_y = y0 + len(script) * lh
    body = f"""{defs_common("t")}
{clips}
<rect width="{W}" height="{H}" rx="14" fill="#0D1117"/>
<rect width="{W}" height="42" rx="14" fill="#161B22"/><rect y="28" width="{W}" height="14" fill="#161B22"/>
<circle cx="26" cy="21" r="7" fill="#FF5F56"/><circle cx="48" cy="21" r="7" fill="#FFBD2E"/><circle cx="70" cy="21" r="7" fill="#27C93F"/>
<text x="{W // 2}" y="26" text-anchor="middle" font-family="{FONT}" font-size="13" fill="#8B949E">yonas@dev: ~/about</text>
<line x1="0" y1="42.5" x2="{W}" y2="42.5" stroke="#30363D"/>
{texts}{cursors}
<text x="{x0}" y="{last_y}" font-family="{FONT}" font-size="{FS}" fill="{GREEN}">$ <animate attributeName="opacity" values="0;0;1" keyTimes="0;.9;1" dur="{TOTAL}s" repeatCount="indefinite"/></text>
<rect x="{x0 + 2 * CW}" y="{last_y - 15}" width="9" height="18" fill="{CYAN}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="#30363D"/>"""
    write("terminal.svg", body, W, H, "Terminal introducing Yonas Girma")


# ─────────────────────────── SKILLS ───────────────────────────
SKILLS = [  # (name, level 1-5, status, colour)  ← edit these to match reality
    ("Python", 5, "daily driver", BLUE), ("TypeScript", 5, "daily driver", BLUE),
    ("React Native / Expo", 4, "shipping apps", CYAN), ("FastAPI", 4, "shipping apis", GREEN),
    ("PostgreSQL / Supabase", 4, "comfortable", VIOLET), ("Docker", 4, "comfortable", CYAN),
    ("Firebase", 4, "comfortable", AMBER), ("Linux & Bash", 3, "comfortable", GREEN),
    ("Azure / CI-CD", 3, "levelling up", PINK), ("System design", 3, "levelling up", PINK),
    ("Security", 2, "learning", AMBER), ("Networking", 2, "learning", AMBER),
]


def skills():
    W, colw, rowh = 940, 450, 58
    rows = (len(SKILLS) + 1) // 2
    H = 70 + rows * rowh
    body = f"""{defs_common("s")}
<rect width="{W}" height="{H}" rx="16" fill="url(#bgs)"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="#2A3566"/>
<text x="30" y="40" font-family="{FONT}" font-size="14" fill="{CYAN}">// skill_levels.ts   <tspan fill="#64748B">(1–5 · where I'm strongest today)</tspan></text>
"""
    for i, (name, lvl, status, col) in enumerate(SKILLS):
        cx = 30 + (i % 2) * (colw + 20)
        cy = 70 + (i // 2) * rowh
        pip_w = 62
        body += f'<text x="{cx}" y="{cy + 14}" font-family="{SANS}" font-weight="600" font-size="16" fill="#E2E8F0">{escape(name)}</text>\n'
        body += f'<text x="{cx + colw - 30}" y="{cy + 14}" text-anchor="end" font-family="{FONT}" font-size="12" fill="#64748B">{status}</text>\n'
        for p in range(5):
            x = cx + p * (pip_w + 6)
            body += f'<rect x="{x}" y="{cy + 24}" width="{pip_w}" height="10" rx="5" fill="#1E2749"/>\n'
            if p < lvl:
                d = 0.15 * (i % 2) + p * 0.12 + (i // 2) * 0.1
                body += (
                    f'<rect x="{x}" y="{cy + 24}" width="{pip_w}" height="10" rx="5" fill="{col}" opacity="0">'
                    f'<animate attributeName="opacity" values="0;1" begin="{d:.2f}s" dur=".4s" fill="freeze"/>'
                    f'<animate attributeName="width" values="0;{pip_w}" begin="{d:.2f}s" dur=".5s" fill="freeze"/></rect>\n'
                )
    write("skills.svg", body, W, H, "Skill levels")


# ─────────────────────── SECTION BANNERS ───────────────────────
SECTIONS = [
    ("about", "01", "About me", "who I am and how I think"),
    ("now", "02", "Right now", "what I'm building and learning"),
    ("principles", "03", "How I build", "principles, workflow and habits"),
    ("skills", "04", "Skills & stack", "tools I reach for"),
    ("projects", "05", "Featured projects", "things I've shipped"),
    ("activity", "06", "Live activity", "auto-updated from GitHub"),
    ("stats", "07", "Stats & contributions", "numbers, languages, rhythm"),
    ("contact", "08", "Let's talk", "collaborations, questions, ideas"),
]


def section_banners():
    W, H = 940, 84
    for key, num, title, sub in SECTIONS:
        body = f"""{defs_common(key)}
<rect width="{W}" height="{H}" rx="14" fill="url(#bg{key})"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="#2A3566"/>
<rect x="0" y="18" width="5" height="48" rx="2.5" fill="url(#brand{key})"/>
<text x="28" y="34" font-family="{FONT}" font-size="13" fill="{CYAN}">// {num}</text>
<text x="28" y="64" font-family="{SANS}" font-weight="800" font-size="28" fill="#F1F5F9">{escape(title)}</text>
<text x="{W - 28}" y="48" text-anchor="end" font-family="{FONT}" font-size="14" fill="#64748B">{escape(sub)}</text>
<rect x="0" y="{H - 3}" width="140" height="3" fill="url(#brand{key})"><animate attributeName="x" values="-140;{W}" dur="4.5s" repeatCount="indefinite"/></rect>"""
        write(f"section-{key}.svg", body, W, H, title)


# ───────────────────────── PROJECT CARDS ─────────────────────────
def project_card(slug, title, tagline, chips, accent, accent2, art, badge):
    W, H = 450, 250
    chip_svg, x = "", 24
    for c in chips:
        w = len(c) * 7.4 + 18
        chip_svg += (
            f'<rect x="{x}" y="196" width="{w:.0f}" height="24" rx="12" fill="{accent}" fill-opacity=".16" stroke="{accent}" stroke-opacity=".5"/>'
            f'<text x="{x + w / 2:.0f}" y="212" text-anchor="middle" font-family="{FONT}" font-size="11.5" fill="#E2E8F0">{escape(c)}</text>\n'
        )
        x += w + 8
    body = f"""<defs>
  <linearGradient id="g{slug}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>
  <linearGradient id="a{slug}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent2}"/></linearGradient>
  <filter id="f{slug}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter>
  <clipPath id="k{slug}"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#k{slug})">
<rect width="{W}" height="{H}" fill="url(#g{slug})"/>
<circle cx="380" cy="40" r="110" fill="{accent}" opacity=".3" filter="url(#f{slug})"/>
{art}
<text x="24" y="40" font-family="{FONT}" font-size="11" fill="{accent}" letter-spacing="2">{escape(badge)}</text>
<text x="24" y="86" font-family="{SANS}" font-weight="800" font-size="31" fill="url(#a{slug})">{escape(title)}</text>
<text x="24" y="116" font-family="{SANS}" font-size="15" fill="#CBD5E1">{escape(tagline[0])}</text>
<text x="24" y="138" font-family="{SANS}" font-size="15" fill="#CBD5E1">{escape(tagline[1])}</text>
<line x1="24" y1="164" x2="{W - 24}" y2="164" stroke="#2A3566"/>
<text x="24" y="184" font-family="{FONT}" font-size="11" fill="#64748B">STACK</text>
{chip_svg}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{accent}" stroke-opacity=".5"/>"""
    write(f"project-{slug}.svg", body, W, H, f"{title}: {tagline[0]} {tagline[1]}")


def projects():
    # Logos Path: orbiting rings + cross of light
    art1 = f"""<g transform="translate(375 70)">
  <circle r="46" fill="none" stroke="{VIOLET}" stroke-opacity=".35"/><circle r="28" fill="none" stroke="{VIOLET}" stroke-opacity=".5"/>
  <g><circle cx="46" r="5" fill="{CYAN}"/><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="9s" repeatCount="indefinite"/></g>
  <g><circle cx="-28" r="4" fill="{PINK}"/><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="6s" repeatCount="indefinite"/></g>
  <rect x="-3" y="-18" width="6" height="36" rx="3" fill="#F1F5F9" opacity=".9"/><rect x="-12" y="-8" width="24" height="6" rx="3" fill="#F1F5F9" opacity=".9"/>
  <animate attributeName="opacity" values=".7;1;.7" dur="4s" repeatCount="indefinite"/></g>"""
    project_card("logospath", "Logos Path", ("AI-powered Bible study: daily reading,", "reflection, quizzes, streaks & cloud sync."),
                 ["React Native", "Expo", "Firebase", "AI"], VIOLET, CYAN, art1, "MOBILE · ANDROID + IOS")
    # Safari: bouncing bingo balls
    balls = ""
    for i, (cx, num, col, d) in enumerate([(335, "B7", GREEN, 2.4), (375, "I22", AMBER, 3.1), (415, "N41", PINK, 2.7)]):
        balls += (
            f'<g><circle cx="{cx}" cy="64" r="19" fill="{col}"/><circle cx="{cx}" cy="64" r="12" fill="#fff" fill-opacity=".92"/>'
            f'<text x="{cx}" y="68" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="10" fill="#0B1020">{num}</text>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -16;0 0" dur="{d}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines=".4 0 .6 1;.4 0 .6 1"/></g>'
        )
    project_card("safari", "Safari Game Zone", ("Multiplayer 75 & 90-ball Bingo with", "server-verified claims and auditable RNG."),
                 ["Python", "FastAPI", "PostgreSQL", "Supabase", "Docker"], GREEN, CYAN, balls, "TELEGRAM MINI APP")
    # Binance: drawing chart line
    pts = "M0,60 L30,44 L58,52 L90,24 L120,36 L150,10 L180,22"
    art3 = f"""<g transform="translate(302 24) scale(.72)">
  <rect x="-8" y="-10" width="196" height="84" rx="10" fill="#0B1020" fill-opacity=".55" stroke="{AMBER}" stroke-opacity=".35"/>
  <path d="{pts}" fill="none" stroke="{AMBER}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="260" stroke-dashoffset="260">
    <animate attributeName="stroke-dashoffset" values="260;0;0;260" keyTimes="0;.45;.85;1" dur="6s" repeatCount="indefinite"/></path>
  <circle r="5" fill="{AMBER}"><animateMotion dur="6s" repeatCount="indefinite" keyTimes="0;.45;1" keyPoints="0;1;1" calcMode="linear" path="{pts}"/></circle>
  <text x="2" y="68" font-family="{FONT}" font-size="10" fill="#94A3B8">USDT/ETB · live</text></g>"""
    project_card("binance", "Binance P2P Bot", ("Live P2P rates in Ethiopian Birr, charts,", "conversion and inline mode on Telegram."),
                 ["Python", "Telegram API", "Matplotlib"], AMBER, PINK, art3, "TELEGRAM BOT")


# ─────────────────────────── DIVIDER + FOOTER ───────────────────────────
def divider():
    W, H = 940, 24
    body = f"""{defs_common("d")}
<line x1="0" y1="12" x2="{W}" y2="12" stroke="#2A3566" stroke-width="2" stroke-dasharray="2 8" stroke-linecap="round"/>
<circle cy="12" r="5" fill="{CYAN}" filter="url(#glowd)"><animate attributeName="cx" values="0;{W};0" dur="9s" repeatCount="indefinite"/></circle>
<circle cy="12" r="3" fill="{VIOLET}"><animate attributeName="cx" values="{W};0;{W}" dur="9s" repeatCount="indefinite"/></circle>"""
    write("divider.svg", body, W, H, "divider")


def footer():
    W, H = 1000, 190
    quotes = ["Thanks for stopping by 👋", "Ship small. Ship often.", "Let's build something great.", "Always learning. Always shipping."]
    n, qs = len(quotes), ""
    for i, q in enumerate(quotes):
        s, e = i / n, (i + 1) / n
        kt = f"0;{max(s - .0001, 0):.4f};{s + .03:.4f};{e - .03:.4f};{e:.4f};1"
        qs += (f'<text x="500" y="108" text-anchor="middle" font-family="{SANS}" font-weight="700" font-size="30" fill="#F1F5F9" opacity="{1 if i == 0 else 0}">{q}'
               f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="{n * 3.5}s" repeatCount="indefinite"/></text>\n')
    stars = ""
    import random
    random.seed(7)
    for _ in range(40):
        x, y, r, d = random.randint(10, 990), random.randint(8, 150), random.choice([1, 1.4, 1.8]), random.uniform(2, 5)
        stars += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff"><animate attributeName="opacity" values=".1;.9;.1" dur="{d:.1f}s" repeatCount="indefinite"/></circle>'
    body = f"""{defs_common("f")}
<clipPath id="cf"><rect width="{W}" height="{H}" rx="22"/></clipPath>
<g clip-path="url(#cf)">
<rect width="{W}" height="{H}" fill="url(#bgf)"/>
{stars}
<circle cx="150" cy="190" r="130" fill="{BLUE}" opacity=".3" filter="url(#blurf)"/><circle cx="860" cy="190" r="140" fill="{VIOLET}" opacity=".3" filter="url(#blurf)"/>
{qs}
<text x="500" y="146" text-anchor="middle" font-family="{FONT}" font-size="13" fill="#64748B">© Yonas Girma · built with care, SVG &amp; GitHub Actions</text>
<path d="M0 {H - 14} Q 250 {H - 38} 500 {H - 14} T 1000 {H - 14}" fill="none" stroke="url(#brandf)" stroke-width="3"><animate attributeName="d" values="M0 {H - 14} Q 250 {H - 38} 500 {H - 14} T 1000 {H - 14};M0 {H - 14} Q 250 {H + 8} 500 {H - 14} T 1000 {H - 14};M0 {H - 14} Q 250 {H - 38} 500 {H - 14} T 1000 {H - 14}" dur="6s" repeatCount="indefinite"/></path>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="22" fill="none" stroke="url(#brandf)" stroke-opacity=".6"/>"""
    write("footer.svg", body, W, H, "Thanks for stopping by")


if __name__ == "__main__":
    hero(); terminal(); skills(); section_banners(); projects(); divider(); footer()
