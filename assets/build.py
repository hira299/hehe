"""Generate every animated SVG for the profile README (dark theme, flowing style).

    python3 assets/build.py

Edit the content blocks and re-run. Pure SVG + CSS/SMIL animation: plays inside a
GitHub <img>, no GIFs, no scripts. Images paint GitHub's dark canvas colour so they
melt into the page; there are no boxed cards, only soft shapes and flowing curves.
"""
import math
from html import escape
from pathlib import Path

OUT = Path(__file__).parent

BG = "#0D1117"                       # GitHub dark canvas
SURFACE = "#151A23"                  # soft fill (used at partial opacity, never outlined)
HAIR = "#2A2E3B"
FG, MUTED = "#E9E6EC", "#8F93A3"
PLUM, PINK, ROSE, WINE = "#9C5B78", "#E6B8CB", "#D69DB5", "#4A2B3C"

SANS = "'Inter','Segoe UI','Helvetica Neue',-apple-system,BlinkMacSystemFont,Roboto,Arial,sans-serif"
MONO = "ui-monospace,'SFMono-Regular','JetBrains Mono',Menlo,Consolas,monospace"
W = 880

# ---------------------------------------------------------------- content

LINES = ["Autonomous LLM pipelines that keep working.",
         "1,500+ defects documented. 0 schema drift.",
         "The model proposes. The verifier decides."]
GATES = ["QUEUED", "ENRICHED", "TRANSLATED", "VERIFIED"]

STATS = [("28K+", "AI records enriched", "status-gated LLM pipeline"),
         ("1,500+", "defects documented", "across 4 client contracts"),
         ("34%", "monthly AWS cost cut", "Lambda, RDS, API Gateway"),
         ("83.81%", "SMT-verified repair", "Sentinel-Mesh, 88 of 105")]

# (slug, tag, title, description, metric, metric label)
PROJECTS = [
    ("techpotion", "Production system", "AI Enrichment Pipeline",
     "Four status-gated LLM stages with 9-language translation. Zero schema drift in production.",
     "28K+", "live records processed"),
    ("compliance", "Independent build", "Cloud Compliance Engine",
     "Autonomous multi-account AWS audit across S3, IAM and GuardDuty, grounded with Corrective RAG.",
     "3", "AWS services audited"),
    ("pharma", "B2B SaaS QA", "PharmaConnect Lead QA",
     "20 end-to-end journeys across 15 modules, with API-level evidence and 75 closed fixes.",
     "110+", "defects documented"),
    ("sentinel", "Research", "Sentinel-Mesh",
     "An LLM proposes Terraform patches and a Z3 SMT verifier decides. No regressions observed.",
     "83.81%", "of 105 cases remediated"),
]

PILLARS = [("AI automation", "& agents", "Stateful agents, tool use, validation, retries, human escalation.", "pipeline"),
           ("LLM pipelines", "& RAG", "Multi-stage pipelines, Corrective RAG, LangGraph, structured output.", "verify"),
           ("Backend", "& cloud", "Python, FastAPI, PostgreSQL, n8n, AWS, Terraform, Docker.", "stack"),
           ("QA &", "reliability", "Multi-tenant isolation, RBAC, API and business-logic testing.", "matrix")]

JOURNEY = [("SEP 2026 – NOW", "Quality Assurance Lead", "TechPotion.ai",
            "Four concurrent client contracts, 1,500+ defects documented."),
           ("2025 – 2026", "Backend & Automation Engineer", "TechPotion.ai",
            "28K+ record AI pipelines, ETL automation, AWS cost optimization."),
           ("2024", "QA Intern", "Sadiq.ai",
            "Automated and manual testing across Flutter web and mobile apps."),
           ("RESEARCH", "Lead author, Sentinel-Mesh", "IEEE Access reviewer",
            "Formally verified AI infrastructure repair. Five verified peer reviews."),
           ("DEGREE", "B.S. Cybersecurity", "SSUET",
            "Sir Syed University of Engineering & Technology.")]

SECTIONS = [("flagship", "Flagship work"), ("research", "Research"), ("expertise", "What I do"),
            ("experience", "Where I've worked"), ("builds", "Independent builds"), ("talk", "Let's talk")]

BUTTONS = [("portfolio", "Portfolio"), ("resume", "Résumé"), ("email", "Email"),
           ("linkedin", "LinkedIn"), ("hire", "Hire me")]

BARS = [("Sentinel-Mesh (LLM + Z3 counterexample feedback)", 83.81, "88/105", PINK),
        ("Same LLM, no counterexample feedback", 64.76, "68/105", PLUM),
        ("Checkov baseline", 35.24, "37/105", WINE)]

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


def css_base():
    return (f".sans{{font-family:{SANS}}}.mono{{font-family:{MONO}}}"
            f".fg{{fill:{FG}}}.muted{{fill:{MUTED}}}.pink{{fill:{PINK}}}.rose{{fill:{ROSE}}}"
            "@keyframes up{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}"
            ".up{opacity:0;animation:up .9s cubic-bezier(.2,.7,.2,1) forwards}"
            "@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}"
            ".float{animation:float 5s ease-in-out infinite}"
            "@media (prefers-reduced-motion:reduce){.up{opacity:1;animation:none}.float{animation:none}}")


def svg(w, h, label, css, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(label)}"><style>{css}</style><defs>{defs}</defs>'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>{body}</svg>\n')


def wave_d(y, amp, period=440, total=1760, x0=0):
    """Open sine-like path made of quadratic segments (period must divide the shift used to loop it)."""
    d = f"M{x0} {y} Q{x0 + period/4:.1f} {y - amp} {x0 + period/2:.1f} {y}"
    x = x0 + period / 2
    while x < x0 + total:
        x += period / 2
        d += f" T{x:.1f} {y}"
    return d


def wave_fill(y, amp, h, fill, op, dur, begin, period=440):
    d = wave_d(y, amp, period) + f" V{h} H0 Z"
    return (f'<g><path d="{d}" fill="{fill}" opacity="{op}">'
            f'<animateTransform attributeName="transform" type="translate" from="0 0" to="-{period*2} 0" '
            f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></path></g>')


def river_d(n, rowh, x0=60, x1=100):
    """Vertical flowing curve; vertical tangent at every row boundary so rows join seamlessly."""
    d = f"M{x0} 0"
    for r in range(n):
        y = r * rowh
        d += (f" C{x0} {y+.25*rowh:.1f} {x1} {y+.3*rowh:.1f} {x1} {y+.5*rowh:.1f}"
              f" S{x0} {y+.75*rowh:.1f} {x0} {y+rowh:.1f}")
    return d


def blob_variants(cx, cy, r):
    """Same-structure closed blobs so SMIL can morph between them."""
    out = []
    for radii in [(1.0, .92, 1.05, .95), (.93, 1.06, .94, 1.04), (1.05, .96, .92, 1.03), (1.0, .92, 1.05, .95)]:
        pts = []
        for k, ri in enumerate(radii):
            th = k * math.pi / 2
            pts.append((cx + r * ri * math.cos(th), cy + r * ri * math.sin(th), th, r * ri))
        d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
        for k in range(4):
            a, b = pts[k], pts[(k + 1) % 4]
            ta = (-math.sin(a[2]), math.cos(a[2]))
            tb = (-math.sin(b[2]), math.cos(b[2]))
            ka, kb = .5523 * a[3], .5523 * b[3]
            d += (f" C{a[0]+ta[0]*ka:.1f} {a[1]+ta[1]*ka:.1f} {b[0]-tb[0]*kb:.1f} {b[1]-tb[1]*kb:.1f} {b[0]:.1f} {b[1]:.1f}")
        out.append(d + " Z")
    return out


def icon(kind, x, y, s=1.0):
    g = f'<g transform="translate({x:.1f} {y:.1f}) scale({s})" fill="none" stroke-linecap="round" stroke-linejoin="round">'
    if kind == "pipeline":
        path = "M6 34 L18 14 L30 34 L42 14"
        g += f'<path d="{path}" stroke="{HAIR}" stroke-width="1.6"/>'
        for px, py in [(6, 34), (18, 14), (30, 34), (42, 14)]:
            g += f'<circle cx="{px}" cy="{py}" r="4.5" stroke="{FG}" stroke-width="1.6" fill="{BG}"/>'
        g += f'<circle r="3" fill="{PINK}" stroke="none"><animateMotion dur="3s" repeatCount="indefinite" path="{path}"/></circle>'
    elif kind == "verify":
        circ = "M38 24 A14 14 0 1 1 10 24 A14 14 0 1 1 38 24"
        g += (f'<circle cx="24" cy="24" r="14" stroke="{HAIR}" stroke-width="1.8"/>'
              f'<path d="M16 25 l6 6 l11 -12" stroke="{PINK}" stroke-width="2.2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1">'
              '<animate attributeName="stroke-dashoffset" values="1;0;0;1" keyTimes="0;.3;.8;1" dur="3.6s" repeatCount="indefinite"/></path>'
              f'<circle r="2.6" fill="{ROSE}" stroke="none"><animateMotion dur="3.6s" repeatCount="indefinite" path="{circ}"/></circle>')
    elif kind == "stack":
        for i in range(3):
            g += (f'<rect x="8" y="{7+i*13}" width="32" height="10" rx="5" stroke="{PINK if i == 0 else FG}" stroke-width="1.6">'
                  f'<animate attributeName="x" values="8;12;8" dur="3.4s" begin="{i*.45}s" repeatCount="indefinite" calcMode="spline" '
                  'keyTimes="0;.5;1" keySplines=".4 0 .6 1;.4 0 .6 1"/></rect>')
    elif kind == "matrix":
        for i in range(9):
            cx, cy = 5 + (i % 3) * 14, 5 + (i // 3) * 14
            bad = i == 5
            g += (f'<rect x="{cx}" y="{cy}" width="11" height="11" rx="4" stroke="{PINK if bad else FG}" stroke-width="1.6" '
                  f'fill="{PINK if bad else "none"}" fill-opacity=".35">'
                  f'<animate attributeName="opacity" values="1;.35;1" dur="{2.2 if bad else 4}s" begin="{i*.3:.1f}s" repeatCount="indefinite"/></rect>')
    return g + "</g>"


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

# ---------------------------------------------------------------- components


def hero():
    H = 340
    css = [css_base(), ".name{font-size:64px;font-weight:700;letter-spacing:-.025em}.role{font-size:24px;font-weight:600}"
           ".line{font-size:18px}.meta{font-size:13px}.status{font-size:12px;letter-spacing:.1em}.gate{font-size:11px;letter-spacing:.1em}"
           "@keyframes r{0%{opacity:0;transform:translateY(8px)}5%{opacity:1;transform:none}28%{opacity:1;transform:none}"
           "33%{opacity:0;transform:translateY(-8px)}100%{opacity:0}}"]
    lines = ""
    for i, t in enumerate(LINES):
        css.append(f".r{i}{{opacity:0;animation:r 12s ease-in-out {.8+i*4:.1f}s infinite}}")
        lines += f'<text x="8" y="222" class="sans line fg r{i}">{escape(t)}</text>'
    # flowing pipeline curve on the right
    P0, C1, C2, P1 = (770, 40), (870, 80), (640, 128), (745, 172)
    C1b = (2*P1[0]-C2[0], 2*P1[1]-C2[1]); C2b = (872, 236); P2 = (752, 262)
    path = f"M{P0[0]} {P0[1]} C{C1[0]} {C1[1]} {C2[0]} {C2[1]} {P1[0]} {P1[1]} S{C2b[0]} {C2b[1]} {P2[0]} {P2[1]}"
    nodes = [bez(P0, C1, C2, P1, 0), bez(P0, C1, C2, P1, .67), bez(P1, C1b, C2b, P2, .34), P2]
    motif = f'<path d="{path}" fill="none" stroke="{HAIR}" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 8"/>'
    for (nx, ny), name in zip(nodes, GATES):
        motif += (f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="6.5" fill="{BG}" stroke="{ROSE}" stroke-width="1.6"/>'
                  f'<text x="{nx-20:.1f}" y="{ny+4:.1f}" text-anchor="end" class="mono gate muted">{name}</text>')
    motif += (f'<circle r="13" fill="{PINK}" opacity=".16"><animateMotion dur="7s" repeatCount="indefinite" path="{path}"/></circle>'
              f'<circle r="5" fill="{PINK}"><animateMotion dur="7s" repeatCount="indefinite" path="{path}"/></circle>')
    waves = (wave_fill(280, 22, H, PLUM, .08, 28, 0) + wave_fill(298, 18, H, ROSE, .07, 20, -7) + wave_fill(318, 14, H, PINK, .08, 15, -3))
    body = (waves + motif +
            f'<g class="up" style="animation-delay:.1s"><circle cx="12" cy="40" r="3.5" fill="{ROSE}"/>'
            f'<text x="26" y="44" class="sans status muted">AVAILABLE FOR ENGAGEMENTS</text></g>'
            f'<text x="4" y="124" class="sans name fg up" style="animation-delay:.3s">Hira Ahmed<tspan class="pink">.</tspan></text>'
            f'<text x="8" y="166" class="sans role pink up" style="animation-delay:.55s">AI Engineer &amp; Systems QA Lead</text>'
            + lines +
            f'<text x="8" y="256" class="sans meta muted up" style="animation-delay:.9s">Karachi, Pakistan  ·  Remote  ·  overlaps US, Canada, UK, Ireland and Germany hours</text>')
    return svg(W, H, "Hira Ahmed. AI Engineer and Systems QA Lead.", "".join(css), body)


def button(label):
    w, h = 148, 44
    css = css_base() + ".b{font-size:14.5px;font-weight:600}"
    body = (f'<rect width="{w}" height="{h}" rx="22" fill="{SURFACE}"/>'
            f'<circle cx="24" cy="{h/2}" r="3.5" fill="{ROSE}"/>'
            f'<text x="{w/2+8:.0f}" y="27.5" text-anchor="middle" class="sans b fg">{escape(label)}</text>')
    return svg(w, h, label, css, body)


def stats():
    H = 156
    css = css_base() + ".num{font-size:44px;font-weight:700;letter-spacing:-.02em}.lbl{font-size:14px;font-weight:600}.sub{font-size:12.5px}"
    col = W / len(STATS)
    body = ""
    for i, (n, l, s) in enumerate(STATS):
        x = 8 + i * col
        body += (f'<g class="up" style="animation-delay:{i*.15:.2f}s">'
                 f'<text x="{x:.0f}" y="58" class="sans num pink">{escape(n)}</text>'
                 f'<text x="{x:.0f}" y="84" class="sans lbl fg">{escape(l)}</text>'
                 f'<text x="{x:.0f}" y="104" class="sans sub muted">{escape(s)}</text></g>')
    path = "M0 134 " + "Q110 122 220 134 " + " ".join(f"T{x} 134" for x in range(440, W + 1, 220))
    body += (f'<path d="{path}" fill="none" stroke="{ROSE}" stroke-opacity=".35" stroke-width="1.6" stroke-linecap="round"/>'
             f'<circle r="3.5" fill="{PINK}"><animateMotion dur="12s" repeatCount="indefinite" path="{path}"/></circle>')
    return svg(W, H, " · ".join(f"{n} {l}" for n, l, _ in STATS), css, body)


def section(title):
    H = 64
    css = css_base() + ".t{font-size:27px;font-weight:700;letter-spacing:-.01em}"
    lx = len(title) * 15 + 30
    defs = f'<clipPath id="c"><rect x="{lx}" y="0" width="{W-lx}" height="{H}"/></clipPath>'
    body = (f'<text x="2" y="42" class="sans t fg">{escape(title)}</text>'
            f'<g clip-path="url(#c)"><path d="{wave_d(34, 5, 160, 1400, lx-160)}" fill="none" stroke="{ROSE}" stroke-opacity=".4" stroke-width="1.6" stroke-linecap="round">'
            '<animateTransform attributeName="transform" type="translate" from="0 0" to="160 0" dur="7s" repeatCount="indefinite"/></path></g>')
    return svg(W, H, title, css, body, defs)


def project(idx, tag, title, desc, metric, mlabel):
    n, rowh = len(PROJECTS), 148
    css = css_base() + (".tag{font-size:11px;letter-spacing:.1em}.title{font-size:22px;font-weight:700}.desc{font-size:14px}"
                        ".met{font-size:46px;font-weight:700;letter-spacing:-.02em}.ml{font-size:13px}.go{font-size:14px;font-weight:600}")
    path = river_d(1, rowh)
    a, b, e = idx / n, (idx + 1) / n, .002
    kt = f"0;{a:.3f};{a+e:.3f};{b-e:.3f};{b:.3f};1"
    drop = (f'<circle r="5" fill="{PINK}" opacity="0"><animateMotion dur="12s" repeatCount="indefinite" path="{path}" '
            f'calcMode="linear" keyPoints="0;0;0;1;1;1" keyTimes="{kt}"/>'
            f'<animate attributeName="opacity" dur="12s" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="{kt}"/></circle>')
    body = (f'<path d="{path}" fill="none" stroke="{HAIR}" stroke-width="2.2" stroke-linecap="round"/>' + drop +
            f'<circle cx="100" cy="{rowh/2}" r="7.5" fill="{BG}" stroke="{ROSE}" stroke-width="2"/>'
            f'<rect x="136" y="10" width="{W-138}" height="{rowh-20}" rx="30" fill="{SURFACE}" fill-opacity=".75"/>'
            f'<g class="up" style="animation-delay:{idx*.12:.2f}s">'
            f'<text x="168" y="50" class="mono tag muted">{escape(tag.upper())}</text>'
            f'<text x="168" y="80" class="sans title fg">{escape(title)}</text>')
    for i, l in enumerate(wrap(desc, 58)[:2]):
        body += f'<text x="168" y="{104+i*20}" class="sans desc muted">{escape(l)}</text>'
    body += (f'<text x="{W-34}" y="86" text-anchor="end" class="sans met pink">{escape(metric)}</text>'
             f'<text x="{W-34}" y="108" text-anchor="end" class="sans ml muted">{escape(mlabel)}</text>'
             f'<text x="{W-34}" y="44" text-anchor="end" class="sans go rose">Case study →'
             f'<animate attributeName="x" values="{W-34};{W-29};{W-34}" dur="2.2s" repeatCount="indefinite"/></text></g>')
    return svg(W, rowh, f"{title}. {metric} {mlabel}. {desc}", css, body)


def pillars():
    H, col = 262, W / 4
    css = css_base() + ".kt{font-size:18px;font-weight:700}.kd{font-size:13.5px}"
    body = ""
    for i, (a, b, d, motif) in enumerate(PILLARS):
        x = i * col
        cx, cy = x + 62, 66
        vs = blob_variants(cx, cy, 40)
        body += (f'<g class="up" style="animation-delay:{i*.15:.2f}s">'
                 f'<path d="{vs[0]}" fill="{PLUM}" fill-opacity=".16"><animate attributeName="d" values="{";".join(vs)}" '
                 f'dur="{10+i*2}s" begin="{-i*3}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.33;.66;1" '
                 'keySplines=".4 0 .6 1;.4 0 .6 1;.4 0 .6 1"/></path>'
                 f'<g class="float" style="animation-delay:{i*.7:.1f}s">{icon(motif, cx-21.6, cy-21.6, .9)}</g>'
                 f'<text x="{x+8:.0f}" y="146" class="sans kt fg">{escape(a)}</text>'
                 f'<text x="{x+8:.0f}" y="169" class="sans kt pink">{escape(b)}</text>')
        for j, l in enumerate(wrap(d, 28)[:3]):
            body += f'<text x="{x+8:.0f}" y="{198+j*19}" class="sans kd muted">{escape(l)}</text>'
        body += "</g>"
    return svg(W, H, " · ".join(f"{a} {b}" for a, b, *_ in PILLARS), css, body)


def journey():
    rowh, n = 100, len(JOURNEY)
    H = rowh * n
    css = css_base() + ".jw{font-size:11px;letter-spacing:.12em}.jr{font-size:19px;font-weight:700}.jc{font-size:15px;font-weight:600}.jd{font-size:14px}"
    path = river_d(n, rowh)
    body = (f'<path d="{path}" fill="none" stroke="{HAIR}" stroke-width="2.2" stroke-linecap="round"/>'
            f'<circle r="13" fill="{PINK}" opacity=".16"><animateMotion dur="14s" repeatCount="indefinite" path="{path}"/></circle>'
            f'<circle r="5" fill="{PINK}"><animateMotion dur="14s" repeatCount="indefinite" path="{path}"/></circle>')
    for i, (when, role, where, desc) in enumerate(JOURNEY):
        ym = i * rowh + rowh / 2
        body += (f'<g class="up" style="animation-delay:{i*.25:.2f}s">'
                 f'<circle cx="100" cy="{ym}" r="7.5" fill="{BG}" stroke="{PINK if i == 0 else ROSE}" stroke-width="2"/>'
                 f'<text x="140" y="{ym-22}" class="mono jw {"pink" if i == 0 else "muted"}">{escape(when)}</text>'
                 f'<text x="140" y="{ym+2}" class="sans jr fg">{escape(role)}<tspan class="muted" style="font-weight:400">   ·   </tspan>'
                 f'<tspan class="jc rose">{escape(where)}</tspan></text>'
                 f'<text x="140" y="{ym+26}" class="sans jd muted">{escape(desc)}</text></g>')
    return svg(W, H, " · ".join(f"{a}: {r}, {wh}" for a, r, wh, _ in JOURNEY), css, body)


def bars():
    H = 252
    css = css_base() + ".bt{font-size:17px;font-weight:700}.bl{font-size:14.5px}.bv{font-size:16px;font-weight:700}.bn{font-size:12px}"
    body = f'<text x="2" y="26" class="sans bt fg">CloudFix-Bench: remediation rate on 105 AWS Terraform cases</text>'
    for i, (label, v, frac, col) in enumerate(BARS):
        y = 62 + i * 54
        full = W - 4
        body += (f'<text x="2" y="{y}" class="sans bl muted">{escape(label)}</text>'
                 f'<text x="{W-70}" y="{y}" text-anchor="end" class="sans bv fg">{v}%</text>'
                 f'<text x="{W-2}" y="{y}" text-anchor="end" class="mono bn muted">{frac}</text>'
                 f'<rect x="2" y="{y+12}" width="{full}" height="10" rx="5" fill="{SURFACE}"/>'
                 f'<rect x="2" y="{y+12}" width="0" height="10" rx="5" fill="{col}">'
                 f'<animate attributeName="width" from="0" to="{full*v/100:.0f}" begin="{.3+i*.25:.2f}s" dur="1.6s" fill="freeze" '
                 'calcMode="spline" keyTimes="0;1" keySplines=".2 .7 .2 1"/></rect>')
    body += f'<text x="2" y="{H-14}" class="sans bn muted">95% Wilson interval 75.59% to 89.64%. Guarantees hold within the modeled Cloud Perimeter Model.</text>'
    return svg(W, H, "CloudFix-Bench results: 83.81% vs 64.76% vs 35.24%", css, body)


def cta():
    H = 230
    css = css_base() + ".big{font-size:30px;font-weight:700;letter-spacing:-.02em}.sub{font-size:16px}"
    defs = f'<clipPath id="r"><rect width="{W}" height="{H}" rx="34"/></clipPath>'
    body = (f'<rect width="{W}" height="{H}" rx="34" fill="{SURFACE}" fill-opacity=".75"/>'
            f'<g clip-path="url(#r)">' + wave_fill(186, 12, H, PLUM, .16, 24, 0) + wave_fill(200, 10, H, ROSE, .14, 17, -5) + wave_fill(214, 8, H, PINK, .14, 12, -2) + '</g>'
            f'<text x="{W/2:.0f}" y="82" text-anchor="middle" class="sans big fg up">Need resilient AI pipelines or high-assurance QA?</text>'
            f'<text x="{W/2:.0f}" y="116" text-anchor="middle" class="sans sub muted up" style="animation-delay:.25s">n8n workflows, LLM extraction, multi-tenant B2B SaaS testing. Remote.</text>'
            f'<text x="{W/2:.0f}" y="152" text-anchor="middle" class="mono up" fill="{PINK}" style="font-size:14px;animation-delay:.5s">hira229922@gmail.com</text>')
    return svg(W, H, "Need resilient AI pipelines or high-assurance QA? hira229922@gmail.com", css, body, defs)


def main():
    for d in ("projects", "sections", "buttons"):
        (OUT / d).mkdir(exist_ok=True)
    (OUT / "hero.svg").write_text(hero())
    (OUT / "stats.svg").write_text(stats())
    (OUT / "pillars.svg").write_text(pillars())
    (OUT / "journey.svg").write_text(journey())
    (OUT / "research.svg").write_text(bars())
    (OUT / "cta.svg").write_text(cta())
    for i, (slug, *rest) in enumerate(PROJECTS):
        (OUT / "projects" / f"{slug}.svg").write_text(project(i, *rest))
    for slug, title in SECTIONS:
        (OUT / "sections" / f"{slug}.svg").write_text(section(title))
    for slug, label in BUTTONS:
        (OUT / "buttons" / f"{slug}.svg").write_text(button(label))


if __name__ == "__main__":
    main()
