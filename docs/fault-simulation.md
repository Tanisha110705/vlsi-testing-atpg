# Fault Simulation and Pattern Simulation

Module: [`fault-simulation/`](../fault-simulation/).

"Fault simulation" means three different activities in the source material. They answer different questions, and only the first two produced numbers.

| # | Simulator | Design | What it does | Produces coverage? | Evidence |
|---|---|---|---|---|---|
| 1 | Atalanta built-in (PPSFP) | ISCAS-85 benchmarks | Fault-simulates random and FAN patterns, drops detected faults, drives compaction | **Yes**: Atalanta fault coverage | Tool (CPU time and coverage in each summary) |
| 2 | Tessent internal, inside `create_patterns` | Lab scan netlist `scan_inserted.v` | Fault-simulates candidate patterns, drops detected faults | **Yes**: every Tessent TC/FC/AE value | Tool (`report_statistics`) |
| 3 | Siemens QuestaSim | Lab scan netlist + Tessent pattern testbenches | Gate-level simulation of `serialpatterns.v` / `parallelpatterns.v`; compares scan-out with ATPG-expected values | **No**: validates patterns against the fault-free circuit only | Two waveform screenshots |
| — | Fsim (standalone) | ISCAS-85 | Listed in the Task 1 procedure | — | **No output recorded** |

## Principle

```text
pattern ─┬─► fault-free circuit ──► expected response ─┐
         │                                             ├─► differ at an observed point? ─► fault detected, drop it
         └─► circuit with fault f ─► faulty response ──┘
```

A pattern detects a fault when good and faulty circuits differ at an observed point: a primary output, or, in a scan design, a scan cell captured and shifted out. *Fault dropping* removes a detected fault so later patterns are not spent on it.

## 1. Atalanta (benchmarks)

Parallel-pattern single-fault propagation (PPSFP), per the Atalanta documentation. It runs in three places: on RPT packets, after each FAN test, and in every reverse/shuffle compaction pass. Each summary reports its CPU time separately:

| Circuit | Fault simulation (s) [R] | Share of total CPU [D] |
|---|---:|---:|
| C880  | 0.000 | — (total 0.000) |
| C3540 | 0.567 | 97 % |
| C5315 | 0.083 | 83 % |
| C6288 | 0.300 | 100 % |
| C7552 | 0.050 | 13 % |

Times have about 16.7 ms resolution. C7552 is the only run where FAN search, not fault simulation, dominates.

**Fsim.** The procedure lists `fsim -s 9999 -r 20000 c432.bench > c432.out` and `fsim -t c880.test iscas85/c880.bench`. No Fsim output was recorded, so no independent cross-check of Atalanta's coverage exists.

## 2. Tessent internal fault simulation (lab scan netlist)

Each candidate pattern is simulated on the good circuit and against the faults still in the list. Faults proven detected without simulation (DI) and structurally untestable faults (UU, TI) are classified first, which is why the log's simulation fault list is smaller than the universe:

| Run | Universe (FU) | Pre-classified | Faults simulated (log `#faults`) | Faults left at end |
|---|---:|---|---:|---:|
| Stuck-at | 3,300 | DI 955, UU 6, TI 66 | 2,273 | 0 |
| Transition | 2,690 | DI 775, MPO 5 | 1,910 | 3 (aborted) |

The "pre-classified" reconciliation is arithmetic [D]; Tessent does not print it. Both runs reached completion, with the final rows showing 0 and 3 faults left. Results: [tessent-atpg.md](tessent-atpg.md).

## 3. QuestaSim pattern simulation

```text
lab scan netlist ───────────────┐
TSMC 65 nm Verilog cell models ─┼─► QuestaSim ─► compare simulated scan-out with ATPG-expected values
serial/parallel testbench ──────┘                (fault-free reference)
```

**Purpose:** confirm independently that the patterns behave on the netlist as Tessent predicted (correct shift, correct capture, no X or timing-model mismatch). A mismatch would mean the patterns fail a good chip on the tester. The report's Task 4 objective speaks of "simulating both stuck-at and transition faults" and "measure fault coverage", but no fault injection is visible. **QuestaSim produced no coverage number here.**

| Run | Screenshot | What is visible |
|---|---|---|
| Stuck-at patterns | [questasim-stuck-at-pattern-sim.png](../fault-simulation/results/screenshots/questasim-stuck-at-pattern-sim.png) | Wave window with about 30 signals, all truncated to `riscv_core_seri…`; bus values that step 3, 4, 5 … 18 (probably pattern or cycle counters); `Now` 461,170 ns, cursor 387,760 ns |
| Transition patterns | [questasim-transition-pattern-sim.png](../fault-simulation/results/screenshots/questasim-transition-pattern-sim.png) | Same structure; counters stepping 1 … 11; cursor 313,263.08 ns; value column shows `-No Data-` at the cursor |

The truncated prefix suggests the serial-pattern testbench. The signal names are cut off, so individual signals (`scan_en`, scan inputs and so on) cannot be identified, and no claim is made about them.

**Completeness:** the report says "Completed 50% of the fault simulation process" (p. 15), "analyzed partial results" and "Fault Simulation was completed successfully" (p. 22). No transcript, mismatch count or pass message is shown. **Whether the simulations ran over all patterns, and whether any mismatches occurred, is not evidenced.** This repository does not claim complete or error-free pattern simulation.

## How a complete QuestaSim run would be documented (future work)

- The simulator compile and run commands and the cell-model library used.
- The transcript ending with the testbench's mismatch count (Tessent Verilog testbenches report mismatches at the end of simulation).
- A serial run (at least the chain test plus a few patterns) and a parallel run (all patterns).
- For actual fault-coverage cross-checks: a fault simulator with fault injection, or Fsim on the benchmark `.test` files.
