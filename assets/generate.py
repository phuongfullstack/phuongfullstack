#!/usr/bin/env python3
"""Generate the self-hosted SVG assets used by README.md.

Everything here is plain SVG + SMIL so it renders (and animates) through
GitHub's image proxy without depending on any third-party service.

    python3 assets/generate.py
"""
from pathlib import Path

OUT = Path(__file__).parent
SANS = "Segoe UI,-apple-system,BlinkMacSystemFont,Helvetica Neue,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,DejaVu Sans Mono,monospace"

PURPLE, BLUE, TEAL = "#512BD4", "#0078D4", "#50E3C2"


def wave(y, amp, fill, opacity, dur, width=1200, height=200):
    """One horizontal wave band, slowly drifting sideways forever."""
    seg = width / 2
    d = (f"M0 {y} "
         f"q {seg/4} {-amp} {seg/2} 0 t {seg/2} 0 t {seg/2} 0 t {seg/2} 0 "
         f"t {seg/2} 0 t {seg/2} 0 "
         f"L{width*2} {height} L0 {height} Z")
    return (f'<g opacity="{opacity}">'
            f'<path d="{d}" fill="{fill}">'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="0 0;{-seg} 0" dur="{dur}s" repeatCount="indefinite"/>'
            f'</path></g>')


def banner(path, *, flip=False, height=200, title=None, subtitle=None):
    w = 1200
    stops = f'<stop offset="0%" stop-color="{PURPLE}"/><stop offset="55%" stop-color="{BLUE}"/><stop offset="100%" stop-color="{TEAL}"/>'
    waves = "".join([
        wave(height * 0.62, 26, "#ffffff", 0.10, 18, height=height),
        wave(height * 0.74, 20, "#ffffff", 0.12, 26, height=height),
        wave(height * 0.86, 16, "#ffffff", 0.10, 34, height=height),
    ])
    body = f'''<rect width="{w}" height="{height}" fill="url(#grad)"/>
  <rect width="{w}" height="{height}" fill="url(#dots)"/>
  {waves}'''
    if flip:
        body = f'<g transform="translate(0,{height}) scale(1,-1)">{body}</g>'

    text = ""
    if title:
        text = f'''<g opacity="1" text-anchor="middle" fill="#ffffff">
    <animate attributeName="opacity" values="0;1" dur="1.1s" begin="0.15s" fill="freeze"/>
    <text x="{w/2}" y="96" font-family="{SANS}" font-size="64" font-weight="700"
          letter-spacing="1" style="paint-order:stroke">{title}</text>
    <text x="{w/2}" y="138" font-family="{SANS}" font-size="20" font-weight="500"
          letter-spacing="6" fill-opacity="0.92">{subtitle}</text>
  </g>'''

    label = f"{title} — {subtitle}" if title else "decorative wave"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" role="img" aria-label="{label}">
  <defs>
    <linearGradient id="grad" x1="0" y1="0" x2="1" y2="1">{stops}</linearGradient>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="2.5" cy="2.5" r="1.3" fill="#ffffff" fill-opacity="0.15"/>
    </pattern>
  </defs>
  {body}
  {text}
</svg>
'''
    (OUT / path).write_text(svg)


def typing(path, lines, *, width=660, size=20, color=BLUE,
           type_s=1.6, hold_s=1.9, erase_s=0.7):
    """Typewriter cycle: each line types in, holds, erases. Monospace keeps
    the character maths exact, so the caret always lands on the last glyph."""
    ch = size * 0.6005  # advance width of the monospace stack at this size
    per = type_s + hold_s + erase_s
    total = per * len(lines)
    height = size + 18
    baseline = size + 4

    parts = []
    for i, line in enumerate(lines):
        w = len(line) * ch
        x0 = round((width - w) / 2, 2)
        begin = round(per * i, 2)
        kt = [0, type_s / per, (type_s + hold_s) / per, 1]
        keytimes = ";".join(f"{k:.4f}" for k in kt)
        # clip rect reveals the text; caret rides its right-hand edge
        base_w = f"{w:.1f}" if i == 0 else "0"
        base_op = "1" if i == 0 else "0"
        parts.append(f'''  <clipPath id="c{i}"><rect x="{x0}" y="0" height="{height}" width="{base_w}">
    <animate attributeName="width" values="0;{w:.1f};{w:.1f};0" keyTimes="{keytimes}"
             dur="{per}s" begin="{begin}s" repeatCount="indefinite" calcMode="linear"/>
  </rect></clipPath>
  <g opacity="{base_op}">
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{(per - 0.001)/total:.4f};{per/total:.4f};1"
             dur="{total}s" begin="{begin}s" repeatCount="indefinite"/>
    <text x="{x0}" y="{baseline}" font-family="{MONO}" font-size="{size}" font-weight="600"
          fill="{color}" clip-path="url(#c{i})" xml:space="preserve">{line}</text>
    <rect y="{baseline - size + 2}" width="2.5" height="{size}" fill="{color}" x="{x0 + w if i == 0 else x0:.1f}">
      <animate attributeName="x" values="{x0};{x0 + w:.1f};{x0 + w:.1f};{x0}" keyTimes="{keytimes}"
               dur="{per}s" begin="{begin}s" repeatCount="indefinite" calcMode="linear"/>
      <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>
    </rect>
  </g>''')

    alt = " — ".join(lines)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
           f'width="{width}" height="{height}" role="img" aria-label="{alt}">\n'
           + "\n".join(parts) + "\n</svg>\n")
    (OUT / path).write_text(svg)


def _ink(hex_color):
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return "#0d1117" if (0.299 * r + 0.587 * g + 0.114 * b) > 165 else "#ffffff"


def pills(path, rows, *, size=14, height=34, gap=10, pad=15):
    ch = size * 0.565  # average advance of the bold sans stack
    laid, widest = [], 0
    for row in rows:
        items = [(label, color, round(len(label) * ch + pad * 2, 1)) for label, color in row]
        total = sum(w for _, _, w in items) + gap * (len(items) - 1)
        laid.append((items, total))
        widest = max(widest, total)

    width = round(widest + 8)
    svg_h = len(rows) * height + (len(rows) - 1) * gap
    parts, n = [], 0
    for r, (items, total) in enumerate(laid):
        x = (width - total) / 2
        y = r * (height + gap)
        for label, color, w in items:
            begin = round(n * 0.06, 2)
            parts.append(
                f'  <g opacity="1"><animate attributeName="opacity" values="0;1" dur="0.45s" '
                f'begin="{begin}s" fill="freeze"/>'
                f'<rect x="{x:.1f}" y="{y}" width="{w}" height="{height}" rx="{height/2}" fill="{color}"/>'
                f'<text x="{x + w/2:.1f}" y="{y + height/2 + size*0.36:.1f}" text-anchor="middle" '
                f'font-family="{SANS}" font-size="{size}" font-weight="600" fill="{_ink(color)}">{label}</text></g>')
            x += w + gap
            n += 1

    alt = ", ".join(label for row in rows for label, _ in row)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {svg_h}" '
           f'width="{width}" height="{svg_h}" role="img" aria-label="{alt}">\n'
           + "\n".join(parts) + "\n</svg>\n")
    (OUT / path).write_text(svg)


if __name__ == "__main__":
    banner("header.svg", title="Phuong", subtitle=".NET FULL-STACK DEVELOPER")
    banner("footer.svg", flip=True, height=120)
    typing("typing.svg", [
        "ASP.NET Core / Blazor / EF Core",
        "Azure / Docker / GitHub Actions",
        "Measure first. Cache second.",
    ])
    pills("tech-stack.svg", [
        [("C#", "#239120"), (".NET", "#512BD4"), ("Blazor", "#5C2D91"),
         ("TypeScript", "#3178C6"), ("React", "#61DAFB"), ("Angular", "#DD0031"), ("Vue", "#4FC08D")],
        [("Azure", "#0078D4"), ("Docker", "#2496ED"), ("Kubernetes", "#326CE5"),
         ("GitHub Actions", "#2088FF"), ("SQL Server", "#CC2927"),
         ("PostgreSQL", "#4169E1"), ("Redis", "#DC382D")],
    ])
    for f in sorted(OUT.glob("*.svg")):
        print(f"{f.name:18} {f.stat().st_size:>6} bytes")
