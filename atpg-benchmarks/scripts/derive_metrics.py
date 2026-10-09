#!/usr/bin/env python3
"""Derive secondary metrics from the transcribed Atalanta summaries.

Input : results/atalanta_summary.csv  (values transcribed from the Atalanta
        summary screenshots in results/screenshots/)
Output: results/derived_metrics.csv

Nothing here re-runs ATPG. Every output column is arithmetic on reported
values, and the script checks that the arithmetic reproduces the reported
fault coverage before writing anything.

Usage: python3 atpg-benchmarks/scripts/derive_metrics.py
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "results" / "atalanta_summary.csv"
OUT = ROOT / "results" / "derived_metrics.csv"
RANKS = ROOT / "results" / "rank_correlation_vs_gates.csv"


def load(path=SRC):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def num(row, key):
    v = row[key].strip()
    return float(v) if v else None


def derive(row):
    total = int(row["collapsed_faults"])
    red = int(row["redundant_faults"])
    abt = int(row["aborted_faults"])
    # Assumption under test: detected = collapsed - redundant - aborted.
    detected = total - red - abt
    fc = 100.0 * detected / total
    reported_fc = float(row["fault_coverage_pct"])
    if round(fc, 3) != round(reported_fc, 3):
        sys.exit(f"{row['circuit']}: derived FC {fc:.3f}% != reported {reported_fc:.3f}%")

    before = num(row, "patterns_before_compaction")
    after = num(row, "patterns_after_compaction")
    reduction = None
    if before is not None and after is not None:
        if after > before:
            sys.exit(f"{row['circuit']}: after ({after}) > before ({before}); refusing to compute a reduction")
        reduction = 100.0 * (before - after) / before

    return {
        "circuit": row["circuit"],
        "gates": row["gates"],
        "collapsed_faults": total,
        "detected_faults_derived": detected,
        "redundant_faults": red,
        "aborted_faults": abt,
        "fault_coverage_pct_reported": f"{reported_fc:.3f}",
        "fault_coverage_pct_recomputed": f"{fc:.3f}",
        # Coverage of faults that are not proven redundant (redundant faults removed from the denominator).
        "coverage_excl_redundant_pct_derived": f"{100.0 * detected / (total - red):.3f}",
        # Fault efficiency: faults resolved (detected or proven redundant) / all faults.
        "fault_efficiency_pct_derived": f"{100.0 * (detected + red) / total:.3f}",
        "pattern_reduction_pct_derived": "" if reduction is None else f"{reduction:.2f}",
    }


def ranks(values):
    s = sorted(values)
    return [s.index(v) + 1 + (s.count(v) - 1) / 2 for v in values]


def spearman(a, b):
    ra, rb = ranks(a), ranks(b)
    ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den


def rank_table(src):
    """Spearman rank correlation of each measure against gate count (descriptive only, n <= 5)."""
    out = []
    measures = ["levels", "collapsed_faults", "redundant_faults", "fault_coverage_pct",
                "backtracks", "cpu_total_s", "memory_kb"]
    for key in measures:
        out.append((key, "all 5 runs", spearman([float(r["gates"]) for r in src], [float(r[key]) for r in src])))
    comp = [r for r in src if r["patterns_before_compaction"]]
    g = [float(r["gates"]) for r in comp]
    for key in ["patterns_before_compaction", "patterns_after_compaction", "memory_kb"]:
        out.append((key, "4 compacted runs", spearman(g, [float(r[key]) for r in comp])))
    return out


def main():
    src = load()
    rows = [derive(r) for r in src]
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(
            f"{r['circuit']:>6}  detected={r['detected_faults_derived']:>5}  "
            f"FC={r['fault_coverage_pct_recomputed']}% (reported {r['fault_coverage_pct_reported']}%)  "
            f"excl-redundant={r['coverage_excl_redundant_pct_derived']}%  "
            f"efficiency={r['fault_efficiency_pct_derived']}%  "
            f"reduction={r['pattern_reduction_pct_derived'] or 'n/a'}"
        )
    print(f"wrote {OUT.relative_to(ROOT)}")
    with open(RANKS, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["measure", "runs", "spearman_rho_vs_gates"])
        for key, scope, rho in rank_table(src):
            w.writerow([key, scope, f"{rho:.2f}"])
            print(f"  rho(gates, {key}) [{scope}] = {rho:+.2f}")
    print(f"wrote {RANKS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
