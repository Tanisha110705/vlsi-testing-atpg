// =============================================================================
// atpg_1.do - Tessent ATPG, stuck-at fault model
// -----------------------------------------------------------------------------
// Provenance : transcribed verbatim from the screenshot of atpg_1.do in the
//              course report (Appendix, page 17). The command lines, and the
//              two original "//" comments marked [original], are unchanged;
//              the other comments were added for documentation.
// Tool       : Siemens Tessent (patterns -scan context; the report names the
//              product as Tessent TestKompress)
// Inputs     : scan_inserted.v          scan-inserted gate-level netlist
//              scan_inserted.dofile     ATPG setup written by scan insertion
//              tcbn65gplushpbwp.mdt     TSMC 65 nm Tessent cell library
// Outputs    : serialpatterns.v, parallelpatterns.v (Verilog testbenches)
//              pattern.ascii            (ASCII pattern file)
//
// NOTE: this script reads scan_inserted.v, not riscv_scan.v (the file written
// by scan-insertion/scripts/scan.do). The ATPG log reports 6 scan chains / 22 shift
// cycles, which does not match the 5 x 464 riscv_core chains.
// See docs/evidence-audit.md.
// Requires access to the corresponding licensed EDA environment and
// technology libraries.
// =============================================================================

set_context patterns -scan
read_verilog scan_inserted.v
read_cell_library tcbn65gplushpbwp.mdt
set_current_design
// Read atpg setup                                          [original]
dofile scan_inserted.dofile
tessent_scan_setup

// Leave setup mode: run rule checks and build the simulation model.
set_system_mode analysis
// Pattern generation, default is stuck-at                  [original]
add_faults -all
create_patterns

// Serial testbench shifts every scan bit; parallel testbench force-loads
// the scan cells (faster simulation); ASCII is the tool-neutral pattern file.
write_patterns serialpatterns.v -verilog -serial -replace
write_patterns parallelpatterns.v -verilog -parallel -replace
write_patterns pattern.ascii -ascii -parallel -replace
report_scan_volume
