#!/usr/bin/env python3
"""Recompute scan-chain balance figures from a Tessent `report_scan_chains` listing.

Usage:
    python3 scan-insertion/scripts/check_chain_balance.py [path/to/report_scan_chains.txt]

With no argument it reads scan-insertion/results/report_scan_chains.txt.

Every figure printed is derived only from the chain lengths in the report file.
Shift-cycle figures are idealised (one shift clock per scan cell in the longest
chain, no pad or tester overhead); they are calculations, not measurements.
"""
import math
import re
import sys
from pathlib import Path

DEFAULT_REPORT = Path(__file__).resolve().parent.parent / "results" / "report_scan_chains.txt"

CHAIN_RE = re.compile(
    r"chain\s*=\s*(\S+)\s+group\s*=\s*(\S+)\s+input\s*=\s*(\S+)\s+"
    r"output\s*=\s*(\S+)\s+length\s*=\s*(\d+)"
)


def parse(path):
    chains = []
    with open(path) as f:
        for line in f:
            if line.lstrip().startswith("#"):
                continue
            m = CHAIN_RE.search(line)
            if m:
                name, _group, si, so, length = m.groups()
                chains.append((name, si, so, int(length)))
    return chains


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_REPORT
    chains = parse(path)
    if not chains:
        sys.exit(f"no scan chains found in {path}")

    lengths = [c[3] for c in chains]
    total = sum(lengths)
    n = len(chains)
    longest, shortest = max(lengths), min(lengths)
    ideal_max = math.ceil(total / n)
    ideal_min = total // n

    print(f"{'Chain':<8} {'Scan in':<10} {'Scan out':<10} {'Length':>6}")
    for name, si, so, length in chains:
        print(f"{name:<8} {si:<10} {so:<10} {length:>6}")
    print()
    print(f"Chains                       : {n}")
    print(f"Total scan cells             : {total}")
    print(f"Longest / shortest chain     : {longest} / {shortest}")
    print(f"Spread (longest - shortest)  : {longest - shortest}")
    print(f"Mean chain length            : {total / n:.1f}")
    print(f"Best possible integer split  : {ideal_max} max / {ideal_min} min")
    print(f"Optimally balanced           : {'yes' if longest == ideal_max and shortest == ideal_min else 'no'}")
    print(f"Shift cycles per load        : {longest} (set by the longest chain)")
    print(f"Shift cycles, single chain   : {total} (hypothetical, same cells in one chain)")
    print(f"Shift-cycle reduction        : {total / longest:.2f}x vs single chain")
    print(f"Idle shift slots per load    : {sum(longest - l for l in lengths)} "
          f"(cells' worth of padding on shorter chains)")


if __name__ == "__main__":
    main()
