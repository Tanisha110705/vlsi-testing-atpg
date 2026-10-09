# Reproduction

Three levels of reproduction apply, and they differ sharply in what is possible:

| Level | What | Possible from this repository? | Tested for this repository? |
|---|---|---|---|
| **1. Analysis** | Recompute every derived number, CSV and data chart from the transcribed tool output | **Yes**: Python 3 standard library only | **Yes**: see below |
| **2. Benchmark ATPG** | Re-run Atalanta on ISCAS-85 | Yes, with Atalanta and the public `.bench` files (not included) | No: Atalanta was not available |
| **3. Commercial flows** | Synthesis, Tessent scan insertion, Tessent ATPG, QuestaSim | **No**: needs licensed tools, the TSMC library and netlists that are not preserved | No |

## 1. Analysis scripts (no EDA tools needed)

Requirements: Python 3, standard library only (tested with 3.11, 3.12 and 3.13). There are no third-party packages; [`requirements.txt`](../requirements.txt) is intentionally empty. Run from the repository root:

```sh
# Scan insertion: chain statistics from the transcribed report_scan_chains
python3 scan-insertion/scripts/check_chain_balance.py

# Benchmark ATPG: check the transcription, derive metrics, redraw the figures
python3 atpg-benchmarks/scripts/derive_metrics.py   # -> atpg-benchmarks/results/derived_metrics.csv, rank_correlation_vs_gates.csv
python3 atpg-benchmarks/scripts/make_charts.py      # -> assets/atalanta-{coverage,undetected-faults,pattern-counts,complexity-effort}.svg
python3 atpg-benchmarks/scripts/make_diagrams.py    # -> assets/atalanta-{testing-flow,dtpg-loop,compaction-flow}.svg, assets/stuck-at-and-gate.svg
```

| Script | Expected result |
|---|---|
| `check_chain_balance.py` | 5 chains, 2,319 cells, longest 464, shortest 463, spread 1, "Optimally balanced: yes" |
| `derive_metrics.py` | Recomputed fault coverage equals the reported value for all five circuits. The script exits non-zero if not. |
| All four | Committed files are reproduced byte-for-byte (`git status` shows no change) |

`check_chain_balance.py` accepts any Tessent `report_scan_chains` listing in the same format, so a fresh run's output can be checked by passing its path.

The Tessent ATPG numbers have no script. Their arithmetic checks (TC, FC, AE, volume) are shown inline in [tessent-atpg.md](tessent-atpg.md#reconciliation-by-arithmetic-derived).

## 2. Benchmark ATPG (Atalanta)

1. Obtain **Atalanta** (Virginia Tech academic tool; public source mirror, e.g. <https://github.com/hsluoyz/Atalanta>; check its licence) and the ISCAS-85 `.bench` netlists ([`atpg-benchmarks/benchmarks/README.md`](../atpg-benchmarks/benchmarks/README.md)). Before comparing, check that each netlist's gate and I/O counts match [benchmark-results.md](benchmark-results.md#benchmark-circuits).
2. Run the commands as documented in the source procedure:

   ```sh
   atalanta -t c880.test  iscas85/c880.bench      # RPT + DTPG + TC (REVERSE + SHUFFLE)
   atalanta -t c3540.test iscas85/c3540.bench
   atalanta -t c5315.test iscas85/c5315.bench
   atalanta -t c6288.test iscas85/c6288.bench     # recorded command unknown, see evidence-audit.md
   atalanta -N -t c7552.test iscas85/c7552.bench  # compaction disabled, as recorded
   ```

3. Copy each summary into a row of `atpg-benchmarks/results/atalanta_summary.csv` and rerun level 1.

**Expected differences:** Atalanta prints a per-run random seed (recorded in the CSV). A different seed changes the random patterns, so pattern counts and possibly aborted counts can differ. Collapsed-fault and redundant counts should not change. CPU time and memory depend on the host. The fill option of the recorded runs is unknown.

Optional, not done: independent fault simulation with `fsim -t c880.test iscas85/c880.bench`.

## 3. Commercial flows

Required for all three: the licensed tools, TSMC 65 nm views (Design Compiler `.db`, Tessent `tcbn65gplushpbwp.mdt`, Verilog simulation models), and the design inputs listed. None of these is in the repository or redistributable. The scripts use bare file names, so they run from the directory that holds their inputs. Invocation commands were not recorded in the report; the `tessent -shell -dofile …` form below is the standard Tessent Shell batch invocation, not a recorded command.

### Scan insertion: `riscv_core`

| | |
|---|---|
| Inputs | `netlist_riscvcore.v` (Design Compiler output; requires the RTL and `syn.tcl`, neither available), `tcbn65gplushpbwp.mdt` |
| Script | [`scan-insertion/scripts/scan.do`](../scan-insertion/scripts/scan.do) |
| Typical invocation | `tessent -shell -dofile scan.do -log scan.log` |
| Outputs | `riscv_scan.v`, ATPG setup `scan.*` |
| A re-run should match | `report_scan_chains`: 5 chains 464/464/464/464/463; `insert_test_logic`: 3 ports, 10 instances, 5 retiming, 5 chains; DRC: FN1, FN4, S7 (per report) |

Cell ordering and lockup-latch placement may change with tool or library version.

### Tessent ATPG: lab scan netlist

| | Stuck-at | Transition |
|---|---|---|
| Script | [`atpg_1.do`](../tessent-atpg/scripts/atpg_1.do) | [`atpg_2.do`](../tessent-atpg/scripts/atpg_2.do) |
| Inputs | `scan_inserted.v`, `scan_inserted.dofile`, library | `LAB4/scan_inserted.v`, `LAB4/scan_inserted.dofile`, library |
| Outputs | `serialpatterns.v`, `parallelpatterns.v`, `pattern.ascii` | Same names under `LAB6/transition/` (the directory must exist) |
| Should match | FU 3,300; TC 100.00 %; FC 97.82 %; 69 patterns; volume 9,240 | FU 2,690; TC = FC 85.95 %; 86 patterns; volume 11,310 |

Pattern counts may vary slightly between Tessent versions (random-pattern seeding, compaction).

**ATPG on `riscv_core` (not done):** change `read_verilog` to `riscv_scan.v` and the `dofile` to the `scan` setup from `write_atpg_setup`. The results would be **new**, not a reproduction of the table above.

### QuestaSim pattern simulation

No script exists in the source. A generic sequence for a Tessent Verilog testbench (not recorded; library paths deliberately omitted):

```sh
vlib work
vlog <cell_models>.v scan_inserted.v serialpatterns.v
vsim -c <testbench_top> -do "run -all; quit"
```

A correct run should end with the testbench reporting zero mismatches. The report contains no such transcript.

### Synthesis

Not reproducible: `syn.tcl` and the RTL are not available, and no synthesis command is reconstructed.
