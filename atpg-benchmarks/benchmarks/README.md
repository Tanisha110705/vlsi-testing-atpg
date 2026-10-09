# Benchmark Circuits

The five circuits are from the **ISCAS-85** combinational benchmark suite, in the `.bench` netlist format that Atalanta reads.

| Circuit | Netlist file | Function (Hansen, Yalcin & Hayes, 1999) |
|---|---|---|
| C880  | `c880.bench`  | 8-bit ALU |
| C3540 | `c3540.bench` | 8-bit ALU with BCD arithmetic |
| C5315 | `c5315.bench` | 9-bit ALU |
| C6288 | `c6288.bench` | 16 × 16 multiplier |
| C7552 | `c7552.bench` | 32-bit adder / comparator |

**The netlists are not stored in this repository.** The original runs used copies from the lab environment (an `iscas85/` directory), and those copies were not preserved. The ISCAS-85 netlists are publicly distributed benchmark data; obtain them from a benchmark archive or the examples shipped with Atalanta. Before comparing results, check that a copy's gate and I/O counts match the table in [`docs/benchmark-results.md`](../../docs/benchmark-results.md#benchmark-circuits).

## `.bench` format (example)

```
INPUT(1)
INPUT(2)
OUTPUT(22)
10 = NAND(1, 3)
22 = NAND(10, 16)
```

Each line declares a primary input, a primary output, or a gate (`AND`, `NAND`, `OR`, `NOR`, `XOR`, `XNOR`, `NOT`, `BUFF`) with its fan-in. The example shows the syntax only and is a fragment of no particular benchmark.
