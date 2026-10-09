#!/usr/bin/env python3
"""Render the conceptual flow diagrams in assets/.

These are explanatory diagrams of the Atalanta flow and of the stuck-at
fault model. They contain no measured data except where a box quotes a
value from results/atalanta_summary.csv (marked "e.g.").

Usage: python3 atpg-benchmarks/scripts/make_diagrams.py
"""

from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT.parent / "assets"  # repository-level assets/

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
LINE = "#52514e"
BOX = "#ffffff"
BORDER = "#c3c2b7"
ACCENT = "#2a78d6"      # tool steps
ACCENT_BG = "#eaf2fc"
WARN = "#eb6834"        # aborted / outcome highlight
WARN_BG = "#fdf0ea"
GOOD_BG = "#e8f6ef"
GOOD = "#1baf7a"
FONT = 'system-ui, -apple-system, "Segoe UI", Helvetica, Arial, sans-serif'


class D:
    def __init__(self, w, h, title, desc):
        self.w, self.h = w, h
        self.p = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="t d" font-family=\'{FONT}\'>',
            f'<title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>',
            '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{LINE}"/></marker></defs>',
            f'<rect width="{w}" height="{h}" fill="{SURFACE}"/>',
        ]

    def text(self, x, y, s, size=13, fill=INK, anchor="middle", weight="normal", style="normal"):
        self.p.append(
            f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}" font-style="{style}">{escape(s)}</text>'
        )

    def box(self, x, y, w, h, title, lines=(), fill=BOX, stroke=BORDER, tcolor=INK):
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        n = len(lines)
        ty = y + h / 2 - (n * 16) / 2 + 5
        self.text(x + w / 2, ty, title, 13.5, tcolor, weight="600")
        for i, l in enumerate(lines):
            self.text(x + w / 2, ty + 17 * (i + 1), l, 11.5, INK2)

    def diamond(self, cx, cy, w, h, lines):
        pts = f"{cx},{cy - h / 2} {cx + w / 2},{cy} {cx},{cy + h / 2} {cx - w / 2},{cy}"
        self.p.append(f'<polygon points="{pts}" fill="{BOX}" stroke="{BORDER}" stroke-width="1.5"/>')
        y0 = cy - (len(lines) - 1) * 8 + 4
        for i, l in enumerate(lines):
            self.text(cx, y0 + 16 * i, l, 12, INK, weight="600")

    def arrow(self, pts, label=None, lx=None, ly=None, anchor="start"):
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        self.p.append(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="1.6" marker-end="url(#arr)"/>')
        if label:
            self.text(lx, ly, label, 11.5, INK2, anchor, "600")

    def raw(self, s):
        self.p.append(s)

    def save(self, name):
        self.p.append("</svg>")
        (ASSETS / name).write_text("\n".join(self.p) + "\n")
        print(f"wrote assets/{name}")


def testing_flow():
    w, h = 760, 840
    d = D(w, h, "Combinational ATPG testing flow",
          "Flow from ISCAS-85 benchmark netlist through Atalanta RPT, DTPG and test compaction to the final test set and summary report.")
    d.text(24, 32, "Testing Flow: ISCAS-85 Benchmark to Final Test Set", 17, INK, "start", "600")
    d.text(24, 54, "Steps in blue boxes run inside one Atalanta invocation (mode RPT + DTPG + TC)", 12.5, INK2, "start")
    cx, bw = 300, 340
    x = cx - bw / 2
    steps = [
        ("Benchmark circuit", ["ISCAS-85 combinational netlist (.bench)", "C880, C3540, C5315, C6288, C7552"], BOX, BORDER),
        ("Fault model and fault list", ["Single stuck-at-0 / stuck-at-1 on every line", "collapsed by equivalence (e.g. C880: 942 faults)"], ACCENT_BG, ACCENT),
        ("RPT - random pattern testing", ["packets of 32 random patterns, fault-simulated", "(PPSFP); detected faults dropped"], ACCENT_BG, ACCENT),
        ("DTPG - deterministic TPG (FAN)", ["one test per remaining fault, backtrack limit 10;", "each new test fault-simulated, detected faults dropped"], ACCENT_BG, ACCENT),
        ("Fault classification", ["detected / identified redundant / aborted"], ACCENT_BG, ACCENT),
        ("TC - test compaction", ["REVERSE + SHUFFLE fault-simulation passes", "remove patterns that detect no new fault"], ACCENT_BG, ACCENT),
        ("Final test set and summary", ["pattern file (-t name.test), fault coverage,", "pattern counts, backtracks, CPU time, memory"], GOOD_BG, GOOD),
    ]
    y, bh, gap = 82, 70, 32
    for i, (t, ls, f, s) in enumerate(steps):
        d.box(x, y, bw, bh, t, ls, f, s)
        if i < len(steps) - 1:
            d.arrow([(cx, y + bh), (cx, y + bh + gap - 2)])
        y += bh + gap
    # Side annotations
    ax = cx + bw / 2 + 28
    notes = [
        (82 + 1 * 102 + 35, "Fault list is built by Atalanta;", "an external list can be read with -A -f"),
        (82 + 2 * 102 + 35, "Stops after 16 consecutive packets", "detect no new fault (limit = 16)"),
        (82 + 3 * 102 + 35, "Unspecified inputs: -0 / -1 / -R / -X", "fill options (setting per run not recorded)"),
        (82 + 4 * 102 + 35, "Fault coverage =", "detected / collapsed faults"),
        (82 + 5 * 102 + 35, "Disabled with -N (C7552 run);", "shuffle limit 2"),
    ]
    for yy, a, b in notes:
        d.raw(f'<line x1="{cx + bw / 2 + 6}" y1="{yy}" x2="{ax - 6}" y2="{yy}" stroke="{BORDER}" stroke-width="1"/>')
        d.text(ax, yy - 3, a, 11.5, INK2, "start")
        d.text(ax, yy + 13, b, 11.5, INK2, "start")
    d.text(24, h - 14, "Conceptual flow of the documented Atalanta procedure. Fsim (standalone fault simulator) was also listed; no Fsim results were recorded.", 11, MUTED, "start")
    d.save("atalanta-testing-flow.svg")


def atpg_flow():
    w, h = 760, 760
    d = D(w, h, "Deterministic test generation loop",
          "Per-fault loop of Atalanta deterministic test pattern generation using FAN, with redundant and aborted outcomes and fault dropping.")
    d.text(24, 32, "ATPG Flow: Deterministic Test Generation for One Fault", 17, INK, "start", "600")
    d.text(24, 54, "DTPG phase of Atalanta (FAN algorithm), repeated until no undetected, unclassified fault remains", 12.5, INK2, "start")
    cx, bw, bh = 270, 300, 56
    x = cx - bw / 2
    d.box(x, 78, bw, bh, "Select next target fault", ["undetected after RPT and earlier tests"])
    d.arrow([(cx, 134), (cx, 156)])
    d.box(x, 158, bw, bh, "Fault activation", ["drive the faulty line to the opposite value"], ACCENT_BG, ACCENT)
    d.arrow([(cx, 214), (cx, 236)])
    d.box(x, 238, bw, bh, "Fault propagation", ["sensitize a path to a primary output (D-frontier)"], ACCENT_BG, ACCENT)
    d.arrow([(cx, 294), (cx, 316)])
    d.box(x, 318, bw, bh, "Line justification", ["backtrace objectives to primary inputs"], ACCENT_BG, ACCENT)
    d.arrow([(cx, 374), (cx, 394)])
    d.diamond(cx, 448, 220, 104, ["Test found?"])
    # Right branch: conflicts
    d.arrow([(cx + 110, 448), (560, 448)], "conflict", cx + 118, 440)
    d.diamond(620, 448, 120, 90, ["Backtracks", "> 10?"])
    d.arrow([(620, 403), (620, 370)], "no: backtrack", 628, 392)
    d.raw(f'<path d="M620,370 L620,346 L{cx + bw / 2 + 2},346" fill="none" stroke="{LINE}" stroke-width="1.6" marker-end="url(#arr)"/>')
    d.arrow([(620, 493), (620, 548)], "yes", 628, 524)
    d.box(540, 550, 160, 50, "Aborted", ["counted as not detected"], WARN_BG, WARN)
    # Search exhausted
    d.raw(f'<path d="M{cx + 60},472 L{cx + 60},665 L393,665" fill="none" stroke="{LINE}" stroke-width="1.6" marker-end="url(#arr)"/>')
    d.text(cx + 70, 560, "no test and no", 11.5, INK2, "start", "600")
    d.text(cx + 70, 576, "alternatives left", 11.5, INK2, "start", "600")
    d.box(395, 640, 160, 50, "Identified redundant", ["fault proven untestable"], WARN_BG, WARN)
    # Down branch: test found
    d.arrow([(cx, 500), (cx, 528)], "yes", cx + 8, 518)
    d.box(x, 530, bw - 120, bh, "Fill unspecified inputs", ["-0 / -1 / -R / -X"], ACCENT_BG, ACCENT)
    d.arrow([(x + 90, 586), (x + 90, 608)])
    d.box(x, 610, bw - 120, 68, "Fault-simulate the test", ["drop every fault it detects;", "update coverage"], GOOD_BG, GOOD)
    d.raw(f'<path d="M{x},644 L{x - 34},644 L{x - 34},106 L{x - 2},106" fill="none" stroke="{LINE}" stroke-width="1.6" marker-end="url(#arr)"/>')
    d.text(x - 40, 380, "next fault", 11.5, INK2, "middle", "600")
    d.text(24, h - 30, "Aborted and redundant faults also return to 'Select next target fault'. After the loop, the pattern set goes to compaction (TC).", 11, MUTED, "start")
    d.text(24, h - 14, "Conceptual diagram of the FAN-based procedure documented for Atalanta; not a trace of a specific run.", 11, MUTED, "start")
    d.save("atalanta-dtpg-loop.svg")


def and_gate(d, x, y, a_label, b_label, out_label, fault=None, fault_color=WARN):
    """Two-input AND gate with input values and output value; optional stuck-at marker on input b."""
    g = (f'<path d="M{x},{y} H{x + 40} A40,40 0 0 1 {x + 40},{y + 80} H{x} Z" fill="{BOX}" '
         f'stroke="{INK}" stroke-width="1.8"/>')
    d.raw(g)
    d.raw(f'<line x1="{x - 60}" y1="{y + 22}" x2="{x}" y2="{y + 22}" stroke="{INK}" stroke-width="1.8"/>')
    d.raw(f'<line x1="{x - 60}" y1="{y + 58}" x2="{x}" y2="{y + 58}" stroke="{INK}" stroke-width="1.8"/>')
    d.raw(f'<line x1="{x + 80}" y1="{y + 40}" x2="{x + 130}" y2="{y + 40}" stroke="{INK}" stroke-width="1.8"/>')
    d.text(x - 70, y + 26, "a", 13, INK2, "end")
    d.text(x - 70, y + 62, "b", 13, INK2, "end")
    d.text(x - 44, y + 16, a_label, 13, INK, "middle", "600")
    d.text(x - 44, y + 52, b_label, 13, INK, "middle", "600")
    d.text(x + 112, y + 34, out_label, 13, INK, "middle", "600")
    d.text(x + 140, y + 44, "z", 13, INK2, "start")
    if fault:
        d.raw(f'<line x1="{x - 22}" y1="{y + 48}" x2="{x - 12}" y2="{y + 68}" stroke="{fault_color}" stroke-width="3"/>')
        d.raw(f'<line x1="{x - 12}" y1="{y + 48}" x2="{x - 22}" y2="{y + 68}" stroke="{fault_color}" stroke-width="3"/>')
        d.text(x - 17, y + 86, fault, 11.5, fault_color, "middle", "600")


def fault_models():
    w, h = 760, 420
    d = D(w, h, "Single stuck-at fault model",
          "Conceptual two-input AND gate shown fault-free, with input b stuck-at-0, and with input b stuck-at-1, including the test vector that detects each fault.")
    d.text(24, 32, "Fault Model: Single Stuck-at Faults on a 2-input AND Gate", 17, INK, "start", "600")
    d.text(24, 54, "Conceptual illustration, not taken from a benchmark netlist. Values shown as fault-free / faulty.", 12.5, INK2, "start")
    panels = [
        (40, "Fault-free", "a=1, b=1", "1", "1", "1", None, "z = a AND b = 1", "Reference response"),
        (290, "b stuck-at-0", "test a=1, b=1", "1", "1/0", "1/0", "s-a-0", "Activate: drive b to 1", "Propagate: a = 1 passes b to z"),
        (540, "b stuck-at-1", "test a=1, b=0", "1", "0/1", "0/1", "s-a-1", "Activate: drive b to 0", "Propagate: a = 1 passes b to z"),
    ]
    for px, title, vec, av, bv, zv, f, n1, n2 in panels:
        d.raw(f'<rect x="{px}" y="78" width="200" height="270" rx="8" fill="{BOX}" stroke="{BORDER}" stroke-width="1.2"/>')
        d.text(px + 100, 102, title, 14, INK, "middle", "600")
        d.text(px + 100, 122, vec, 12, INK2)
        and_gate(d, px + 70, 150, av, bv, zv, f)
        d.text(px + 100, 296, n1, 11.5, INK2)
        d.text(px + 100, 314, n2, 11.5, INK2)
        if f:
            d.text(px + 100, 336, "Detected: z differs (1/0 or 0/1)", 11.5, WARN, "middle", "600")
    d.text(24, 372, "A line stuck-at-v is activated by driving it to the opposite value and detected when the difference reaches an observable output.", 11.5, INK2, "start")
    d.text(24, 390, "Equivalent faults (here b s-a-0, a s-a-0 and z s-a-0) need the same test, so ATPG keeps one per class: the collapsed fault list.", 11.5, INK2, "start")
    d.text(24, h - 10, "Transition (slow-to-rise / slow-to-fall) faults are not modelled by Atalanta and are not part of this project.", 11, MUTED, "start")
    d.save("stuck-at-and-gate.svg")


def compaction_flow():
    w, h = 760, 640
    d = D(w, h, "REVERSE + SHUFFLE test compaction",
          "Atalanta static compaction: reverse-order fault simulation followed by repeated random shuffles, each dropping patterns that detect no new fault.")
    d.text(24, 32, "Compaction Flow: REVERSE + SHUFFLE", 17, INK, "start", "600")
    d.text(24, 54, "Static compaction by repeated fault simulation of the generated pattern set (Atalanta TC phase)", 12.5, INK2, "start")
    cx, bw = 290, 380
    x = cx - bw / 2
    d.box(x, 78, bw, 58, "Original pattern set", ["patterns in generation order P1 ... Pn"])
    d.arrow([(cx, 136), (cx, 158)])
    d.box(x, 160, bw, 72, "Reverse-order fault simulation", ["apply Pn ... P1 on a fresh fault list;", "drop each pattern that detects no new fault"], ACCENT_BG, ACCENT)
    d.arrow([(cx, 232), (cx, 254)])
    d.box(x, 256, bw, 72, "Shuffle compaction pass", ["apply surviving patterns in random order;", "drop each pattern that detects no new fault"], ACCENT_BG, ACCENT)
    d.arrow([(cx, 328), (cx, 350)])
    d.diamond(cx, 408, 300, 112, ["Shuffles without a", "dropped pattern = limit?"])
    d.raw(f'<path d="M{cx + 150},408 L{cx + 230},408 L{cx + 230},292 L{cx + bw / 2 + 2},292" fill="none" stroke="{LINE}" stroke-width="1.6" marker-end="url(#arr)"/>')
    d.text(cx + 238, 360, "no: shuffle again", 11.5, INK2, "start", "600")
    d.arrow([(cx, 464), (cx, 490)], "yes", cx + 8, 482)
    d.box(x, 492, bw, 58, "Reduced pattern set", ["e.g. C880: 107 -> 54 patterns after 14 shuffles"], GOOD_BG, GOOD)
    d.arrow([(cx, 550), (cx, 572)])
    d.box(x, 574, bw, 40, "Coverage preserved by construction", [], BOX, BORDER)
    nx = cx + bw / 2 + 28
    d.text(nx, 510, "Limit of shuffling", 11.5, INK2, "start")
    d.text(nx, 526, "compaction = 2 in", 11.5, INK2, "start")
    d.text(nx, 542, "all compacted runs", 11.5, INK2, "start")
    d.text(nx, 592, "A pattern is removed only if", 11.5, INK2, "start")
    d.text(nx, 608, "every fault it detects is already", 11.5, INK2, "start")
    d.text(nx, 624, "detected by retained patterns", 11.5, INK2, "start")
    d.save("atalanta-compaction-flow.svg")


def main():
    ASSETS.mkdir(exist_ok=True)
    testing_flow()
    atpg_flow()
    fault_models()
    compaction_flow()


if __name__ == "__main__":
    main()
