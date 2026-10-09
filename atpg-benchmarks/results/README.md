# Results Data

## `atalanta_summary.csv`: transcribed tool output

One row per circuit. Each value is copied from the matching screenshot in [`screenshots/`](screenshots/). An empty cell means Atalanta did not print that field for that run.

| Column | Atalanta summary field |
|---|---|
| `circuit` | Name of the circuit |
| `primary_inputs`, `primary_outputs` | Number of primary inputs / outputs |
| `gates`, `levels` | Number of gates / Level of the circuit |
| `tpg_mode` | Test pattern generation mode |
| `random_pattern_limit_packets` | Limit of random patterns (packets) |
| `backtrack_limit` | Backtrack limit |
| `rng_seed` | Initial random number generator seed |
| `compaction_mode` | Test pattern compaction mode |
| `shuffle_limit` | Limit of suffling compaction *(tool's spelling)* |
| `shuffles` | Number of shuffles |
| `patterns_before_compaction`, `patterns_after_compaction` | Number of test patterns before / after compaction |
| `patterns_uncompacted_run` | Number of test patterns (printed only when compaction is NONE) |
| `fault_coverage_pct` | Fault coverage (%) |
| `collapsed_faults` | Number of collapsed faults |
| `redundant_faults` | Number of identified redundant faults |
| `aborted_faults` | Number of aborted faults |
| `backtracks` | Total number of backtrackings |
| `memory_kb` | Memory used (Kbytes) |
| `cpu_init_s`, `cpu_fault_sim_s`, `cpu_fan_s`, `cpu_total_s` | CPU time: Initialization / Fault simulation / FAN / Total (s) |
| `evidence` | Screenshot the row was transcribed from (path relative to `atpg-benchmarks/`) |

## `derived_metrics.csv`: generated

Written by [`../scripts/derive_metrics.py`](../scripts/derive_metrics.py). Do not edit by hand.

| Column | Formula |
|---|---|
| `detected_faults_derived` | collapsed − redundant − aborted |
| `fault_coverage_pct_recomputed` | 100 × detected / collapsed (checked equal to the reported value) |
| `coverage_excl_redundant_pct_derived` | 100 × detected / (collapsed − redundant) |
| `fault_efficiency_pct_derived` | 100 × (detected + redundant) / collapsed |
| `pattern_reduction_pct_derived` | 100 × (before − after) / before, only where both counts are reported |

## `rank_correlation_vs_gates.csv`: generated

Spearman rank correlation of each measure against gate count. Descriptive only (n = 5, or 4 for compaction-dependent measures).
