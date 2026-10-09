# Atalanta Commands

These commands are as documented in the original assignment procedure. The table marks which ones produced the results in this repository.

## Test generation

| Command | Effect | Used for recorded results |
|---|---|---|
| `atalanta -t c880.test iscas85/c880.bench` | RPT + DTPG + TC with REVERSE + SHUFFLE compaction; write the test set to `c880.test` | C880, C3540, C5315 (and C6288; see note) |
| `atalanta -N -t c7552.test c7552.bench` | Same, with compaction disabled | C7552 |
| `atalanta -t c880.test -D 2 c880.bench` | Generate *n* = 2 tests per fault; unspecified inputs left as X; no fault simulation | No results recorded |
| `atalanta -A -f c880.flt iscas85/c880.bench` | Read the fault list from `c880.flt`; generate all tests for each fault | No results recorded |

## Unspecified-input fill

| Option | Unspecified inputs set to |
|---|---|
| `-0` | logic 0 |
| `-1` | logic 1 |
| `-R` | random 0/1 |
| `-X` | left unknown (X) |

The assignment asked for a comparison of fill modes. No results were recorded.

## Fault simulation (Fsim)

```sh
fsim -s 9999 -r 20000 c432.bench > c432.out   # random-pattern fault simulation
fsim -t c880.test iscas85/c880.bench          # fault-simulate an existing test set
```

No Fsim results were recorded.

## Parameters reported in all compacted runs

| Parameter | Value |
|---|---|
| Limit of random patterns (packets) | 16 |
| Backtrack limit | 10 |
| Compaction mode | REVERSE + SHUFFLE |
| Limit of shuffling compaction | 2 |

The exact command behind the recorded C6288 summary cannot be identified; see [`docs/evidence-audit.md`](../docs/evidence-audit.md#c6288-run-provenance).
