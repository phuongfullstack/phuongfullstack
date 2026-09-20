#!/usr/bin/env python3
"""Build the SVG artwork used by README.md.

Design notes
------------
The old artwork was a three-colour wave gradient plus fourteen brand-coloured
pills. That reads as decoration, not design: fourteen competing hues give the
eye nowhere to land. This version keeps ONE accent and builds hierarchy out of
typography, weight and border instead — core skills get the accent, everything
else recedes into a neutral chip.

Both files are dark self-contained cards with rounded corners, so they look
deliberate on GitHub's light *and* dark themes without needing two variants.

Everything is plain SVG + SMIL, so it animates through GitHub's image proxy
and still renders completely when animation is ignored.

    python3 assets/generate.py
"""
import json
from pathlib import Path

OUT = Path(__file__).parent
T = json.loads((OUT / "tokens.json").read_text())["color"]["dark"]
R = json.loads((OUT / "tokens.json").read_text())["radius"]

SANS = ("Inter,Segoe UI,-apple-system,BlinkMacSystemFont,"
        "Helvetica Neue,Arial,sans-serif")
MONO = ("JetBrains Mono,ui-monospace,SFMono-Regular,Menlo,"
        "Consolas,DejaVu Sans Mono,monospace")

MONO_CH = 0.6005   # advance width of the mono stack, in em
SANS_CH = 0.5400   # average advance of the sans stack at weight 500, in em


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def card(width, height, body, *, label, extra_defs=""):
    """A dark rounded card with a hairline border, a faint grid and a soft
    accent glow in the top-right. The shared shell for every asset."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{esc(label)}">
  <defs>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0 L0 0 0 40" fill="none" stroke="{T['border']}" stroke-width="1" opacity="0.55"/>
    </pattern>
    <radialGradient id="glow" cx="0.82" cy="0.12" r="0.65">
      <stop offset="0%" stop-color="{T['accent']}" stop-opacity="0.20"/>
      <stop offset="60%" stop-color="{T['accent']}" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="{T['accent']}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="cardclip">
      <rect x="0" y="0" width="{width}" height="{height}" rx="{R['xl']}"/>
    </clipPath>
{extra_defs}  </defs>
  <g clip-path="url(#cardclip)">
    <rect width="{width}" height="{height}" fill="{T['bg']}"/>
    <rect width="{width}" height="{height}" fill="url(#grid)"/>
    <rect width="{width}" height="{height}" fill="url(#glow)"/>
{body}
  </g>
  <rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="{R['xl']}"
        fill="none" stroke="{T['border']}" stroke-width="1"/>
</svg>
'''


def typing_block(lines, x, y, *, size=19, color=None, type_s=1.7, hold_s=2.0,
                 erase_s=0.8):
    """Left-aligned typewriter cycle. The first line is drawn in full in the
    base state so a renderer that ignores SMIL still shows a complete tagline
    rather than an empty row."""
    color = color or T["text-muted"]
    ch = size * MONO_CH
    per = type_s + hold_s + erase_s
    total = per * len(lines)
    kt = ";".join(f"{v:.4f}" for v in
                  (0, type_s / per, (type_s + hold_s) / per, 1))
    out = []
    for i, line in enumerate(lines):
        w = len(line) * ch
        begin = round(per * i, 2)
        first = i == 0
        out.append(f'''    <clipPath id="t{i}"><rect x="{x}" y="{y - size}" height="{size + 8}" width="{w if first else 0:.1f}">
      <animate attributeName="width" values="0;{w:.1f};{w:.1f};0" keyTimes="{kt}"
               dur="{per}s" begin="{begin}s" repeatCount="indefinite" calcMode="linear"/>
    </rect></clipPath>
    <g opacity="{1 if first else 0}">
      <animate attributeName="opacity" values="1;1;0;0"
               keyTimes="0;{(per - 0.001) / total:.4f};{per / total:.4f};1"
               dur="{total}s" begin="{begin}s" repeatCount="indefinite"/>
      <text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" font-weight="500"
            fill="{color}" clip-path="url(#t{i})" xml:space="preserve">{esc(line)}</text>
      <rect x="{(x + w) if first else x:.1f}" y="{y - size + 3}" width="2" height="{size}"
            fill="{T['accent']}">
        <animate attributeName="x" values="{x};{x + w:.1f};{x + w:.1f};{x}" keyTimes="{kt}"
                 dur="{per}s" begin="{begin}s" repeatCount="indefinite" calcMode="linear"/>
        <animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/>
      </rect>
    </g>''')
    return "\n".join(out)


def build_hero(path="hero.svg"):
    W, H = 1280, 328
    PAD = 72
    lines = [
        "ASP.NET Core / Angular / EF Core",
        "Azure / AWS / Docker / Terraform",
        "Measure first. Cache second.",
    ]

    # Concentric rounded squares: an abstract mark that reads as layered
    # architecture and, unlike a logo or a bracket glyph, does not date.
    cx, cy = 1058, H / 2
    rings = []
    for i, (s, op) in enumerate([(264, 0.09), (202, 0.15), (140, 0.24), (78, 0.40)]):
        rings.append(
            f'      <rect x="{cx - s/2}" y="{cy - s/2}" width="{s}" height="{s}" rx="{s*0.24:.0f}"\n'
            f'            fill="none" stroke="{T["accent"]}" stroke-width="1.5" opacity="{op}"\n'
            f'            transform="rotate({i * 4} {cx} {cy})"/>')
    mark = f'''    <g>
      <animateTransform attributeName="transform" type="rotate"
                        values="0 {cx} {cy};360 {cx} {cy}" dur="90s" repeatCount="indefinite"/>
{chr(10).join(rings)}
    </g>
    <circle cx="{cx}" cy="{cy}" r="7" fill="{T['accent']}">
      <animate attributeName="opacity" values="1;0.35;1" dur="3.2s" repeatCount="indefinite"/>
    </circle>'''

    body = f'''{mark}
    <text x="{PAD}" y="86" font-family="{MONO}" font-size="13" font-weight="600"
          fill="{T['accent']}" letter-spacing="3.4">FULL-STACK DEVELOPER</text>
    <text x="{PAD}" y="166" font-family="{SANS}" font-size="78" font-weight="700"
          fill="{T['text']}" letter-spacing="-2.4">Phuong</text>
    <rect x="{PAD}" y="198" width="56" height="3" rx="1.5" fill="{T['accent']}"/>
{typing_block(lines, PAD, 250)}'''

    (OUT / path).write_text(card(
        W, H, body,
        label="Phuong — full-stack developer. " + " ".join(lines)))


def chips(groups, *, width=1280, pad=56, size=14, h=36, gap=9, row_gap=10,
          label_gap=18, group_gap=34):
    """Two tiers of chips. The accent tier says what I actually build in; the
    neutral tier says what I also reach for. Fourteen equal candy pills said
    neither."""
    ch = size * SANS_CH
    avail = width - pad * 2
    blocks, y = [], pad

    for gi, (title, items, accent) in enumerate(groups):
        if gi:
            y += group_gap
        blocks.append(
            f'    <text x="{pad}" y="{y + 10}" font-family="{MONO}" font-size="11.5"'
            f' font-weight="600" fill="{T["text-faint"]}" letter-spacing="2.6">{esc(title)}</text>')
        y += label_gap + 8

        # greedy wrap
        rows, row, rw = [], [], 0.0
        for label in items:
            w = round(len(label) * ch + 34, 1)
            if row and rw + gap + w > avail:
                rows.append((row, rw))
                row, rw = [], 0.0
            rw += (gap if row else 0) + w
            row.append((label, w))
        if row:
            rows.append((row, rw))

        for row, _ in rows:
            x = pad
            for label, w in row:
                if accent:
                    fill, stroke, ink = T["accent-subtle"], T["accent"], T["accent-hover"]
                    sop = 0.55
                else:
                    fill, stroke, ink = T["bg-subtle"], T["border-strong"], T["text-muted"]
                    sop = 1
                blocks.append(
                    f'    <g><rect x="{x:.1f}" y="{y}" width="{w}" height="{h}" rx="{R["sm"]+2}"'
                    f' fill="{fill}" stroke="{stroke}" stroke-opacity="{sop}" stroke-width="1"/>'
                    f'<text x="{x + w/2:.1f}" y="{y + h/2 + size*0.35:.1f}" text-anchor="middle"'
                    f' font-family="{SANS}" font-size="{size}" font-weight="{600 if accent else 500}"'
                    f' fill="{ink}">{esc(label)}</text></g>')
                x += w + gap
            y += h + row_gap
        y -= row_gap
    return blocks, y + pad


def build_stack(path="stack.svg"):
    groups = [
        ("CORE", ["C#", ".NET", "ASP.NET Core", "EF Core"], True),
        ("FRONTEND", ["Angular", "TypeScript", "Vue", "Svelte", "React", "WPF"], False),
        ("DATA", ["SQL Server", "PostgreSQL", "MongoDB", "Cosmos DB", "Redis"], False),
        ("CLOUD & OPS", ["Azure", "AWS", "Docker", "Terraform", "GitHub Actions",
                         "RabbitMQ"], False),
    ]
    W = 1280
    blocks, H = chips(groups, width=W)
    alt = "; ".join(f"{t}: {', '.join(i)}" for t, i, _ in groups)
    (OUT / path).write_text(card(W, round(H), "\n".join(blocks), label=alt))



def _box(x, y, w, h, title, sub, *, accent=False):
    fill = T["accent-subtle"] if accent else T["bg-subtle"]
    stroke = T["accent"] if accent else T["border-strong"]
    ink = T["accent-hover"] if accent else T["text"]
    return (f'    <g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{R["md"]}"'
            f' fill="{fill}" stroke="{stroke}" stroke-opacity="{0.6 if accent else 1}"'
            f' stroke-width="1"/>'
            f'<text x="{x + w/2:.0f}" y="{y + h/2 - 3}" text-anchor="middle"'
            f' font-family="{SANS}" font-size="14.5" font-weight="600" fill="{ink}">{esc(title)}</text>'
            f'<text x="{x + w/2:.0f}" y="{y + h/2 + 16}" text-anchor="middle"'
            f' font-family="{MONO}" font-size="10.5" fill="{T["text-faint"]}"'
            f' letter-spacing="0.6">{esc(sub)}</text></g>')


def _arrow(x1, y1, x2, y2, *, accent=False, both=False, dashed=False):
    marker = "arrowA" if accent else "arrowN"
    attrs = f' marker-end="url(#{marker})"'
    if both:
        attrs += f' marker-start="url(#{marker})"'
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    stroke = T["accent"] if accent else T["border-strong"]
    return (f'    <line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}"'
            f' stroke="{stroke}" stroke-width="1.5"{dash}{attrs}/>')



def build_experience(path="experience.svg"):
    """Seven years as a picture rather than a paragraph: a KPI strip, one
    timeline track, and the domains worked in. Segments run older to newer in
    increasing weight, and each is labelled inside, so colour carries emphasis
    rather than identity."""
    W, PAD = 1280, 56
    track_w = W - PAD * 2

    kpis = [("~7", "YEARS"), ("15", "PROJECTS"), ("4", "COMPANIES"), ("12", "LARGEST TEAM")]
    roles = [("Enclave", 2019.0, 2021.0), ("Axon Active", 2021.0, 2022.0),
             ("FPT Software", 2022.0, 2024.0), ("Propel Ventures", 2024.0, 2025.5)]
    domains = ["Healthcare", "Fintech", "Fund management", "Education",
               "Property tax", "Real estate", "Gaming"]

    start, end = roles[0][1], roles[-1][2]
    span = end - start
    bar_y, bar_h, gap = 196, 44, 2

    parts = []
    col = track_w / len(kpis)
    for i, (value, label) in enumerate(kpis):
        x = PAD + col * i
        parts.append(
            f'    <text x="{x:.0f}" y="96" font-family="{SANS}" font-size="34"'
            f' font-weight="700" fill="{T["text"]}" letter-spacing="-1.1">{esc(value)}</text>'
            f'<text x="{x:.0f}" y="118" font-family="{MONO}" font-size="10.5"'
            f' font-weight="600" fill="{T["text-faint"]}" letter-spacing="1.8">{esc(label)}</text>')

    parts.append(f'    <text x="{PAD}" y="170" font-family="{MONO}" font-size="11.5"'
                 f' font-weight="600" fill="{T["text-faint"]}" letter-spacing="2.6">EXPERIENCE</text>')

    weights = [0.28, 0.44, 0.66, 1.0]
    for i, (name, a, b) in enumerate(roles):
        x = PAD + (a - start) / span * track_w + (gap if i else 0)
        w = (b - a) / span * track_w - (gap if i else 0)
        ink = T["on-accent"] if weights[i] == 1.0 else T["text"]
        parts.append(
            f'    <rect x="{x:.1f}" y="{bar_y}" width="{w:.1f}" height="{bar_h}" rx="{R["sm"]}"'
            f' fill="{T["accent"]}" fill-opacity="{weights[i]}"/>'
            f'<text x="{x + w/2:.1f}" y="{bar_y + bar_h/2 + 5}" text-anchor="middle"'
            f' font-family="{SANS}" font-size="13.5" font-weight="600" fill="{ink}">{esc(name)}</text>')

    for year in range(int(start), int(end) + 1):
        x = PAD + (year - start) / span * track_w
        # the first tick sits on the padding edge; centring it would hang outside
        anchor = "start" if year == int(start) else "middle"
        parts.append(f'    <text x="{x:.1f}" y="{bar_y + bar_h + 24}" text-anchor="{anchor}"'
                     f' font-family="{MONO}" font-size="11" fill="{T["text-faint"]}">{year}</text>')

    parts.append(f'    <text x="{PAD}" y="{bar_y + bar_h + 66}" font-family="{MONO}"'
                 f' font-size="11.5" font-weight="600" fill="{T["text-faint"]}"'
                 f' letter-spacing="2.6">DOMAINS</text>')
    cy, ch = bar_y + bar_h + 84, 32
    x = PAD
    for d in domains:
        cw = round(len(d) * 14 * SANS_CH + 30, 1)
        parts.append(
            f'    <rect x="{x:.1f}" y="{cy}" width="{cw}" height="{ch}" rx="{R["sm"]+2}"'
            f' fill="{T["bg-subtle"]}" stroke="{T["border-strong"]}" stroke-width="1"/>'
            f'<text x="{x + cw/2:.1f}" y="{cy + ch/2 + 4.8:.1f}" text-anchor="middle"'
            f' font-family="{SANS}" font-size="13" font-weight="500"'
            f' fill="{T["text-muted"]}">{esc(d)}</text>')
        x += cw + 9

    H = cy + ch + PAD
    alt = ("Seven years, fifteen projects, four companies, largest team twelve. "
           + "Timeline: " + "; ".join(f"{n} {int(a)}–{int(b)}" for n, a, b in roles)
           + ". Domains: " + ", ".join(domains) + ".")
    (OUT / path).write_text(card(W, H, "\n".join(parts), label=alt))


def build_architecture(path="architecture.svg"):
    """What a typical application I build actually looks like. A profile can
    list technologies; a diagram shows how they fit together, which is the
    part an employer is actually trying to work out."""
    W, PAD = 1280, 56
    avail = W - PAD * 2

    gap, bh = 48, 64
    bw = (avail - gap * 3) / 4
    row1 = PAD + 92
    xs = [PAD + (bw + gap) * i for i in range(4)]

    cache_y, cache_h = row1 + bh + 40, 52
    lane2 = cache_y + cache_h + 58
    bw2 = (avail - gap * 2) / 3
    xs2 = [PAD + (bw2 + gap) * i for i in range(3)]
    row2 = lane2 + 32
    H = row2 + bh + PAD

    def label(x, y, text):
        return (f'    <text x="{x}" y="{y}" font-family="{MONO}" font-size="11.5"'
                f' font-weight="600" fill="{T["text-faint"]}" letter-spacing="2.6">{text}</text>')

    parts = [label(PAD, PAD + 4, "REQUEST PATH")]
    boxes = [("Angular SPA", "typescript"),
             ("ASP.NET Core", "middleware · endpoints"),
             ("EF Core", "compiled queries"),
             ("SQL Server", "indexed · pooled")]
    for i, (title, sub) in enumerate(boxes):
        parts.append(_box(xs[i], row1, bw, bh, title, sub, accent=(i == 1)))
        if i:
            parts.append(_arrow(xs[i] - gap + 4, row1 + bh / 2, xs[i] - 8,
                                row1 + bh / 2, accent=(i <= 2)))

    # cache-aside hangs off the application, not off the database
    cx = xs[1] + bw / 2
    parts.append(_box(xs[1], cache_y, bw, cache_h, "Redis", "cache-aside"))
    parts.append(_arrow(cx, row1 + bh + 6, cx, cache_y - 8, accent=True, both=True))

    parts.append(label(PAD, lane2, "DELIVERY"))
    ship = [("GitHub Actions", "build · test · scan"),
            ("Container image", "multi-stage build"),
            ("Azure", "container apps")]
    for i, (title, sub) in enumerate(ship):
        parts.append(_box(xs2[i], row2, bw2, bh, title, sub, accent=(i == 2)))
        if i:
            parts.append(_arrow(xs2[i] - gap + 4, row2 + bh / 2, xs2[i] - 8,
                                row2 + bh / 2, dashed=True))

    defs = (f'    <marker id="arrowN" viewBox="0 0 10 10" refX="8" refY="5"'
            f' markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
            f'<path d="M0 0 L10 5 L0 10 Z" fill="{T["border-strong"]}"/></marker>\n'
            f'    <marker id="arrowA" viewBox="0 0 10 10" refX="8" refY="5"'
            f' markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
            f'<path d="M0 0 L10 5 L0 10 Z" fill="{T["accent"]}"/></marker>\n')

    alt = ("How I build: request path from browser or Blazor through ASP.NET Core "
           "to EF Core and SQL Server, with Redis as a cache aside the application. "
           "Delivery: GitHub Actions builds, tests and scans, producing a container "
           "image deployed to Azure Container Apps.")
    (OUT / path).write_text(card(W, round(H), "\n".join(parts),
                                 label=alt, extra_defs=defs))


if __name__ == "__main__":
    for f in OUT.glob("*.svg"):
        f.unlink()
    build_hero()
    build_stack()
    build_experience()
    build_architecture()
    for f in sorted(OUT.glob("*.svg")):
        print(f"{f.name:14} {f.stat().st_size:>6} bytes")
