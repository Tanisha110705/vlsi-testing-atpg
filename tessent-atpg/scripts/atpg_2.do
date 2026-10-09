// =============================================================================
// atpg_2.do - Tessent ATPG, transition (delay) fault model
// -----------------------------------------------------------------------------
// Provenance : transcribed verbatim from the screenshot of atpg_2.do in the
//              course report (Appendix, page 18). The command lines, and the
//              two original "//" comments marked [original], are unchanged;
//              the other comments were added for documentation.
// Tool       : Siemens Tessent (patterns -scan context)
// Inputs     : LAB4/scan_inserted.v, LAB4/scan_inserted.dofile,
//              tcbn65gplushpbwp.mdt (TSMC 65 nm Tessent cell library)
// Outputs    : LAB6/transition/serialpatterns.v, parallelpatterns.v,
//              pattern.ascii
//
// NOTE: the ATPG log for this run reports 5 scan chains / 26 shift cycles,
// which does not match the 5 x 464 riscv_core chains, and differs from the
// stuck-at run (6 chains / 22 shift cycles). See docs/evidence-audit.md.
// Requires access to the corresponding licensed EDA environment and
// technology libraries.
// =============================================================================

set_context patterns -scan
read_verilog LAB4/scan_inserted.v
read_cell_library tcbn65gplushpbwp.mdt
set_current_design
// Read atpg setup                                          [original]
dofile LAB4/scan_inserted.dofile
tessent_scan_setup

set_system_mode analysis
// Pattern generation, default is stuck-at                  [original]
add_faults -all
// Switch the fault model to transition (slow-to-rise / slow-to-fall).
// The log shows the transition fault universe (2690 faults) was targeted.
set_fault_type transition
report_statistics
// The tool log shows create_patterns then applying: set_transition_holdpi on,
// set_output_masks on, and set_pattern_type -sequential 2 (broadside
// launch-off-capture needs a sequential depth of at least 2).
create_patterns
write_patterns LAB6/transition/serialpatterns.v -verilog -serial -replace
write_patterns LAB6/transition/parallelpatterns.v -verilog -parallel -replace
write_patterns LAB6/transition/pattern.ascii -ascii -parallel -replace
report_scan_volume
