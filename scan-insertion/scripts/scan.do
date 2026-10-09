// =============================================================================
// scan.do - Tessent Scan scan-insertion dofile for riscv_core
// -----------------------------------------------------------------------------
// Provenance : transcribed verbatim from the screenshot of scan.do in the
//              course report (Appendix, page 17). The command lines are
//              unchanged; only these "//" comments were added.
//              Screenshot: scan-insertion/results/screenshots/scan-do-script.png
// Tool       : Siemens (Mentor) Tessent Scan, dft -scan context
// Inputs     : netlist_riscvcore.v      gate-level netlist from Design Compiler
//              tcbn65gplushpbwp.mdt     TSMC 65 nm Tessent cell library
// Outputs    : riscv_scan.v             scan-inserted netlist
//              scan.*                   ATPG setup (dofile + test procedure)
// Requires access to the corresponding licensed EDA environment and
// technology libraries. Neither input file is included in this repository.
// =============================================================================

// Enter the DFT context for scan insertion.
set_context dft -scan

// Load the synthesized netlist and the DFT view of the standard-cell library.
read_verilog netlist_riscvcore.v
read_cell_library tcbn65gplushpbwp.mdt
set_current_design

// Identify clocks/resets/sets and add control logic where they are not
// controllable from primary inputs in test mode.
analyze_control_signals -auto_fix

// Run DFT design-rule checks and list the rules / scannable elements.
check_design_rules
report_drc_rules
report_scan_elements

// Define a single (unwrapped) scan mode with 5 chains, then plan and stitch them.
add_scan_mode unwrapped -chain_count 5
analyze_scan_chains
insert_test_logic

// Report inserted test logic, chain summary, and per-cell chain membership.
report_test_logic
report_scan_chains
report_scan_cells

// Write the scan-inserted netlist and the ATPG setup files for Tessent ATPG.
write_design -output_file riscv_scan.v -replace
write_atpg_setup scan -replace
