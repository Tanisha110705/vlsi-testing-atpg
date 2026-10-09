#!/usr/bin/env python3
"""Render the data charts in assets/ from results/atalanta_summary.csv.

Charts are derived from transcribed Atalanta summaries; they are not EDA
screenshots. Standard library only.

Usage: python3 atpg-benchmarks/scripts/make_charts.py
"""

import csv
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "results" / "atalanta_summary.csv"
ASSETS = ROOT.parent / "assets"  # repository-level assets/

# Palette (validated: adjacent CVD dE >= 9.2, normal-vision dE >= 27.6 on #fcfcfb)
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
S1 = "#2a78d6"  # blue
S2 = "#eb6834"  # orange
FONT = 'system-ui, -apple-system, "Segoe UI", Helvetica, Arial, sans-serif'

SOURCE_NOTE = "Source: Atalanta summaries, transcribed in atpg-benchmarks/results/atalanta_summary.csv. Derived chart, not a tool screenshot."


def load():
    with open(SRC, newline="") as f:
        rows = list(csv.DictReader(f))
    # Order circuits by gate count so every chart reads small -> large.
    return sorted(rows, key=lambda r: int(r["gates"]))


def label(r):
    return r["circuit"].upper()


class Svg:
    def __init__(self, w, h, title, desc):
        self.w, self.h = w, h
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="t d" font-family=\'{FONT}\'>',
            f"<title id=\"t\">{escape(title)}</title><desc id=\"d\">{escape(desc)}</desc>",
            f'<rect width="{w}" height="{h}" fill="{SURFACE}"/>',
        ]

    def text(self, x, y, s, size=13, fill=INK, anchor="start", weight="normal"):
        self.parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" font-weight="{weight}">{escape(str(s))}</text>'
        )

    def line(self, x1, y1, x2, y2, stroke=GRID, width=1):
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{width}"/>'
        )

    def hbar(self, x, y, length, h, fill, tip):
        """Horizontal bar anchored at x with a 4px rounded data-end."""
        if length <= 0:
            return
        r = min(4, length / 2, h / 2)
        p = (
            f"M{x:.1f},{y:.1f} H{x + length - r:.1f} Q{x + length:.1f},{y:.1f} {x + length:.1f},{y + r:.1f} "
            f"V{y + h - r:.1f} Q{x + length:.1f},{y + h:.1f} {x + length - r:.1f},{y + h:.1f} H{x:.1f} Z"
        )
        self.parts.append(f'<path d="{p}" fill="{fill}"><title>{escape(tip)}</title></path>')

    def dot(self, cx, cy, r, fill, tip):
        self.parts.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{SURFACE}" stroke-width="2">'
            f"<title>{escape(tip)}</title></circle>"
        )

    def legend(self, x, y, items):
        for name, color in items:
            self.parts.append(f'<rect x="{x}" y="{y - 10}" width="12" height="12" rx="2" fill="{color}"/>')
            self.text(x + 18, y, name, 12, INK2)
            x += 30 + 7 * len(name)

    def header(self, title, subtitle):
        self.text(24, 32, title, 17, INK, weight="600")
        self.text(24, 54, subtitle, 12.5, INK2)

    def footer(self, *notes):
        y = self.h - 14 - 16 * (len(notes) - 1)
        for n in notes:
            self.text(24, y, n, 11, MUTED)
            y += 16

    def save(self, name):
        self.parts.append("</svg>")
        (ASSETS / name).write_text("\n".join(self.parts) + "\n")
        print(f"wrote assets/{name}")


def coverage_dotplot(rows):
    """Reported fault coverage per circuit as a dot plot (non-zero axis is legitimate for dots)."""
    lo, hi = 95.0, 100.0
    left, right, top, rowh = 150, 700, 96, 40
    h = top + rowh * len(rows) + 70
    s = Svg(760, h, "Reported Fault Coverage Across Benchmark Circuits",
            "Dot plot of Atalanta-reported fault coverage for C880, C3540, C5315, C6288 and C7552.")
    s.header("Reported Fault Coverage Across Benchmark Circuits",
             "Atalanta stuck-at fault coverage; circuits ordered by gate count (smallest at top)")
    xs = lambda v: left + (v - lo) / (hi - lo) * (right - left)
    base = top + rowh * len(rows)
    for t in range(95, 101):
        s.line(xs(t), top - 8, xs(t), base, GRID)
        s.text(xs(t), base + 18, f"{t}%", 11, MUTED, "middle")
    s.text((left + right) / 2, base + 36, "Fault coverage (axis starts at 95%)", 11.5, INK2, "middle")
    for i, r in enumerate(rows):
        y = top + rowh * i + rowh / 2
        fc = float(r["fault_coverage_pct"])
        s.text(left - 14, y - 2, label(r), 13, INK, "end", "600")
        s.text(left - 14, y + 13, f"{int(r['gates']):,} gates", 11, MUTED, "end")
        s.line(left, y, xs(fc), y, AXIS, 1)
        s.dot(xs(fc), y, 6, S1, f"{label(r)}: {fc:.3f}%")
        s.text(xs(fc) - 12, y + 4, f"{fc:.3f}%", 12, INK, "end")
    s.footer(SOURCE_NOTE)
    s.save("atalanta-coverage.svg")


def undetected_breakdown(rows):
    """Faults not detected, split into proven-redundant and aborted."""
    left, right, top, rowh = 150, 640, 104, 40
    h = top + rowh * len(rows) + 86
    vmax = 160
    s = Svg(760, h, "Undetected faults by class",
            "Stacked bars of identified-redundant and aborted faults per circuit, with reported fault coverage.")
    s.header("Why Coverage Is Below 100%: Undetected Faults by Class",
             "Coverage derived from reported/project results; detected = collapsed - redundant - aborted")
    s.legend(left, 82, [("Identified redundant", S1), ("Aborted (backtrack limit)", S2)])
    xs = lambda v: left + v / vmax * (right - left)
    base = top + rowh * len(rows)
    for t in range(0, vmax + 1, 40):
        s.line(xs(t), top - 6, xs(t), base, GRID)
        s.text(xs(t), base + 18, t, 11, MUTED, "middle")
    s.text((left + right) / 2, base + 36, "Collapsed stuck-at faults not detected", 11.5, INK2, "middle")
    s.text(right + 64, top - 12, "Fault coverage", 11, MUTED, "middle")
    for i, r in enumerate(rows):
        y = top + rowh * i + 8
        red, abt = int(r["redundant_faults"]), int(r["aborted_faults"])
        s.text(left - 14, y + 11, label(r), 13, INK, "end", "600")
        s.text(left - 14, y + 26, f"{int(r['collapsed_faults']):,} faults", 11, MUTED, "end")
        if red:
            s.hbar(left, y, xs(red) - left - (2 if abt else 0), 22, S1, f"{label(r)}: {red} redundant")
        if abt:
            s.hbar(xs(red), y, xs(red + abt) - xs(red), 22, S2, f"{label(r)}: {abt} aborted")
        total = red + abt
        s.text(xs(total) + 8 if total else left + 8, y + 16,
               "0" if not total else (f"{red} + {abt}" if abt else f"{red}"), 12, INK)
        s.text(right + 64, y + 16, f"{float(r['fault_coverage_pct']):.3f}%", 12, INK, "middle")
    s.footer("Every undetected fault was identified as redundant, except the 61 aborted faults in C7552.", SOURCE_NOTE)
    s.save("atalanta-undetected-faults.svg")


def pattern_counts(rows):
    pairs = [r for r in rows if r["patterns_before_compaction"] and r["patterns_after_compaction"]]
    left, right, top, grp = 150, 660, 104, 58
    h = top + grp * len(pairs) + 104
    vmax = 300
    s = Svg(760, h, "Test patterns before and after compaction",
            "Grouped bars of Atalanta pattern counts before and after REVERSE + SHUFFLE compaction.")
    s.header("Test Patterns Before and After REVERSE + SHUFFLE Compaction",
             "Circuits with a reported before/after pair only; ordered by gate count")
    s.legend(left, 82, [("Before compaction", S1), ("After compaction", S2)])
    xs = lambda v: left + v / vmax * (right - left)
    base = top + grp * len(pairs)
    for t in range(0, vmax + 1, 50):
        s.line(xs(t), top - 6, xs(t), base, GRID)
        s.text(xs(t), base + 18, t, 11, MUTED, "middle")
    s.text((left + right) / 2, base + 36, "Test patterns", 11.5, INK2, "middle")
    for i, r in enumerate(pairs):
        y = top + grp * i + 6
        b, a = int(r["patterns_before_compaction"]), int(r["patterns_after_compaction"])
        red = 100.0 * (b - a) / b
        s.text(left - 14, y + 16, label(r), 13, INK, "end", "600")
        s.text(left - 14, y + 31, f"-{red:.1f}%", 11, MUTED, "end")
        s.hbar(left, y, xs(b) - left, 20, S1, f"{label(r)} before: {b}")
        s.text(xs(b) + 6, y + 14.5, b, 12, INK)
        s.hbar(left, y + 22, xs(a) - left, 20, S2, f"{label(r)} after: {a}")
        s.text(xs(a) + 6, y + 36.5, a, 12, INK)
    s.footer("C7552 omitted: run with compaction disabled (atalanta -N); it reports one set of 373 patterns.",
             "Percentages under each name are (before - after) / before.", SOURCE_NOTE)
    s.save("atalanta-pattern-counts.svg")


def effort_multiples(rows):
    """Small multiples: one measure per panel, each on its own zero-based axis."""
    panels = [
        ("Gates", "gates", lambda v: f"{int(v):,}"),
        ("Collapsed faults", "collapsed_faults", lambda v: f"{int(v):,}"),
        ("Backtracks", "backtracks", lambda v: f"{int(v)}"),
        ("Total CPU time (s)", "cpu_total_s", lambda v: f"{v:.3f}"),
        ("Memory (KB)", "memory_kb", lambda v: f"{int(v):,}"),
        ("Patterns in final set", None, lambda v: f"{int(v)}"),
    ]
    cols, pw, ph = 3, 232, 190
    top, left0 = 80, 24
    h = top + ph * 2 + 48
    s = Svg(760, h, "ATPG effort by circuit",
            "Six small-multiple bar charts of circuit size and Atalanta effort measures per circuit.")
    s.header("Circuit Size and ATPG Effort, Ordered by Gate Count",
             "Each panel has its own zero-based axis; compare shapes, not bar lengths across panels")
    for k, (name, key, fmt) in enumerate(panels):
        px, py = left0 + (k % cols) * (pw + 12), top + (k // cols) * ph
        s.text(px, py + 12, name, 12.5, INK, weight="600")
        vals = []
        for r in rows:
            if key:
                vals.append(float(r[key]))
            else:
                vals.append(float(r["patterns_after_compaction"] or r["patterns_uncompacted_run"]))
        vmax = max(vals) or 1
        bx, bw = px + 56, pw - 56 - 52
        s.line(bx, py + 22, bx, py + 22 + 28 * len(rows), AXIS)
        for i, (r, v) in enumerate(zip(rows, vals)):
            y = py + 26 + 28 * i
            s.text(bx - 8, y + 13, label(r), 11.5, INK2, "end")
            fill = S2 if (key is None and not r["patterns_after_compaction"]) else S1
            s.hbar(bx, y, v / vmax * bw, 18, fill, f"{label(r)} {name}: {fmt(v)}")
            s.text(bx + v / vmax * bw + 5, y + 13, fmt(v), 11, INK)
    s.footer("Last panel: compacted pattern count; C7552 (orange) is its 373-pattern set from a run with compaction disabled.",
             SOURCE_NOTE)
    s.save("atalanta-complexity-effort.svg")


def main():
    ASSETS.mkdir(exist_ok=True)
    rows = load()
    coverage_dotplot(rows)
    undetected_breakdown(rows)
    pattern_counts(rows)
    effort_multiples(rows)


if __name__ == "__main__":
    main()
