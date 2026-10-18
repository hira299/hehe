"""Generate every animated SVG for the profile README (dark theme only).

    python3 assets/build.py

Edit the content blocks below and re-run. Everything is plain SVG with CSS /
SMIL animation, so it plays inside a GitHub <img> tag: no GIFs, no scripts.
Set PREVIEW=1 to render static frames (for checking layout with a rasteriser).
"""
import os
from html import escape
from pathlib import Path

OUT = Path(__file__).parent
PREVIEW = bool(os.environ.get("PREVIEW"))

# bg is GitHub's dark canvas; every image paints it so it also reads on light theme.
BG, SURFACE, HAIR = "#0D1117", "#151116", "#2D2328"
FG, MUTED = "#EFE7E9", "#9B9094"
BLOOD, BLOODHI = "#8E1F30", "#C1304A"      # oxblood, oxblood highlight
PINK, ROSE = "#F4B8C8", "#E98AA5"          # light pink accents

SANS = "'Inter','Segoe UI','Helvetica Neue',-apple-system,BlinkMacSystemFont,Roboto,Arial,sans-serif"
MONO = "ui-monospace,'SFMono-Regular','JetBrains Mono',Menlo,Consolas,monospace"

# ---------------------------------------------------------------- content

TYPED = [
    "Autonomous LLM pipelines that keep working.",
    "1,500+ defects documented. 0 schema drift.",
    "The model proposes. The verifier decides.",
]

GATES = ["QUEUED", "ENRICHED", "TRANSLATED", "VERIFIED"]

STATS = [
    ("28K+", "AI records enriched", "status-gated LLM pipeline"),
    ("1,500+", "defects documented", "across 4 client contracts"),
    ("34%", "monthly AWS cost cut", "Lambda, RDS, API Gateway"),
    ("83.81%", "SMT-verified repair", "Sentinel-Mesh, 88/105"),
]

# (slug, tag, title, metric, metric label, description, motif)
PROJECTS = [
    ("techpotion", "Production system", "AI Enrichment Pipeline", "28K+", "live records processed",
     "Four status-gated LLM stages with 9-language translation. Zero schema drift in production.", "pipeline"),
    ("compliance", "Independent build", "Cloud Compliance Engine", "3", "AWS services audited",
     "Autonomous multi-account audit across S3, IAM and GuardDuty, grounded with Corrective RAG.", "cloud"),
    ("pharma", "B2B SaaS QA", "PharmaConnect Lead QA", "110+", "defects documented",
     "20 end-to-end journeys across 15 modules, with API-level evidence and 75 closed fixes.", "matrix"),
    ("sentinel", "Research", "Sentinel-Mesh", "83.81%", "of 105 cases remediated",
     "An LLM proposes Terraform patches and a Z3 SMT verifier decides. No regressions observed.", "verify"),
]

PILLARS = [
    ("AI automation", "& agents", "Stateful agents, tool use, validation, retries, human escalation.", "pipeline"),
    ("LLM pipelines", "& RAG", "Multi-stage pipelines, Corrective RAG, LangGraph, structured output.", "verify"),
    ("Backend", "& cloud", "Python, FastAPI, PostgreSQL, n8n, AWS, Terraform, Docker.", "stack"),
    ("QA &", "reliability", "Multi-tenant isolation, RBAC, API and business-logic testing.", "matrix"),
]

# (label, role, where, line)  newest first
JOURNEY = [
    ("SEP 2026 –", "Quality Assurance Lead", "TechPotion.ai",
     "Four concurrent client contracts, 1,500+ defects documented."),
    ("2025 – 26", "Backend & Automation Engineer", "TechPotion.ai",
     "28K+ record AI pipelines, ETL automation, AWS cost optimization."),
    ("2024", "QA Intern", "Sadiq.ai",
     "Automated and manual testing across Flutter web and mobile apps."),
    ("RESEARCH", "Lead author, Sentinel-Mesh", "IEEE Access reviewer",
     "Formally verified AI infrastructure repair. Five verified peer reviews."),
    ("DEGREE", "B.S. Cybersecurity", "SSUET",
     "Sir Syed University of Engineering & Technology."),
]

SECTIONS = [
    ("flagship", "01", "Flagship work"),
    ("research", "02", "Research"),
    ("expertise", "03", "What I do"),
    ("experience", "04", "Where I've worked"),
    ("builds", "05", "Independent builds"),
    ("activity", "06", "On GitHub"),
    ("talk", "07", "Let's talk"),
]

BUTTONS = [("portfolio", "Portfolio"), ("resume", "Résumé"), ("email", "Email"),
           ("linkedin", "LinkedIn"), ("hire", "Hire me")]

BARS = [("Sentinel-Mesh (LLM + Z3 counterexample feedback)", 83.81, "88/105", PINK),
        ("Same LLM, no counterexample feedback", 64.76, "68/105", BLOODHI),
        ("Checkov baseline", 35.24, "37/105", "#4A3A40")]

# ---------------------------------------------------------------- helpers


def wrap(text, width):
    lines, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur] if cur else lines


def svg(w, h, label, css, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(label)}"><style>{css}</style>'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>\n')


def base_css():
    up = ".up{opacity:1}" if PREVIEW else ".up{opacity:0;animation:up .8s cubic-bezier(.2,.7,.2,1) forwards}"
    return (f".sans{{font-family:{SANS}}}.mono{{font-family:{MONO}}}"
            f".fg{{fill:{FG}}}.muted{{fill:{MUTED}}}.pink{{fill:{PINK}}}.rose{{fill:{ROSE}}}.hi{{fill:{BLOODHI}}}"
            "@keyframes up{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}" + up +
            "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}"
            ".pulse{animation:pulse 2.4s ease-in-out infinite}"
            "@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}"
            ".float{animation:float 4s ease-in-out infinite}"
            "@media (prefers-reduced-motion:reduce){.up{opacity:1;animation:none}.pulse,.float{animation:none}}")


def trace(w, h, rx, color=PINK, dur=7, sw=1.5, frac=.12):
    """A short bright dash that circles a rounded rectangle forever."""
    return (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" pathLength="1" stroke-dasharray="{frac} {1-frac}">'
            f'<animate attributeName="stroke-dashoffset" from="0" to="-1" dur="{dur}s" repeatCount="indefinite"/></rect>')


def icon(kind, x, y, s=1.0):
    """Animated line-art motifs in a 48x48 box."""
    g = f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke-linecap="round" stroke-linejoin="round">'
    if kind == "pipeline":
        path = "M6 34 L18 14 L30 34 L42 14"
        g += f'<path d="{path}" stroke="{HAIR}" stroke-width="1.6"/>'
        for px, py in [(6, 34), (18, 14), (30, 34), (42, 14)]:
            g += f'<circle cx="{px}" cy="{py}" r="4.5" stroke="{FG}" stroke-width="1.6" fill="{SURFACE}"/>'
        g += (f'<circle r="3" fill="{PINK}" stroke="none"><animateMotion dur="3s" repeatCount="indefinite" path="{path}"/></circle>')
    elif kind == "cloud":
        g += (f'<path d="M14 36 H35 A8 8 0 0 0 36 20 A12 12 0 0 0 14 21 A7.5 7.5 0 0 0 14 36 Z" stroke="{FG}" stroke-width="1.6"/>'
              f'<line x1="12" x2="38" y1="14" y2="14" stroke="{PINK}" stroke-width="2">'
              '<animate attributeName="y1" values="14;40;14" dur="3.4s" repeatCount="indefinite"/>'
              '<animate attributeName="y2" values="14;40;14" dur="3.4s" repeatCount="indefinite"/>'
              '<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.85;1" dur="3.4s" repeatCount="indefinite"/></line>')
    elif kind == "matrix":
        for i in range(9):
            cx, cy = 5 + (i % 3) * 14, 5 + (i // 3) * 14
            bad = i == 5
            col = BLOODHI if bad else FG
            g += (f'<rect x="{cx}" y="{cy}" width="11" height="11" rx="3" stroke="{col}" stroke-width="1.6" '
                  f'{"fill=" + chr(34) + BLOODHI + chr(34) if bad else ""} class="pulse" '
                  f'style="animation-delay:{i*.25:.2f}s;animation-duration:{1.6 if bad else 3.2}s"/>')
    elif kind == "verify":
        circ = "M38 24 A14 14 0 1 1 10 24 A14 14 0 1 1 38 24"
        g += (f'<circle cx="24" cy="24" r="14" stroke="{HAIR}" stroke-width="1.8"/>'
              f'<path d="M16 25 l6 6 l11 -12" stroke="{PINK}" stroke-width="2.2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">'
              '<animate attributeName="stroke-dashoffset" values="1;0;0;1" keyTimes="0;.3;.8;1" dur="3.6s" repeatCount="indefinite"/></path>'
              f'<circle r="3" fill="{BLOODHI}" stroke="none"><animateMotion dur="3.6s" repeatCount="indefinite" path="{circ}"/></circle>')
    elif kind == "stack":
        for i in range(3):
            g += (f'<rect x="8" y="{7+i*13}" width="32" height="10" rx="4" stroke="{PINK if i == 0 else FG}" stroke-width="1.6">'
                  f'<animate attributeName="x" values="8;12;8" dur="3s" begin="{i*.4}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines=".4 0 .6 1;.4 0 .6 1"/></rect>')
    return g + "</g>"


# ---------------------------------------------------------------- components


def hero():
    w, h = 880, 300
    cycle = 4.0 * len(TYPED)
    share = 100 / len(TYPED)
    css = [base_css(), ".name{font-size:54px;font-weight:700;letter-spacing:-.02em}.lead{font-size:22px;font-weight:600}"
           ".pill{font-size:12px;letter-spacing:.08em}.typed{font-size:15px}.gate{font-size:11px;letter-spacing:.08em}"
           f"@keyframes gate{{0%,3%{{stroke:{HAIR}}}6%,16%{{stroke:{PINK}}}24%,100%{{stroke:{HAIR}}}}}",
           "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}"]
    typed = ""
    for i, line in enumerate(TYPED):
        full = len(line) * 9.0
        delay = i * cycle / len(TYPED) + 1.2
        frames = (f"0%{{width:0}}{share*.45:.2f}%{{width:{full:.0f}px}}{share*.92:.2f}%{{width:{full:.0f}px}}"
                  f"{share:.2f}%{{width:0}}100%{{width:0}}")
        cur = (f"0%{{transform:translateX(0);opacity:1}}{share*.45:.2f}%{{transform:translateX({full:.0f}px);opacity:1}}"
               f"{share*.92:.2f}%{{transform:translateX({full:.0f}px);opacity:1}}{share:.2f}%{{transform:translateX(0);opacity:1}}"
               f"{share+.01:.2f}%{{opacity:0}}100%{{opacity:0}}")
        # static fallback for preview: show the first line fully
        wid = f"{full:.0f}" if (PREVIEW and i == 0) else "0"
        css.append(f"@keyframes t{i}{{{frames}}}@keyframes k{i}{{{cur}}}"
                   f".c{i}{{width:{wid}px;animation:t{i} {cycle}s steps({len(line)},end) {delay}s infinite}}"
                   f".k{i}{{opacity:0;animation:k{i} {cycle}s steps({len(line)},end) {delay}s infinite}}")
        typed += (f'<clipPath id="k{i}"><rect class="c{i}" x="52" y="218" height="30"/></clipPath>'
                  f'<text x="52" y="240" class="mono typed fg" clip-path="url(#k{i})">{escape(line)}</text>'
                  f'<rect class="k{i}" x="52" y="226" width="8" height="16" fill="{PINK}"/>')
    if PREVIEW:
        css.append(".k0{opacity:1}")
    # pipeline motif (right)
    gx, gw, gh = 660, 170, 38
    ys = [44, 104, 164, 224]
    dot_path = f"M{gx+gw/2:.0f} {ys[0]+gh/2:.0f} V{ys[-1]+gh/2:.0f}"
    motif = (f'<line x1="{gx+gw/2:.0f}" y1="{ys[0]+gh/2:.0f}" x2="{gx+gw/2:.0f}" y2="{ys[-1]+gh/2:.0f}" stroke="{HAIR}" stroke-width="2" stroke-dasharray="3 5"/>')
    for i, (y, name) in enumerate(zip(ys, GATES)):
        last = i == len(GATES) - 1
        motif += (f'<rect x="{gx}" y="{y}" width="{gw}" height="{gh}" rx="10" fill="{SURFACE}" stroke="{HAIR}" stroke-width="1.5" '
                  f'style="animation:gate 6s linear {i*2-.4:.1f}s infinite"/>'
                  f'<circle cx="{gx+20}" cy="{y+gh/2:.0f}" r="4" fill="{BLOODHI if not last else PINK}"/>'
                  f'<text x="{gx+36}" y="{y+gh/2+4:.0f}" class="mono gate muted">{name}</text>')
    motif += (f'<circle r="5" fill="{PINK}"><animateMotion dur="6s" repeatCount="indefinite" path="{dot_path}" calcMode="linear"/></circle>'
              f'<circle r="11" fill="none" stroke="{PINK}" opacity=".35"><animateMotion dur="6s" repeatCount="indefinite" path="{dot_path}" calcMode="linear"/></circle>')
    body = (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="20" fill="{SURFACE}" stroke="{HAIR}"/>' + trace(w, h, 20, PINK, 12, 1.5, .08) + motif +
            f'<g class="up" style="animation-delay:.1s"><rect x="32" y="30" width="238" height="30" rx="15" fill="{BG}" stroke="{BLOOD}"/>'
            f'<circle cx="50" cy="45" r="4.5" class="pink pulse"/><text x="64" y="49.5" class="sans pill fg">AVAILABLE FOR ENGAGEMENTS</text></g>'
            f'<text x="30" y="128" class="sans name fg up" style="animation-delay:.3s">Hira Ahmed<tspan class="pink">.</tspan></text>'
            f'<text x="32" y="166" class="sans lead pink up" style="animation-delay:.55s">AI Engineer &amp; Systems QA Lead</text>'
            f'<line x1="32" y1="192" x2="560" y2="192" stroke="{HAIR}"/>'
            f'<line x1="32" y1="192" x2="560" y2="192" stroke="{BLOODHI}" stroke-width="2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="{0 if PREVIEW else 1}">'
            '<animate attributeName="stroke-dashoffset" from="1" to="0" begin=".8s" dur="1.4s" fill="freeze"/></line>'
            f'<text x="32" y="240" class="mono typed pink">›</text>' + typed)
    return svg(w, h, "Hira Ahmed. AI Engineer and Systems QA Lead.", "".join(css), body)


def stats():
    w, h, gap = 880, 132, 12
    tw = (w - gap * (len(STATS) - 1)) / len(STATS)
    css = base_css() + ".num{font-size:34px;font-weight:700;letter-spacing:-.02em}.lbl{font-size:13.5px;font-weight:600}.sub{font-size:12px}"
    body = ""
    for i, (num, label, sub) in enumerate(STATS):
        x, d = i * (tw + gap), i * .15
        bw = tw - 40
        body += (f'<g class="up" style="animation-delay:{d:.2f}s">'
                 f'<rect x="{x+.5:.1f}" y=".5" width="{tw-1:.1f}" height="{h-1}" rx="14" fill="{SURFACE}" stroke="{HAIR}"/>'
                 f'<text x="{x+20:.1f}" y="54" class="sans num pink">{escape(num)}</text>'
                 f'<text x="{x+20:.1f}" y="78" class="sans lbl fg">{escape(label)}</text>'
                 f'<text x="{x+20:.1f}" y="97" class="sans sub muted">{escape(sub)}</text>'
                 f'<rect x="{x+20:.1f}" y="112" width="{bw:.1f}" height="3" rx="1.5" fill="{HAIR}"/>'
                 f'<rect x="{x+20:.1f}" y="112" width="{0 if not PREVIEW else bw:.1f}" height="3" rx="1.5" fill="{BLOODHI}">'
                 f'<animate attributeName="width" from="0" to="{bw:.1f}" begin="{d+.4:.2f}s" dur="1.2s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .7 .2 1"/></rect>'
                 f'<rect x="{x+20:.1f}" y="112" width="26" height="3" rx="1.5" fill="{PINK}" opacity=".9">'
                 f'<animate attributeName="x" values="{x+20:.1f};{x+20+bw-26:.1f};{x+20:.1f}" dur="4.5s" begin="{d+1.6:.2f}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines=".5 0 .5 1;.5 0 .5 1"/></rect></g>')
    return svg(w, h, " · ".join(f"{n} {l}" for n, l, _ in STATS), css, body)


def section(num, title):
    w, h = 880, 60
    css = base_css() + ".n{font-size:13px;letter-spacing:.1em}.t{font-size:24px;font-weight:700;letter-spacing:-.01em}"
    tx = 52
    lx = tx + len(title) * 13 + 24
    body = (f'<text x="0" y="38" class="mono n hi">{num}</text>'
            f'<text x="{tx}" y="40" class="sans t fg">{escape(title)}</text>'
            f'<line x1="{lx:.0f}" y1="32" x2="{w}" y2="32" stroke="{HAIR}" pathLength="1" stroke-dasharray="1" stroke-dashoffset="{0 if PREVIEW else 1}">'
            '<animate attributeName="stroke-dashoffset" from="1" to="0" dur="1.2s" fill="freeze"/></line>'
            f'<line x1="{lx:.0f}" y1="32" x2="{w}" y2="32" stroke="{PINK}" stroke-width="2" stroke-linecap="round" pathLength="1" stroke-dasharray=".05 .95">'
            '<animate attributeName="stroke-dashoffset" from="0.05" to="-1" dur="5s" repeatCount="indefinite"/></line>')
    return svg(w, h, f"{num} {title}", css, body)


def card(tag, title, metric, mlabel, desc, motif):
    w, h = 432, 278
    css = base_css() + (".tag{font-size:11px;letter-spacing:.08em}.title{font-size:19px;font-weight:700}"
                        ".met{font-size:44px;font-weight:700;letter-spacing:-.02em}.ml{font-size:13px}"
                        ".desc{font-size:13.5px}.more{font-size:12.5px;font-weight:600}")
    tag_w = len(tag) * 7.6 + 26
    body = (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="{SURFACE}" stroke="{HAIR}"/>' + trace(w, h, 16) +
            f'<g class="float">{icon(motif, 24, 20)}</g>'
            f'<rect x="{w-24-tag_w:.0f}" y="24" width="{tag_w:.0f}" height="24" rx="12" fill="none" stroke="{BLOOD}"/>'
            f'<text x="{w-24-tag_w/2:.0f}" y="40" text-anchor="middle" class="sans tag muted">{escape(tag.upper())}</text>'
            f'<text x="24" y="100" class="sans title fg">{escape(title)}</text>'
            f'<text x="24" y="148" class="sans met pink">{escape(metric)}</text>'
            f'<text x="24" y="170" class="sans ml muted">{escape(mlabel)}</text>')
    for i, line in enumerate(wrap(desc, 54)[:3]):
        body += f'<text x="24" y="{198 + i*20}" class="sans desc muted">{escape(line)}</text>'
    body += (f'<circle cx="30" cy="{h-24}" r="3.5" class="pink pulse"/>'
             f'<text x="{w-24}" y="{h-20}" text-anchor="end" class="sans more pink">Case study →'
             f'<animate attributeName="x" values="{w-24};{w-20};{w-24}" dur="1.8s" repeatCount="indefinite"/></text>')
    return svg(w, h, f"{title}. {metric} {mlabel}. {desc}", css, body)


def pillars():
    w, h, gap = 880, 214, 14
    tw = (w - gap * (len(PILLARS) - 1)) / len(PILLARS)
    css = base_css() + ".kt{font-size:17px;font-weight:700}.kd{font-size:13px}"
    body = ""
    for i, (a, b, desc, motif) in enumerate(PILLARS):
        x = i * (tw + gap)
        body += (f'<g class="up" style="animation-delay:{i*.15:.2f}s">'
                 f'<rect x="{x+.5:.1f}" y=".5" width="{tw-1:.1f}" height="{h-1}" rx="16" fill="{SURFACE}" stroke="{HAIR}"/>'
                 f'<g class="float" style="animation-delay:{i*.6:.1f}s">{icon(motif, x+20, 20, .9)}</g>'
                 f'<text x="{x+20:.1f}" y="104" class="sans kt fg">{escape(a)}</text>'
                 f'<text x="{x+20:.1f}" y="126" class="sans kt pink">{escape(b)}</text>')
        for j, line in enumerate(wrap(desc, 27)[:3]):
            body += f'<text x="{x+20:.1f}" y="{152 + j*18}" class="sans kd muted">{escape(line)}</text>'
        body += "</g>"
    return svg(w, h, " · ".join(f"{a} {b}" for a, b, *_ in PILLARS), css, body)


def journey():
    row, top = 74, 18
    w, h = 880, top + row * len(JOURNEY)
    lx = 150
    css = base_css() + ".jy{font-size:12px;letter-spacing:.08em;font-weight:700}.jr{font-size:17px;font-weight:700}.jw{font-size:15px;font-weight:600}.jd{font-size:13.5px}"
    y0, y1 = top + 8, top + (len(JOURNEY) - 1) * row + 8
    body = (f'<line x1="{lx}" y1="{y0}" x2="{lx}" y2="{y1}" stroke="{HAIR}" stroke-width="2"/>'
            f'<line x1="{lx}" y1="{y0}" x2="{lx}" y2="{y1}" stroke="{BLOODHI}" stroke-width="2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="{0 if PREVIEW else 1}">'
            '<animate attributeName="stroke-dashoffset" from="1" to="0" dur="2.6s" fill="freeze"/></line>'
            f'<line x1="{lx}" y1="{y0}" x2="{lx}" y2="{y1}" stroke="{PINK}" stroke-width="3" stroke-linecap="round" pathLength="1" stroke-dasharray=".06 .94">'
            '<animate attributeName="stroke-dashoffset" from=".06" to="-1" dur="5s" begin="2.6s" repeatCount="indefinite"/></line>')
    for i, (when, role, where, desc) in enumerate(JOURNEY):
        y = top + i * row
        now = i == 0
        body += (f'<g class="up" style="animation-delay:{i*.3:.2f}s">'
                 f'<text x="{lx-26}" y="{y+13}" text-anchor="end" class="sans jy {"pink" if now else "muted"}">{escape(when)}</text>'
                 f'<circle cx="{lx}" cy="{y+8}" r="7" fill="{PINK if now else SURFACE}" stroke="{PINK if now else BLOODHI}" stroke-width="2"/>'
                 f'<text x="{lx+28}" y="{y+14}" class="sans jr fg">{escape(role)}<tspan class="muted" style="font-weight:400">  ·  </tspan><tspan class="jw rose">{escape(where)}</tspan></text>'
                 f'<text x="{lx+28}" y="{y+38}" class="sans jd muted">{escape(desc)}</text></g>')
    body += (f'<circle cx="{lx}" cy="{y0}" r="7" fill="none" stroke="{PINK}"><animate attributeName="r" values="7;20" dur="2.4s" repeatCount="indefinite"/>'
             '<animate attributeName="opacity" values=".8;0" dur="2.4s" repeatCount="indefinite"/></circle>')
    return svg(w, h, " · ".join(f"{a}: {r}, {wh}" for a, r, wh, _ in JOURNEY), css, body)


def bars():
    w, h = 880, 236
    css = base_css() + ".bt{font-size:17px;font-weight:700}.bl{font-size:14px}.bv{font-size:15px;font-weight:700}.bn{font-size:12px}"
    bx, bwid = 380, 340
    body = (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="{SURFACE}" stroke="{HAIR}"/>'
            f'<text x="24" y="38" class="sans bt fg">CloudFix-Bench: remediation rate on 105 AWS Terraform cases</text>')
    for i, (label, v, frac, col) in enumerate(BARS):
        y = 70 + i * 46
        fill = bwid * v / 100
        body += (f'<text x="24" y="{y+14}" class="sans bl muted">{escape(label)}</text>'
                 f'<rect x="{bx}" y="{y}" width="{bwid}" height="20" rx="10" fill="{BG}" stroke="{HAIR}"/>'
                 f'<rect x="{bx}" y="{y}" width="{fill if PREVIEW else 0:.0f}" height="20" rx="10" fill="{col}">'
                 f'<animate attributeName="width" from="0" to="{fill:.0f}" begin="{.3+i*.25:.2f}s" dur="1.4s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .7 .2 1"/></rect>'
                 f'<text x="{bx+bwid+14}" y="{y+15}" class="sans bv fg">{v}%</text>'
                 f'<text x="{bx+bwid+84}" y="{y+15}" class="mono bn muted">{frac}</text>')
    body += (f'<text x="24" y="{h-20}" class="sans bn muted">95% Wilson interval 75.59% to 89.64%. Guarantees hold within the modeled Cloud Perimeter Model.</text>')
    return svg(w, h, "CloudFix-Bench results: 83.81% vs 64.76% vs 35.24%", css, body)


def cta():
    w, h = 880, 200
    css = base_css() + ".big{font-size:30px;font-weight:700;letter-spacing:-.02em}.sub{font-size:16px}"
    body = (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="20" fill="{SURFACE}" stroke="{HAIR}"/>' + trace(w, h, 20, PINK, 8, 1.5, .2) +
            f'<text x="{w/2:.0f}" y="82" text-anchor="middle" class="sans big fg up">Need resilient AI pipelines or high-assurance QA?</text>'
            f'<text x="{w/2:.0f}" y="116" text-anchor="middle" class="sans sub muted up" style="animation-delay:.25s">n8n workflows, LLM extraction, multi-tenant B2B SaaS testing. Remote.</text>'
            f'<g class="up" style="animation-delay:.5s"><circle cx="{w/2-100:.0f}" cy="154" r="4.5" class="pink pulse"/>'
            f'<text x="{w/2-88:.0f}" y="158.5" class="mono" fill="{PINK}" style="font-size:14px">hira229922@gmail.com</text></g>')
    return svg(w, h, "Need resilient AI pipelines or high-assurance QA? hira229922@gmail.com", css, body)


def button(label):
    w, h = 150, 46
    css = base_css() + ".b{font-size:14.5px;font-weight:600}"
    body = (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="23" fill="{SURFACE}" stroke="{BLOOD}" stroke-width="1.3"/>'
            f'<text x="{w/2-10:.0f}" y="28.5" text-anchor="middle" class="sans b fg">{escape(label)}</text>'
            f'<text x="{w-36}" y="28.5" class="sans b pink">→<animate attributeName="x" values="{w-38};{w-32};{w-38}" dur="1.8s" repeatCount="indefinite"/></text>')
    return svg(w, h, label, css, body)


def main():
    for d in ("cards", "sections", "buttons"):
        (OUT / d).mkdir(exist_ok=True)
    (OUT / "hero.svg").write_text(hero())
    (OUT / "stats.svg").write_text(stats())
    (OUT / "pillars.svg").write_text(pillars())
    (OUT / "journey.svg").write_text(journey())
    (OUT / "research.svg").write_text(bars())
    (OUT / "cta.svg").write_text(cta())
    for slug, *rest in PROJECTS:
        (OUT / "cards" / f"{slug}.svg").write_text(card(*rest))
    for slug, num, title in SECTIONS:
        (OUT / "sections" / f"{slug}.svg").write_text(section(num, title))
    for slug, label in BUTTONS:
        (OUT / "buttons" / f"{slug}.svg").write_text(button(label))


if __name__ == "__main__":
    main()
