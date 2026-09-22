"""
Architecture figure. Bands: Oversight ⊃ RegOps ⊃ AgentOps (Setup and Compiler are RegOps only).
Same style as the original prototype figure; adds GRADER and VERIFIER.
Usage: python images/make_architecture.py  ->  images/architecture.svg / .pdf / .png
"""
import os

W, H = 2450, 1380
STROKE = "#0f2b3c"
F = "DejaVu Sans, Open Sans, Verdana, sans-serif"

parts = []
A = parts.append


def box(x1, y1, x2, y2, lines, fs=40):
    A(f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" rx="22" ry="22" fill="#fff" stroke="{STROKE}" stroke-width="3"/>')
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    n = len(lines)
    for k, t in enumerate(lines):
        y = cy + (k - (n - 1) / 2) * (fs * 1.15) + fs * 0.36
        A(f'<text x="{cx}" y="{y:.0f}" text-anchor="middle" font-family="{F}" font-size="{fs}" font-weight="bold" fill="#000">{t}</text>')


def band(x1, y1, x2, y2, label=None, lx=None):
    A(f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" rx="120" ry="120" fill="none" stroke="{STROKE}" stroke-width="2.5"/>')
    if label:
        lx = lx if lx is not None else (x1 + x2) / 2
        w = 40 + 22 * len(label)
        A(f'<rect x="{lx-w/2}" y="{y1-36}" width="{w}" height="72" fill="#fff" stroke="{STROKE}" stroke-width="2.5"/>')
        A(f'<text x="{lx}" y="{y1+14}" text-anchor="middle" font-family="{F}" font-size="42" fill="#000">{label}</text>')


def arrow(pts, w=11):
    d = " ".join(("M" if i == 0 else "L") + f"{x},{y}" for i, (x, y) in enumerate(pts))
    A(f'<path d="{d}" fill="none" stroke="#000" stroke-width="{w}" stroke-linejoin="miter" marker-end="url(#ah)"/>')


A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
A('<defs><marker id="ah" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="4.2" markerHeight="4.2" '
  'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#000"/></marker></defs>')
A(f'<rect width="{W}" height="{H}" fill="#fff"/>')

# bands: Oversight ⊃ RegOps ⊃ AgentOps (Setup and Compiler are RegOps only)
band(400, 40, 2400, 1150, "Oversight", lx=680)
band(500, 115, 2320, 1095, "RegOps", lx=1130)
band(520, 370, 1940, 1045, "AgentOps", lx=1230)

# user and pull request
A('<circle cx="105" cy="530" r="40" fill="#000"/>')
A('<path d="M 30,650 A 75,75 0 0 1 180,650 L 180,655 L 30,655 Z" fill="#000"/>')
A('<circle cx="372" cy="225" r="135" fill="#fff" stroke="#000" stroke-width="3"/>')
A(f'<text x="372" y="212" text-anchor="middle" font-family="{F}" font-size="34" font-weight="bold">PULL</text>')
A(f'<text x="372" y="256" text-anchor="middle" font-family="{F}" font-size="34" font-weight="bold">REQUEST</text>')

# boxes
box(775, 155, 1105, 300, ["SETUP"])
box(740, 405, 1145, 565, ["LLM", "ORCHESTRATOR"], fs=37)
box(555, 625, 885, 785, ["TOOLS"])
box(765, 850, 1105, 1010, ["HARVESTER"])
box(1535, 400, 1895, 540, ["GRADER"])
box(1535, 610, 1895, 750, ["GENERATOR"])
box(1535, 820, 1895, 960, ["VERIFIER"])
box(2000, 620, 2290, 770, ["COMPILER"])

# output document
A('<path d="M 2300,1180 L 2365,1180 L 2390,1205 L 2390,1290 L 2300,1290 Z" fill="#fff" stroke="#000" stroke-width="5"/>')
A('<path d="M 2365,1180 L 2365,1205 L 2390,1205" fill="none" stroke="#000" stroke-width="5"/>')
for yy in range(1220, 1280, 14):
    A(f'<rect x="2318" y="{yy}" width="55" height="6" fill="#000"/>')

# arrows
arrow([(105, 465), (105, 225), (232, 225)])                 # user -> PR
arrow([(507, 225), (770, 225)])                             # PR -> setup
arrow([(940, 300), (940, 400)])                             # setup -> orchestrator
arrow([(740, 485), (720, 485), (720, 620)])                 # orchestrator -> tools
arrow([(720, 785), (720, 930), (760, 930)])                 # tools -> harvester
arrow([(945, 850), (945, 570)])                             # harvester -> orchestrator
arrow([(1145, 485), (1530, 485)])                           # orchestrator -> grader
arrow([(1715, 540), (1715, 605)])                           # grader -> generator
arrow([(1715, 750), (1715, 815)])                           # generator -> verifier
arrow([(1895, 890), (2145, 890), (2145, 775)])              # verifier -> compiler
arrow([(1895, 470), (2145, 470), (2145, 615)])              # grader -> compiler (abstained fields)
arrow([(2290, 695), (2345, 695), (2345, 1175)])             # compiler -> document
arrow([(2345, 1290), (2345, 1340), (105, 1340), (105, 680)])# document -> user

A('</svg>')

here = os.path.dirname(os.path.abspath(__file__))
svg = os.path.join(here, "architecture.svg")
open(svg, "w", encoding="utf-8").write("\n".join(parts))
try:
    import cairosvg
    cairosvg.svg2pdf(url=svg, write_to=os.path.join(here, "architecture.pdf"))
    cairosvg.svg2png(url=svg, write_to=os.path.join(here, "architecture.png"))
    print("written: architecture.svg / .pdf / .png")
except ImportError:
    print("written: architecture.svg (install cairosvg for PDF/PNG)")
