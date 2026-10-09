# Evidence Audit

This page records where every published fact comes from, where the sources disagree, and how each disagreement was resolved. All other pages point here when a number needs a caveat.

## Sources

| Source | Content | In this repository? |
|---|---|---|
| Course report, *BEVD309L Testing of VLSI Circuits*, VIT, Fall 2025-26 (23 pages) | Task 1: Atalanta/Fsim on ISCAS-85 (pp. 2–9). Task 2: synthesis, DRC and scan insertion (pp. 10–14, 17). Task 3: Tessent ATPG (pp. 15–21). Task 4: QuestaSim (pp. 22–23). Prose, tables, editor screenshots of the scripts, terminal screenshots and waveform screenshots. | **No.** It contains a student register number, instructor details and lab server names. Its screenshots are kept in cropped form under each module's `results/screenshots/`. |
| `Tanisha110705/vlsi-testing-atpg` (this repository, before consolidation) | Task 1 only | Kept as the [`atpg-benchmarks/`](../atpg-benchmarks/) module |
| `Tanisha110705/scan-insertion-tessent` | Task 2 only | Merged into [`scan-insertion/`](../scan-insertion/) |
| `Tanisha110705/riscv-dft-atpg` | Tasks 2, 3 and 4 | Task 2 merged into `scan-insertion/`; Task 3 into [`tessent-atpg/`](../tessent-atpg/); Task 4 into [`fault-simulation/`](../fault-simulation/) |

All three source repositories were reconstructed from the same report. During consolidation, every number they publish was re-checked against the report's screenshots. No value disagreed with the tool output, apart from the report-prose discrepancies listed below, which the source repositories had already identified.

Page numbers on this page refer to the course report.

## Evidence classes

Every result in this repository carries one of these tags:

| Tag | Meaning | Strength |
|---|---|---|
| **Tool** | Text visible in a tool screenshot (Atalanta summary, Tessent terminal, QuestaSim wave window) or in a transcribed script | Strongest available |
| **Text** | A statement in the report's prose or hand-typed tables | Weaker; conflicts with tool output in several places |
| **Derived** | Arithmetic on Tool values, with the arithmetic shown or scripted | As strong as its inputs |

When Tool and Text disagree, the Tool value is used and the Text value is recorded here.

No raw log, netlist, pattern file or waveform database exists for any experiment. Every "Tool" value comes from a screenshot.

## Design under test per experiment

| Experiment | Design under test | Evidence |
|---|---|---|
| Benchmark ATPG (Task 1) | ISCAS-85 C880, C3540, C5315, C6288, C7552 (`.bench`) | Atalanta summaries name each circuit |
| Scan insertion (Task 2) | `riscv_core`, gate-level netlist `netlist_riscvcore.v`, 2,319 flip-flops | `scan.do`; instance paths `riscv_core/u_mul`, `u_div`, … in `report_test_logic` |
| Tessent ATPG (Task 3) | Lab scan netlist `scan_inserted.v` (stuck-at) and `LAB4/scan_inserted.v` (transition), about 130 scan cells | `atpg_1.do`, `atpg_2.do`; scan volume reports |
| QuestaSim (Task 4) | The Task 3 pattern testbenches on the lab scan netlist | Wave-window signal prefix `riscv_core_seri…` |

## Task 1: ISCAS-85 benchmark ATPG (Atalanta)

Values used: the five Atalanta summary screenshots ([`atpg-benchmarks/results/screenshots/`](../atpg-benchmarks/results/screenshots/)), transcribed in [`atalanta_summary.csv`](../atpg-benchmarks/results/atalanta_summary.csv). The transcription was re-checked against pp. 4–6 during consolidation and matches.

### C7552 pattern counts in the observations table

| Field | Observations table (p. 7) | Atalanta screenshot (C7552, p. 4) |
|---|---|---|
| Compaction mode | NONE | `NONE` |
| Number of shuffles | 12 | not printed |
| Patterns before compaction | 216 | not printed; single count `Number of test patterns: 373` |
| Patterns after compaction | 117 | not printed |

216 / 117 / 12 are exactly C5315's values: a copy error between columns. The table also contradicts its own "NONE" entry. The C880 screenshot shows the next command as `atalanta -N -t c7552.test c7552.bench`, where `-N` disables compaction. **Used:** 373 patterns, uncompacted, no reduction figure.

### Discussion text on pattern counts

> "Pre-compaction test pattern counts were circuit size-dependent, ranging from 52 for the C6288 to 253 for the C3540." (p. 8)

This ignores C7552's 373 uncompacted patterns, and the counts do not track size. The post-compaction list "27, 54, 117, 153, and 117" does not follow the order in which the circuits are named and gives C7552 a compacted count. **Correct values:** C880 54, C3540 153, C5315 117, C6288 27.

### Discussion text on redundancy and effort

> "The number of redundant faults increased with circuit complexity …" / "The total backtracking count and CPU time also scaled with the size of the circuit." / "There is strong correlation between the measures of circuit complexity, fault coverage, and test pattern count." (pp. 8–9)

The data does not support these statements. C3540 (1,669 gates) has the most redundant faults (137). Backtracks and CPU time do not rise monotonically with gate count. Spearman ρ against gate count: 0.30 for redundant faults, 0.60 for backtracks, 0.40 for CPU time, −0.30 for fault coverage, and −0.40 for patterns (four compacted runs). None of these is "strong", and with n = 5 none is statistically meaningful. See [benchmark-results.md](benchmark-results.md#rank-correlation-with-gate-count).

### "Without compromising on coverage"

Each Atalanta summary prints one post-compaction coverage value, so the evidence has no measured before/after coverage pair. The claim is still correct by construction of REVERSE + SHUFFLE compaction, which drops a pattern only if it detects no new fault. It is stated on that basis.

### C6288 run provenance

The C7552 screenshot ends with the next command typed as `atalanta -t c6288.test -D 2 c6288.bench`. The `-D` mode generates *n* patterns per fault with no fault simulation, yet the C6288 summary shown next reports REVERSE + SHUFFLE compaction with 13 shuffles. It is also rendered differently (no banner or prompt), and its seed (1761820498) is outside the range of the other four runs (1762600250–1762601580). The command that produced it therefore cannot be identified. Its printed values are internally consistent: (7744 − 34) / 7744 = 99.561 %.

### Unrecorded assignment items

Items 2–5 of the Task 1 objective were not recorded: the `-D` N-detect mode, user fault lists, manual pattern files fault-simulated in Fsim, and the X/0/1 fill comparison. Their commands are listed (pp. 2–3), but no output exists, so no result is claimed.

### Minor items

- The procedure calls c880 an "ISCAS89" circuit (p. 2); it is ISCAS-85, and the commands use `iscas85/`.
- `fsim -s 9999 -r 20000 c432.bench` is described as "initialized by 20000"; `-s 9999` is the seed and `-r 20000` the pattern count (p. 3).
- `fsim -t c880.test iscas85/c880.bench` is described as using "c432.test" (p. 3).
- "Limit of suffling compaction" is the tool's own spelling.
- Pattern pairs such as "C880: 52 → 27", "C5315: 170 → 54" and "C6288: 52 → 117" are **not** supported by the report and are not used anywhere.

## Task 2: scan insertion on riscv_core

Values used: `scan.do` (p. 17) and the Tessent `insert_test_logic`, `report_test_logic`, `report_scan_chains` and `report_scan_cells` screenshots (p. 14).

| # | Item | Report text | Tool output / script | Resolution |
|---|---|---|---|---|
| 1 | Chain count in procedure | `add_scan_mode unwrapped -chain_count 4` (p. 11) | `-chain_count 5` in `scan.do`; 5 chains reported | **5** |
| 2 | Chains in the DRC analysis | "created 6 scan chains … ranging from 386 to 387 cells" (p. 11) | 5 chains, 464/464/464/464/463 | **5**. 3 × 387 + 3 × 386 = 2,319, so the text probably describes an earlier 6-chain trial with no surviving output |
| 3 | Netlist read | `read_verilog inserted.v` (p. 10) | `read_verilog netlist_riscvcore.v` | **`netlist_riscvcore.v`** |
| 4 | `analyze_drc_violation <drc_id>` | Listed (p. 11) | Not in `scan.do` | Treated as an interactive step; no output |
| 5 | DRC status | "After successfully clearing the DRC…" (p. 11) vs "Minor warnings (FN1, FN4, S7) need attention but don't stop the scan process" and "mostly DFT-clean" (p. 12) | No DRC output shown | **Unresolved.** FN1, FN4 and S7 are documented as open warnings; the design is **not** described as DFT-clean |
| 6 | "100 % scan insertion" | p. 13 | 4 × 464 + 463 = 2,319 cells in chains = 2,319 flip-flops in the text | Accepted as *consistent*, not proven: no Tessent non-scan count for `riscv_core` is shown |
| 7 | "Distribution … 100.0 % completed (estimate)" | — | Chain-allocation progress line | **Not** a coverage metric; never quoted as one |
| 8 | Gate count 34,714 | p. 12 | No tool output | Text only; the counting basis is unknown |
| 9 | Benefits of balancing ("less power", "reduced test time") | p. 13 | Nothing measured | General statements only; nothing measured is claimed |

## Task 3: Tessent ATPG

Values used: the Tessent `create_patterns`, `report_statistics` and `report_scan_volume` screenshots (pp. 19–21).

### The ATPG netlist is not the riscv_core scan netlist

The ATPG results **cannot be attributed to the 2,319-cell `riscv_core` scan netlist** produced in Task 2:

| Evidence | riscv_core scan netlist (Task 2) | ATPG runs (Task 3) |
|---|---|---|
| Netlist file | `riscv_scan.v` (written by `scan.do`) | `scan_inserted.v` (stuck-at); `LAB4/scan_inserted.v` (transition) |
| ATPG setup | `scan.*` from `write_atpg_setup scan` | `scan_inserted.dofile` |
| Chains × shift cycles | 5 × 464 | 6 × 22 (stuck-at); 5 × 26 (transition) |
| Scan cells (upper bound) | 2,319 | ≤ 132 (stuck-at); ≤ 130 (transition) |
| Gates | 34,714 (report text) | `#gates = 1158` (stuck-at); `1153` (transition) |
| Capture clock | `clk_i` | `blif_clk_net` |
| Lab directory (editor title bar) | `…/1.scan_insertion/LAB3` | `…/2.atpg/LAB4` |

Shift cycles per load equal the longest chain, so a netlist with 464-cell chains cannot report 22 or 26 shift cycles. Volume per load also matches the small configurations exactly: 132 = 6 × 22 and 130 = 5 × 26. The two ATPG runs also differ **from each other** in chain count, shift cycles and gate count. The QuestaSim signal prefix `riscv_core_seri…` suggests that the lab netlist's top module may also be named `riscv_core`, so it may be a reduced RISC-V netlist supplied for the lab. The report does not say, and this repository does not assume it.

**Consequence.** Scan-insertion results are reported for `riscv_core`. ATPG and pattern-simulation results are reported for "the lab scan netlist `scan_inserted.v`". No ATPG coverage exists for the 2,319-cell core.

### Report text vs tool output

| # | Item | Report text | Tool output | Resolution |
|---|---|---|---|---|
| 1 | Stuck-at fault coverage | 97.08 % (p. 15) | 97.82 % | (2273 + 955) / 3300 = 97.82 %; the text looks like a digit transposition |
| 2 | Stuck-at simulated patterns | 70 (p. 16) | 85 | 70 is the scan-load total (69 + 1 chain test) |
| 3 | Transition test patterns | 83 (p. 16) | 86 = 3 basic + 83 clock-sequential | Text quotes only the clock-sequential subset |
| 4 | Transition simulated patterns | 87 (p. 16) | 103 | 87 is the scan-load total (86 + 1) |
| 5 | Transition ATPG effectiveness | 100.00 % (p. 16) | 99.89 % | 3 aborted faults: (2690 − 3) / 2690 = 99.89 % |
| 6 | Transition "No. of Faults" | 1910 (p. 16) | FU = 2690; 1910 is the `#faults` count on the simulation line | 2690 − 775 (DI) − 5 (MPO) = 1910. The text gives the full universe for stuck-at (3300) but the simulated subset for transition |
| 7 | Total scan loads / volume | 11,318 (p. 16) | 11,310 | 87 × 5 × 26 = 11,310 |
| 8 | Scan volume scope | One volume presented | Transition run only; stuck-at is 6 chains, 22 shift cycles, 9,240 | Both are reported |
| 9 | CPU time 4.3 s | Presented as overall | Transition 4.3 s (4.4 s in a second printout); stuck-at 3.8 s | Each attributed to its own run |
| 10 | Tool name | "Tessent TestKompress" (p. 15) | Scripts use `set_context patterns -scan`; no EDT commands | Described as uncompressed scan ATPG in Tessent |
| 11 | "100 % test coverage … ensuring complete fault detection capability" (p. 16) | — | FC 97.82 %; 72 faults (UU + TI) not detected | Not repeated; TC and FC kept separate |

## Task 4: QuestaSim

| # | Item | Report text | Evidence | Resolution |
|---|---|---|---|---|
| 1 | Completeness | "Completed 50% of the fault simulation process" (p. 15); "analyzed partial results" and "Fault Simulation was completed successfully" (p. 22) | Two wave-window screenshots; no transcript, pass/mismatch count or coverage figure | **Unknown.** Described as pattern simulation of unproven completeness |
| 2 | "Fault simulation using QuestaSim … measure fault coverage" | p. 22 | Waveforms of the Tessent-generated testbenches; no fault injection visible | The coverage numbers come from Tessent's internal fault simulator, not QuestaSim |

## Inconsistencies between the three source repositories

Found while merging. None changes a number.

| # | Item | Resolution |
|---|---|---|
| 1 | `report_scan_cells` excerpt: "first 19 rows" (scan-insertion-tessent) vs "first 18 rows" (riscv-dft-atpg) | Both describe the same screenshot: 19 rows = 1 lockup latch (no cell number) + scan cells 0–17. Stated that way here |
| 2 | DRC status: "remaining warning; resolution not documented" vs "Status: Not stated" | Same meaning. Stated as "open, resolution not documented" |
| 3 | The old `vlsi-testing-atpg` README described the Tessent ATPG and QuestaSim work as being "on a RISC-V core" | Corrected: they ran on the lab netlist `scan_inserted.v` (see above) |
| 4 | QuestaSim screenshots described as "cropped" (riscv-dft-atpg README) and "reproduced uncropped" (its fault-simulation page) | They are the full wave windows as in the report; they contain no host or user information, so no crop was needed |
| 5 | "TessentScan" vs "Tessent Scan" | Normalised to "Tessent Scan" in prose. The report's spelling remains only in quotes |
| 6 | Two transcriptions each of `scan.do` and of the scan-insertion reports | Command lines and values are identical (checked by diff; only comments and whitespace differ). One copy of each is kept |

## Missing evidence

| Item | Experiment | Effect |
|---|---|---|
| `riscv_core` RTL, `syn.tcl`, Design Compiler logs | Scan insertion | Synthesis cannot be re-run; the gate count is text only |
| `netlist_riscvcore.v`, `riscv_scan.v`, ATPG setup `scan.*` | Scan insertion | Insertion cannot be re-run from this repository |
| `report_drc_rules` / `analyze_control_signals` / `report_scan_elements` output | Scan insertion | FN1/FN4/S7 counts and locations unknown |
| Full `report_scan_cells` | Scan insertion | Ordering of chains 1–4 unknown |
| `scan_inserted.v`, `scan_inserted.dofile` | Tessent ATPG | ATPG cannot be re-run |
| Pattern files (`serialpatterns.v`, `parallelpatterns.v`, `pattern.ascii`) | Tessent ATPG, QuestaSim | No pattern-level analysis is possible |
| QuestaSim transcript, compile and run commands | QuestaSim | Pass/fail of pattern simulation unknown |
| Atalanta `.test` files, fault lists, raw logs; any Fsim output | Benchmark ATPG | Only summary-level analysis is possible |
| ISCAS-85 `.bench` files | Benchmark ATPG | Public; not committed (see [`atpg-benchmarks/benchmarks/`](../atpg-benchmarks/benchmarks/README.md)) |

## Sanitisation

- Terminal screenshots were cropped to remove session tab bars (server hostname, user ID), file-browser sidebars (home-directory listings) and shell prompts.
- The editor screenshots of `atpg_1.do` and `atpg_2.do` were **not** reproduced, because their title bars show the server name and directory paths. The scripts were transcribed instead. The `scan.do` editor screenshot is kept cropped to the text area only.
- The relative paths inside the scripts (`LAB4/`, `LAB6/transition/`) are kept. They contain no user or host information.
- No licence-server address, credential, IP address, absolute library path or foundry library content appears in this repository. Only library and cell **names** (for example `tcbn65gplushpbwp.mdt`, `SDFCNQD1HPBWP`) are mentioned.
