"""Render the profile README cards (hero / about / skills / footer) as light and dark SVGs.

Usage: python scripts/render_cards.py

The cards only use system font stacks, so no webfont is needed: GitHub renders the
SVGs as <img>, where external fonts and styles cannot load.
"""
from html import escape
from pathlib import Path

FONT = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', "
        "'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans SC', Helvetica, Arial, sans-serif")
MONO = ("ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, "
        "'PingFang SC', 'Microsoft YaHei', monospace")

THEMES = {
    "light": dict(bg="#ffffff", card="#f8fafc", border="#e2e8f0", text="#0f172a",
                  muted="#64748b", faint="#cbd5e1", accent="#0369a1", accent2="#6d28d9",
                  chip="#f1f5f9"),
    "dark": dict(bg="#0d1117", card="#11161f", border="#222b38", text="#e6edf3",
                 muted="#8b97a8", faint="#4b5566", accent="#7dd3fc", accent2="#c4b5fd",
                 chip="#161d29"),
}

NAME = "Flandern"
TAGLINE = ("AI 应用开发 <tspan fill=\"url(#g)\">→ Agent / RAG 工程</tspan>")
SUBLINE = "白天写后端服务，晚上调模型与 Agent。"
HERO_CHIPS = ["Python", "Go", "TypeScript", "Docker", "MySQL"]

TERM_LINES = [
    ("$", "whoami", "text"),
    ("", "ai application developer", "muted"),
    ("$", "cat now.txt", "text"),
    ("", "llm apps & agent engineering:", "muted"),
    ("", "rag, react loops, fine-tuning", "muted"),
    ("$", "status", "text"),
]
TERM_LAST = "mostly building"

ABOUT = [
    ("AI", [
        "Tool、ReAct、Context",
        "LLM 应用层开发、Harness 工程",
        "推理部署、LoRA 微调、Dataset 构建",
    ]),
    ("后端", [
        "Go、Python 后端服务开发",
        "MySQL、Redis、消息队列",
        "Docker 容器化部署",
    ]),
    ("工程", [
        "CI/CD（GitHub Actions、Jenkins）",
        "调试、性能排查与问题定位",
        "Git 工作流（rebase / merge）",
    ]),
]

SKILL_GROUPS = [
    ("LANGUAGES", ["Go", "Python", "TypeScript"]),
    ("AI & AGENT", ["Tool", "ReAct", "Context", "RAG", "Harness", "LoRA"]),
    ("DATA & INFRA", ["MySQL", "Redis", "消息队列", "Docker", "Kubernetes", "Linux"]),
    ("WORKFLOW", ["GitHub Actions", "Jenkins", "Git", "Linux"]),
]

FOOTER_TITLE = "感谢访问我的 GitHub 主页"
FOOTER_SUB = "让我们一起探索 AI 与代码的无限可能"
FOOTER_META = "github.com/Flandern1211  ·  31@gmail.com"


def text_width(text, size):
    """Rough advance width; CJK glyphs are full-width, everything else ~0.62em."""
    return sum(size * (1.0 if ord(ch) > 0x2E80 else 0.62) for ch in text)


def svg(width, height, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(label)}">\n'
            f'{body}\n</svg>\n')


def card(width, height, t, radius=16):
    return (f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="{radius}" '
            f'fill="{t["card"]}" stroke="{t["border"]}"/>')


def chips(x, y, labels, t, size=11):
    out, cx = [], x
    for label in labels:
        w = text_width(label, size) + 18
        out.append(
            f'<rect x="{cx:.1f}" y="{y}" width="{w:.1f}" height="22" rx="11" '
            f'fill="{t["chip"]}" stroke="{t["border"]}"/>'
            f'<text x="{cx + w / 2:.1f}" y="{y + 15}" text-anchor="middle" '
            f'font-family="{MONO}" font-size="{size}" fill="{t["muted"]}">{escape(label)}</text>')
        cx += w + 8
    return "".join(out)


def hero(t):
    w, h = 880, 280
    term, y = [], 98
    for prompt, text, key in TERM_LINES:
        if prompt:
            term.append(f'<text x="534" y="{y}" font-family="{MONO}" font-size="13" '
                        f'fill="{t["accent"]}">$</text>')
        term.append(f'<text x="550" y="{y}" font-family="{MONO}" font-size="13" '
                    f'fill="{t[key]}">{escape(text)}</text>')
        y += 20
    cursor_x = 550 + text_width(TERM_LAST, 13) + 8
    term.append(f'<text x="550" y="{y}" font-family="{MONO}" font-size="13" '
                f'fill="{t["muted"]}">{escape(TERM_LAST)}</text>'
                f'<rect x="{cursor_x:.1f}" y="{y - 11}" width="8" height="14" fill="{t["accent"]}">'
                f'<animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/>'
                f'</rect>')
    body = f'''<defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["accent"]}"/><stop offset="1" stop-color="{t["accent2"]}"/></linearGradient>
<pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{t["border"]}"/></pattern>
</defs>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="{t["bg"]}" stroke="{t["border"]}"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="url(#dots)" opacity="0.6"/>
<text x="44" y="70" font-family="{MONO}" font-size="13" fill="{t["muted"]}">hi there, I'm</text>
<text x="42" y="122" font-family="{FONT}" font-size="50" font-weight="700" letter-spacing="-1.5" fill="{t["text"]}">{NAME}</text>
<rect x="44" y="140" width="64" height="3" rx="1.5" fill="url(#g)"/>
<text x="44" y="178" font-family="{FONT}" font-size="18" font-weight="600" fill="{t["text"]}">{TAGLINE}</text>
<text x="44" y="206" font-family="{FONT}" font-size="14" fill="{t["muted"]}">{escape(SUBLINE)}</text>
{chips(44, 228, HERO_CHIPS, t)}
<rect x="510" y="44" width="330" height="192" rx="12" fill="{t["chip"]}" stroke="{t["border"]}"/>
<circle cx="530" cy="64" r="4.5" fill="#ff5f57"/><circle cx="545" cy="64" r="4.5" fill="#febc2e"/><circle cx="560" cy="64" r="4.5" fill="#28c840"/>
<text x="824" y="68" text-anchor="end" font-family="{MONO}" font-size="11" fill="{t["faint"]}">~/flandern</text>
{"".join(term)}'''
    return svg(w, h, body, "Flandern, AI 应用开发 / Agent 与 RAG 工程 / 后端服务")


def about(t):
    w, h = 880, 200
    parts = [card(w, h, t, 14),
             f'<text x="32" y="44" font-family="{MONO}" font-size="11" letter-spacing="1" '
             f'fill="{t["accent"]}">ABOUT ME</text>']
    for i, (title, lines) in enumerate(ABOUT):
        x = 32 + i * 276
        parts.append(f'<text x="{x}" y="84" font-family="{FONT}" font-size="16" '
                     f'font-weight="700" fill="{t["text"]}">{escape(title)}</text>')
        for j, line in enumerate(lines):
            parts.append(f'<text x="{x}" y="{114 + j * 24}" font-family="{FONT}" '
                         f'font-size="13" fill="{t["muted"]}">{escape(line)}</text>')
    label = "关于我：" + "；".join(f"{title}：{'、'.join(lines)}" for title, lines in ABOUT)
    return svg(w, h, "\n".join(parts), label)


def skills(t):
    w, h = 880, 232
    parts = [card(w, h, t, 14),
             f'<text x="32" y="44" font-family="{MONO}" font-size="11" letter-spacing="1" '
             f'fill="{t["accent"]}">SKILLS &amp; TOOLS</text>']
    for i, (group, items) in enumerate(SKILL_GROUPS):
        x, y = 32 + (i % 2) * 424, 86 + (i // 2) * 82
        parts.append(f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="10.5" '
                     f'letter-spacing="1" fill="{t["faint"]}">{escape(group)}</text>')
        parts.append(chips(x, y + 8, items, t))
    label = "技能与工具：" + "；".join(f"{group}: {', '.join(items)}" for group, items in SKILL_GROUPS)
    return svg(w, h, "\n".join(parts), label)


def footer(t):
    w, h = 880, 140
    body = f'''{card(w, h, t, 14)}
<text x="440" y="56" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="700" fill="{t["text"]}">{escape(FOOTER_TITLE)}</text>
<rect x="412" y="68" width="56" height="3" rx="1.5" fill="url(#g)"/>
<text x="440" y="94" text-anchor="middle" font-family="{FONT}" font-size="13" fill="{t["muted"]}">{escape(FOOTER_SUB)}</text>
<text x="440" y="120" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{t["accent"]}">{escape(FOOTER_META)}</text>
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["accent"]}"/><stop offset="1" stop-color="{t["accent2"]}"/></linearGradient></defs>'''
    return svg(w, h, body, f"{FOOTER_TITLE}。{FOOTER_SUB}。{FOOTER_META}")


CARDS = {"hero": hero, "about": about, "skills": skills, "footer": footer}


def main():
    out_dir = Path(__file__).resolve().parent.parent / "assets"
    out_dir.mkdir(exist_ok=True)
    for name, build in CARDS.items():
        for theme, palette in THEMES.items():
            path = out_dir / f"{name}-{theme}.svg"
            path.write_text(build(palette), encoding="utf-8")
            print(f"wrote {path.relative_to(out_dir.parent)}")


if __name__ == "__main__":
    main()