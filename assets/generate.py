#!/usr/bin/env python3
"""Build the SVG artwork used by README.md.

Design: editorial. Paper background, a serif display face, hairline rules
instead of boxes, and the accent reserved for numbers and the caret. No
card chrome — the artwork is meant to sit on the page rather than on top
of it.

Each file carries its own light and dark values in a `<style>` block and
switches on `prefers-color-scheme`, so one file serves both GitHub themes.
Light is the base state, so a renderer that ignores the media query still
gets the intended design.

    python3 assets/generate.py
"""
import json
from pathlib import Path

OUT = Path(__file__).parent
_TOK = json.loads((OUT / "tokens.json").read_text())
L, D = _TOK["color"]["light"], _TOK["color"]["dark"]

SERIF = "ui-serif,Georgia,Iowan Old Style,Palatino Linotype,Times New Roman,serif"
SANS = ("Inter,-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica Neue,"
        "Arial,sans-serif")
MONO = ("ui-monospace,SFMono-Regular,Menlo,Consolas,DejaVu Sans Mono,monospace")

MONO_CH = 0.6005
SANS_CH = 0.5400

VARS = ["bg", "border", "border-strong", "text", "text-muted", "text-faint", "accent"]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _theme_css():
    def block(tokens):
        return " ".join(f"--{k}:{tokens[k]};" for k in VARS)
    return f"""  <style>
    svg {{ {block(L)} }}
    @media (prefers-color-scheme: dark) {{ svg {{ {block(D)} }} }}
    .bg   {{ fill: var(--bg); }}
    .ink  {{ fill: var(--text); }}
    .mut  {{ fill: var(--text-muted); }}
    .fai  {{ fill: var(--text-faint); }}
    .acc  {{ fill: var(--accent); }}
    .hair {{ stroke: var(--border); stroke-width: 1; fill: none; }}
    .edge {{ stroke: var(--border-strong); stroke-width: 1; fill: none; }}
    .accs {{ stroke: var(--accent); stroke-width: 1.5; fill: none; }}
    .serif {{ font-family: {SERIF}; }}
    .sans  {{ font-family: {SANS}; }}
    .mono  {{ font-family: {MONO}; }}
    .lbl  {{ font-size: 11px; font-weight: 600; letter-spacing: 2.4px; }}
  </style>
"""


def sheet(width, height, body, *, label, extra_defs=""):
    """A plain sheet: page-coloured background, no border, no rounded corners.
    It is meant to read as part of the README, not as a widget on top of it."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="{esc(label)}">
{_theme_css()}{f"  <defs>{chr(10)}{extra_defs}  </defs>{chr(10)}" if extra_defs else ""}  <rect class="bg" width="{width}" height="{height}"/>
{body}
</svg>
'''


def rule(x1, x2, y, cls="hair"):
    return f'    <line class="{cls}" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}"/>'


def label(x, y, text):
    return f'    <text class="mono lbl fai" x="{x}" y="{y}">{esc(text)}</text>'


def typing_block(lines, x, y, *, size=17, type_s=1.7, hold_s=2.0, erase_s=0.8):
    """Left-aligned typewriter cycle. The first line is drawn in full in the
    base state, so a renderer that ignores SMIL shows a complete tagline."""
    ch = size * MONO_CH
    per = type_s + hold_s + erase_s
    total = per * len(lines)
    kt = ";".join(f"{v:.4f}" for v in (0, type_s / per, (type_s + hold_s) / per, 1))
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
      <text class="mono mut" x="{x}" y="{y}" font-size="{size}"
            clip-path="url(#t{i})" xml:space="preserve">{esc(line)}</text>
      <rect class="acc" x="{(x + w) if first else x:.1f}" y="{y - size + 3}" width="2" height="{size}">
        <animate attributeName="x" values="{x};{x + w:.1f};{x + w:.1f};{x}" keyTimes="{kt}"
                 dur="{per}s" begin="{begin}s" repeatCount="indefinite" calcMode="linear"/>
        <animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/>
      </rect>
    </g>''')
    return "\n".join(out)


def build_hero(path="hero.svg"):
    W, H, PAD = 1280, 300, 64
    lines = ["ASP.NET Core / Angular / EF Core",
             "Azure / AWS / Docker / Terraform",
             "Measure first. Cache second."]
    body = f'''{rule(PAD, W - PAD, 58)}
    <text class="mono lbl fai" x="{PAD}" y="92">FULL-STACK DEVELOPER</text>
    <text class="mono lbl acc" x="{W - PAD}" y="92" text-anchor="end">8 YEARS</text>
    <text class="serif ink" x="{PAD}" y="196" font-size="96" letter-spacing="-3">Phuong</text>
{rule(PAD, W - PAD, 228)}
{typing_block(lines, PAD, 268)}'''
    (OUT / path).write_text(sheet(W, H, body,
        label="Phuong — full-stack developer, 8 years. " + " ".join(lines)))


def build_stack(path="stack.svg"):
    """Tiers as a specification table: a mono label in a fixed left column,
    the technologies set as text on the right, a hairline between rows. No
    chips, no boxes — the type carries the structure."""
    W, PAD = 1280, 64
    col, pitch = 210, 62
    tiers = [
        ("CORE", ["C#", ".NET", "ASP.NET Core", "EF Core"]),
        ("FRONTEND", ["Angular", "TypeScript", "Vue", "Svelte", "React", "WPF"]),
        ("DATA", ["SQL Server", "PostgreSQL", "MongoDB", "Cosmos DB", "Redis"]),
        ("CLOUD & OPS", ["Azure", "AWS", "Docker", "Terraform", "GitHub Actions", "RabbitMQ"]),
        ("QUALITY", ["xUnit", "NUnit", "Moq", "Testcontainers", "BenchmarkDotNet"]),
    ]
    parts, y = [label(PAD, 40, "STACK")], 78
    for i, (name, items) in enumerate(tiers):
        parts.append(rule(PAD, W - PAD, y))
        parts.append(f'    <text class="mono lbl fai" x="{PAD}" y="{y + 34}">{esc(name)}</text>')
        first = i == 0
        parts.append(
            f'    <text class="sans {"ink" if first else "mut"}" x="{PAD + col}" y="{y + 36}"'
            f' font-size="17" font-weight="{600 if first else 400}">'
            f'{esc("  ·  ".join(items))}</text>')
        y += pitch
    parts.append(rule(PAD, W - PAD, y))
    H = y + PAD
    alt = "; ".join(f"{n}: {', '.join(i)}" for n, i in tiers)
    (OUT / path).write_text(sheet(W, H, "\n".join(parts), label=alt))


def _node(x, y, w, h, title, sub, *, accent=False):
    cls = "accs" if accent else "edge"
    ink = "acc" if accent else "ink"
    return (f'    <g><rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}"/>'
            f'<text class="sans {ink}" x="{x + w/2:.0f}" y="{y + h/2 - 2}" text-anchor="middle"'
            f' font-size="14" font-weight="600">{esc(title)}</text>'
            f'<text class="mono fai" x="{x + w/2:.0f}" y="{y + h/2 + 17}" text-anchor="middle"'
            f' font-size="10.5">{esc(sub)}</text></g>')


def _link(x1, y1, x2, y2, *, accent=False, both=False, dashed=False):
    marker = "aA" if accent else "aN"
    attrs = f' marker-end="url(#{marker})"' + (f' marker-start="url(#{marker})"' if both else "")
    dash = ' stroke-dasharray="4 4"' if dashed else ""
    cls = "accs" if accent else "edge"
    return (f'    <line class="{cls}" x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}"'
            f' y2="{y2:.0f}"{dash}{attrs}/>')


def build_architecture(path="architecture.svg"):
    """What a system I build looks like. A profile can list technologies; a
    diagram shows how they fit together, which is the part a reader is
    actually trying to work out."""
    W, PAD = 1280, 64
    avail = W - PAD * 2
    gap, bh = 40, 60
    bw = (avail - gap * 3) / 4
    r1 = 106
    xs = [PAD + (bw + gap) * i for i in range(4)]

    side_y = r1 + bh + 44
    r2_label = side_y + 54 + 42
    r2 = r2_label + 30
    bw2 = (avail - gap * 2) / 3
    xs2 = [PAD + (bw2 + gap) * i for i in range(3)]
    H = r2 + bh + PAD

    parts = [label(PAD, 40, "REQUEST PATH"), rule(PAD, W - PAD, 58)]
    row = [("Angular SPA", "typescript"), ("ASP.NET Core", "middleware · endpoints"),
           ("EF Core", "compiled queries"), ("SQL Server", "indexed · pooled")]
    for i, (t, s) in enumerate(row):
        parts.append(_node(xs[i], r1, bw, bh, t, s, accent=(i == 1)))
        if i:
            parts.append(_link(xs[i] - gap + 2, r1 + bh / 2, xs[i] - 6, r1 + bh / 2,
                               accent=(i <= 2)))

    # what hangs off the application rather than sitting in the request path
    cx = xs[1] + bw / 2
    parts.append(_node(xs[1], side_y, bw, 54, "Redis", "cache-aside"))
    parts.append(_link(cx, r1 + bh + 4, cx, side_y - 6, accent=True, both=True))
    qx = xs[2] + bw / 2
    parts.append(_node(xs[2], side_y, bw, 54, "RabbitMQ", "workers · batch jobs"))
    parts.append(_link(qx, r1 + bh + 4, qx, side_y - 6))

    parts += [label(PAD, r2_label, "DELIVERY"), rule(PAD, W - PAD, r2_label + 18)]
    ship = [("GitHub Actions", "build · test · scan"),
            ("Container image", "multi-stage build"),
            ("Azure", "container apps · terraform")]
    for i, (t, s) in enumerate(ship):
        parts.append(_node(xs2[i], r2, bw2, bh, t, s, accent=(i == 2)))
        if i:
            parts.append(_link(xs2[i] - gap + 2, r2 + bh / 2, xs2[i] - 6, r2 + bh / 2,
                               dashed=True))

    defs = ('    <marker id="aN" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5"'
            ' markerHeight="5" orient="auto-start-reverse">'
            '<path d="M0 0 L10 5 L0 10 Z" fill="var(--border-strong)"/></marker>\n'
            '    <marker id="aA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5"'
            ' markerHeight="5" orient="auto-start-reverse">'
            '<path d="M0 0 L10 5 L0 10 Z" fill="var(--accent)"/></marker>\n')

    alt = ("Request path: Angular SPA to ASP.NET Core to EF Core to SQL Server, with "
           "Redis cache-aside and RabbitMQ workers alongside the application. Delivery: "
           "GitHub Actions builds, tests and scans into a container image deployed to "
           "Azure Container Apps with Terraform.")
    (OUT / path).write_text(sheet(W, round(H), "\n".join(parts), label=alt,
                                  extra_defs=defs))


if __name__ == "__main__":
    for f in OUT.glob("*.svg"):
        f.unlink()
    build_hero()
    build_stack()
    build_architecture()
    for f in sorted(OUT.glob("*.svg")):
        print(f"{f.name:18} {f.stat().st_size:>6} bytes")
