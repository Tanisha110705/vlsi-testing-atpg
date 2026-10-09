# Repository Guide

## File map

| Path | Purpose | Origin |
|---|---|---|
| `README.md` | Portfolio overview, results, file index | Written for the consolidation |
| `LICENSE` | MIT licence for this repository's own text, data transcriptions and scripts | From `vlsi-testing-atpg`; scope note extended |
| `.gitignore` | EDA run outputs, netlists, pattern files, vendor libraries, Python caches | Merged from all three sources |
| `.gitattributes` | Marks Tessent `*.do` dofiles as Tcl for GitHub's language statistics (Linguist would otherwise count them as Stata) | New |
| `requirements.txt` | Empty by design: all scripts use the Python standard library | New |
| **scan-insertion/** | | |
| `README.md` | Module summary | Written |
| `scripts/scan.do` | Tessent Scan dofile for `riscv_core`, transcribed from the p. 17 editor screenshot | `riscv-dft-atpg/dft/scripts/scan.do` |
| `scripts/check_chain_balance.py` | Chain statistics from a `report_scan_chains` listing | `scan-insertion-tessent/scripts/` (default path updated) |
| `results/report_scan_chains.txt` | Transcribed `report_scan_chains` | `scan-insertion-tessent/dft/reports/` |
| `results/insert_test_logic_summary.txt` | Transcribed `insert_test_logic` summary and `report_test_logic` | `scan-insertion-tessent/dft/reports/` |
| `results/report_scan_cells_excerpt.txt` | First 19 rows of `report_scan_cells` | `scan-insertion-tessent/dft/reports/` |
| `results/screenshots/tessent-test-logic-insertion.png` | Tessent screenshot, cropped (p. 14) | `riscv-dft-atpg/assets/evidence/` |
| `results/screenshots/tessent-scan-chains-report.png` | Tessent screenshot, cropped (p. 14) | `riscv-dft-atpg/assets/evidence/` |
| `results/screenshots/scan-do-script.png` | `scan.do` editor text, cropped (p. 17) | `scan-insertion-tessent/assets/` |
| **tessent-atpg/** | | |
| `README.md` | Module summary | Written |
| `scripts/atpg_1.do`, `scripts/atpg_2.do` | Tessent stuck-at and transition ATPG dofiles, transcribed (pp. 17–18) | `riscv-dft-atpg/atpg/{stuck_at,transition}/` |
| `results/stuck_at_atpg_excerpt.txt`, `results/transition_atpg_excerpt.txt` | Transcribed run logs, statistics and scan volume | `riscv-dft-atpg/atpg/…` |
| `results/screenshots/tessent-*.png` (5) | Tessent ATPG screenshots, cropped (pp. 19–21) | `riscv-dft-atpg/assets/evidence/` |
| **fault-simulation/** | | |
| `README.md` | Module summary | Written |
| `results/screenshots/questasim-*.png` (2) | QuestaSim wave windows (p. 23) | `riscv-dft-atpg/assets/evidence/` |
| **atpg-benchmarks/** | | |
| `README.md` | Module summary | Written (from the old top-level README) |
| `atalanta-commands.md` | Atalanta/Fsim commands from the procedure | `atpg/README.md` |
| `benchmarks/README.md` | Which ISCAS-85 netlists were used and how to obtain them | `circuits/README.md` |
| `scripts/derive_metrics.py` | Checks the transcription and writes the derived CSVs | `scripts/` (CSV line endings fixed to LF) |
| `scripts/make_charts.py`, `scripts/make_diagrams.py` | Draw the Atalanta charts and diagrams into `assets/` | `scripts/` (output names prefixed `atalanta-`) |
| `results/atalanta_summary.csv` | Every value from the five Atalanta summaries | `results/` (screenshot paths updated) |
| `results/derived_metrics.csv`, `results/rank_correlation_vs_gates.csv` | Generated | `results/` |
| `results/README.md` | CSV column definitions | `results/README.md` |
| `results/screenshots/*.png` (5), `README.md` | Atalanta summaries, cropped (pp. 4–6) | `evidence/` |
| **docs/** | | |
| `architecture.md` | The three tracks, annotated flow, module layout, tool map | Written |
| `scan-insertion.md` | Synthesis, DRC, insertion, stitching, chains, balance, shift/capture | Merged from both scan-insertion sources |
| `riscv-dft.md` | What is and is not RISC-V work; DUT facts | Merged |
| `atpg-methodology.md` | Fault models, Atalanta and Tessent methods, coverage definitions | Merged |
| `tessent-atpg.md` | Stuck-at and transition results in full | From `riscv-dft-atpg` |
| `benchmark-results.md` | ISCAS-85 results, effort, correlation, interpretation | Merged from the old `results`, `benchmark-circuits` and `coverage-analysis` pages |
| `test-pattern-compaction.md` | Atalanta REVERSE + SHUFFLE; Tessent pattern growth; scan volume | Merged |
| `fault-simulation.md` | Atalanta, Tessent and QuestaSim simulation; Fsim | Merged |
| `evidence-audit.md` | Sources, evidence classes, every discrepancy, missing files, sanitisation | Merged from the three audits |
| `reproduction.md` | What can and cannot be re-run, with commands | Merged |
| `repository-guide.md` | This file | Written |
| **assets/** | | |
| `dft-flow.svg` | Unified three-track workflow | **New** |
| `scan-insertion-flow.svg`, `chain-balance.svg`, `scan-before-after.svg` | Scan insertion flow, chain-length chart, before/after | `scan-insertion-tessent/assets/` |
| `riscv-core-scan-architecture.svg`, `scan-chain.svg`, `scan-shift-capture.svg` | `riscv_core` DFT architecture, chain diagram, conceptual shift/capture | `riscv-dft-atpg/assets/` |
| `tessent-atpg-flow.svg`, `tessent-coverage-summary.svg`, `tessent-fault-classes.svg`, `fault-models.svg` | Tessent ATPG flow and data charts; stuck-at/transition concept | `riscv-dft-atpg/assets/` |
| `atalanta-*.svg` (7), `stuck-at-and-gate.svg` | Atalanta charts and diagrams, generated by `atpg-benchmarks/scripts/` | `vlsi-testing-atpg/assets/` (renamed) |

**Figure types.** Files under `results/screenshots/` are genuine tool output. Data charts in `assets/` are drawn from transcribed values. Flow and concept diagrams in `assets/` are explanatory and contain no measured data except where labelled.

## Source files not carried over

Nothing unique was dropped. The table lists every source file that has no direct copy here, and why.

| Source file | Reason |
|---|---|
| `scan-insertion-tessent/assets/tessent-insert-test-logic.png`, `tessent-scan-chains.png` | Second crops of the same p. 14 screenshots. The `riscv-dft-atpg` crops were kept because they show slightly more of the terminal |
| `scan-insertion-tessent/dft/scripts/scan.do` | Command lines identical to the kept copy (verified by diff) |
| `riscv-dft-atpg/dft/reports/test_logic_and_scan_chains_excerpt.txt` | Same transcription as the three kept `scan-insertion/results/*.txt` files; values identical (verified) |
| `scan-insertion-tessent/assets/architecture.svg`, `scan-chain.svg` | Superseded by the `riscv-dft-atpg` versions, which show the same data plus modes, ports and balance arithmetic |
| `scan-insertion-tessent/assets/scan-cell.svg`, `scan-operation.svg` | Conceptual; both covered by `scan-shift-capture.svg` (mux-scan cell + shift/capture timing) |
| `riscv-dft-atpg/assets/dft-flow.svg` | Single-design flow superseded by the unified `dft-flow.svg`, which keeps its "hand-off not evidenced" marker |
| Every source `README.md` and `docs/*.md` | Content merged into the module READMEs and `docs/`; duplicated explanations removed |
| `scan-insertion-tessent/LICENSE` | Same MIT licence and holder as the kept `LICENSE` |

## Not in the repository (never available)

RTL, `syn.tcl`, all netlists, ATPG setup files, pattern files, raw logs, QuestaSim scripts and transcripts, Atalanta `.test` files, Fsim output, ISCAS-85 `.bench` files (public; see [`atpg-benchmarks/benchmarks/`](../atpg-benchmarks/benchmarks/README.md)), TSMC library files (NDA), and the course report PDF (personal and institutional details). See [evidence-audit.md](evidence-audit.md#missing-evidence).
