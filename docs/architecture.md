# Architecture of the Project

## Three tracks, one portfolio

![Unified DFT / ATPG workflow](../assets/dft-flow.svg)

The work comes from four tasks of one course report. Read as a textbook flow (design → DFT checks → scan → ATPG → compaction → fault simulation → coverage), it looks like a single pipeline. **The evidence shows it was not one.** Three tracks were executed separately, on three different designs:

| Track | Stages actually run, in order | Design under test | Module |
|---|---|---|---|
| **A** | (synthesis) → DFT rule checks → scan insertion → scan-chain analysis → write netlist + ATPG setup | `riscv_core`, 2,319 flip-flops | [`scan-insertion/`](../scan-insertion/) |
| **B** | ATPG (stuck-at, transition) with internal compaction and fault simulation → pattern write-out → QuestaSim pattern simulation | Lab scan netlist `scan_inserted.v`, about 130 scan cells | [`tessent-atpg/`](../tessent-atpg/), [`fault-simulation/`](../fault-simulation/) |
| **C** | Fault list → random + FAN TPG with fault simulation → REVERSE + SHUFFLE compaction → summary | ISCAS-85 C880, C3540, C5315, C6288, C7552 | [`atpg-benchmarks/`](../atpg-benchmarks/) |

Track A ends by writing `riscv_scan.v` and an ATPG setup, but **no ATPG run read them**. Track B started from a different, much smaller lab netlist. The evidence is in [evidence-audit.md](evidence-audit.md#the-atpg-netlist-is-not-the-riscv_core-scan-netlist).

## The canonical flow, annotated

```text
Design / RTL                       riscv_core RTL ........................ not available
     ↓
Synthesis                          Design Compiler, TSMC 65 nm ........... report text only            [A]
     ↓
DFT rule checks                    Tessent Scan: clk_i, rst_i; FN1/FN4/S7  report text; left open      [A]
     ↓
Scan insertion                     Tessent Scan: +3 ports, +10 instances   tool output                 [A]
     ↓
Scan-chain analysis                5 chains: 464/464/464/464/463 ......... tool output                 [A]
     ┆
     ┆  ✗ no evidenced hand-off: ATPG did not read riscv_scan.v
     ┆
ATPG                               Tessent, lab netlist scan_inserted.v .. tool output                 [B]
                                   Atalanta, ISCAS-85 .................... tool output (separate run)  [C]
     ↓
Pattern compaction                 Tessent: implicit in create_patterns .. no before/after counts      [B]
                                   Atalanta: REVERSE + SHUFFLE ........... before/after reported       [C]
     ↓
Fault simulation                   Tessent internal; Atalanta internal ... produce all coverage        [B][C]
                                   QuestaSim pattern simulation .......... waveforms; completion unknown [B]
     ↓
Coverage and result analysis       one table per track; never pooled
```

## Module layout

Each module follows the same pattern where the files exist:

```text
<module>/
├── README.md        what was run, on which design, key results with sources, how to run
├── scripts/         original scripts (transcribed) or analysis scripts
└── results/         transcribed tool output, CSV data, and results/screenshots/ (evidence)
```

| Module | scripts/ | results/ | Notes |
|---|---|---|---|
| `scan-insertion/` | `scan.do` (Tessent, transcribed), `check_chain_balance.py` | 3 transcribed Tessent reports, 3 screenshots | |
| `tessent-atpg/` | `atpg_1.do`, `atpg_2.do` (Tessent, transcribed) | 2 transcribed ATPG logs, 5 screenshots | |
| `fault-simulation/` | — (no QuestaSim scripts exist in the source) | 2 QuestaSim screenshots | No empty `scripts/` folder was created |
| `atpg-benchmarks/` | `derive_metrics.py`, `make_charts.py`, `make_diagrams.py` | Atalanta CSV, derived CSVs, 5 screenshots | Plus `benchmarks/` (how to obtain the netlists) and `atalanta-commands.md` |

Cross-cutting explanations live in [`docs/`](.), and every figure lives in [`../assets/`](../assets/).

## Why there is no `riscv-dft/rtl/` folder

No RTL for `riscv_core` exists in any source repository or in the report, so no `rtl/` folder was created. The RISC-V-specific content is the scan insertion in `scan-insertion/`. The question "which results are RISC-V?" is answered in [riscv-dft.md](riscv-dft.md). The ATPG work is in `tessent-atpg/`, under a name that does not imply it ran on the RISC-V core.

## Tool map

| Tool | Version | Licence | Used in |
|---|---|---|---|
| Synopsys Design Compiler | not recorded | Commercial | Track A synthesis (report text only) |
| Siemens Tessent Shell: `dft -scan` context (Tessent Scan) | not recorded | Commercial | Track A |
| Siemens Tessent Shell: `patterns -scan` context (ATPG) | not recorded | Commercial | Track B |
| Siemens QuestaSim | not recorded | Commercial | Track B pattern simulation |
| TSMC 65 nm library (`tcbn65gplus`, HPBWP; Tessent model `tcbn65gplushpbwp.mdt`) | — | Foundry NDA | Tracks A and B |
| Atalanta (Virginia Tech) | not recorded; banner credits Dong S. Ha | Academic | Track C |
| Fsim (Virginia Tech) | — | Academic | Listed in Track C; no output |
| Python 3, standard library only | tested with 3.11, 3.12, 3.13 | — | `check_chain_balance.py`, `atpg-benchmarks/scripts/*.py` |

No tool version appears in any surviving screenshot, so none is stated.
