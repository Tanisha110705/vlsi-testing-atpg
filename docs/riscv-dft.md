# RISC-V DFT: What the Evidence Supports

This page answers one question: **which parts of this portfolio are RISC-V work, and which are not?**

| Activity | On the RISC-V core `riscv_core`? | Evidence |
|---|---|---|
| Gate-level synthesis | Yes | Report text only |
| DFT rule checks | Yes | `scan.do`; findings in report text only |
| Scan insertion, stitching, balancing | **Yes** | `scan.do`; Tessent tool output with `riscv_core/…` instance paths |
| Stuck-at and transition ATPG | **Not shown.** It ran on the lab scan netlist `scan_inserted.v` | Chain/shift-cycle/gate counts in the ATPG logs |
| QuestaSim pattern simulation | **Not shown.** It ran on the ATPG patterns for that lab netlist | Waveform screenshots |
| ISCAS-85 benchmark ATPG | No | Separate combinational benchmarks |

So the RISC-V DFT evidence is the **scan insertion** documented in [`scan-insertion/`](../scan-insertion/). There is no ATPG coverage for the `riscv_core` scan netlist. The reasoning is in [evidence-audit.md](evidence-audit.md#the-atpg-netlist-is-not-the-riscv_core-scan-netlist).

## Design under test

![riscv_core scan architecture](../assets/riscv-core-scan-architecture.svg)

| Item | Value | Evidence |
|---|---|---|
| Top module | `riscv_core` | Tessent instance paths (p. 14) |
| Input netlist | `netlist_riscvcore.v` | `scan.do` (p. 17) |
| Visible sub-blocks | `u_issue` (with `u_pipe_ctrl`, `u_regfile`), `u_csr`, `u_mul`, `u_div` | `report_test_logic` (p. 14) |
| Clock | `clk_i`, rising edge for every visible scan cell | Text p. 11; `report_scan_cells` |
| Reset | `rst_i` | Text p. 11 only |
| Sequential cells | 2,319 | Text p. 12; equals the chain total |
| Gates | 34,714 | Text p. 12 only |
| Technology | TSMC 65 nm; Tessent library `tcbn65gplushpbwp.mdt` | Text; scripts |

The block names come from instance names (`u_mul` multiplier, `u_div` divider, `u_csr` control/status registers, `u_issue/u_pipe_ctrl` pipeline control, `u_issue/u_regfile` register file). They have not been checked against RTL. Register names such as `u_div/dividend_q_reg[31:16]` and `u_div/quotient_q_reg[…]` indicate a divider with dividend and quotient registers; nothing further is inferred.

**Not available:** the RTL, which RISC-V core this is (in-house or open-source), its ISA subset, its micro-architecture and its functional port list. The report does not name the core, and this repository does not guess.

## Scan configuration

| Item | Value | Evidence |
|---|---|---|
| Scan mode | `unwrapped` (internal chains only, no wrapper chains) | `scan.do`, tool output |
| Chains | 5: `chain0`–`chain4`, lengths 464 / 464 / 464 / 464 / 463 | `report_scan_chains` |
| Scan cell | `SDFCNQD1HPBWP` (mux-scan DFF with active-low clear) | `report_scan_cells` (visible rows) |
| Added ports | `ts_si[4:0]`, `ts_so[4:0]`, `scan_en` | `report_test_logic` |
| Added instances | 5 lockup latches `LNQD4HPBWP`, 5 buffers `CKBD2HPBWP` | `report_test_logic` |
| Shift cycles per load | 464 | Derived (longest chain) |

Details: [scan-insertion.md](scan-insertion.md).

## Functional and test modes

| Mode | `scan_en` | Flip-flop D source | Purpose |
|---|---|---|---|
| Functional | de-asserted | combinational logic | normal operation |
| Shift | asserted | previous scan cell (`SI`) | load stimulus through `ts_si`, unload response through `ts_so` |
| Capture | de-asserted for one pulse (stuck-at) or launch + capture (broadside transition) | combinational logic | record the logic's response |

None of these modes was simulated on `riscv_core`.

## ATPG setup

`scan.do` ends with `write_atpg_setup scan -replace`, which writes the dofile and test procedure needed to run ATPG on `riscv_scan.v`. Neither file is preserved, and **no ATPG run read them**:

| | riscv_core (from `scan.do`) | Recorded ATPG runs |
|---|---|---|
| Netlist | `riscv_scan.v` | `scan_inserted.v`, `LAB4/scan_inserted.v` |
| Setup | `scan.*` | `scan_inserted.dofile` |
| Chains × shift cycles | 5 × 464 | 6 × 22 and 5 × 26 |
| Gates seen by ATPG | — | 1,158 and 1,153 |
| Capture clock | `clk_i` | `blif_clk_net` |

The QuestaSim signal names begin with `riscv_core_seri…`, so the lab netlist may also have a top module called `riscv_core`, perhaps a reduced RISC-V netlist supplied for the lab. The report does not say. Its ATPG results are documented in [`tessent-atpg/`](../tessent-atpg/) as results for the lab netlist only.

## Results attributable to riscv_core

| Metric | Value | Evidence |
|---|---|---|
| Scan chains | 5 | Tool |
| Chain lengths | 464 / 464 / 464 / 464 / 463 | Tool |
| Scan cells in chains | 2,319 | Derived (4 × 464 + 463) |
| Flip-flops | 2,319 | Text (consistent with the above) |
| Chain spread | 1 cell (arithmetic optimum) | Derived |
| Added ports / instances / retiming latches | 3 / 10 / 5 | Tool |
| DRC warnings | FN1, FN4, S7, open | Text |
| Stuck-at or transition coverage | **None exists** | — |

## What would complete the RISC-V DFT flow

Not implemented:

1. Run [`atpg_1.do`](../tessent-atpg/scripts/atpg_1.do) and [`atpg_2.do`](../tessent-atpg/scripts/atpg_2.do) with `read_verilog riscv_scan.v` and `dofile` pointed at the `scan` setup from `write_atpg_setup`. The numbers would be new results, not reproductions.
2. Archive `report_drc_rules` and resolve FN1/FN4/S7.
3. Run a formal equivalence check between `netlist_riscvcore.v` and `riscv_scan.v` in functional mode.
4. Simulate the chain test and a few serial patterns on `riscv_scan.v` and keep the transcript with its mismatch count.
5. Add EDT compression; 464-cycle loads are long without it.
