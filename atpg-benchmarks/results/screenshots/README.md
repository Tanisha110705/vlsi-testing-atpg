# Evidence: Atalanta summary screenshots

This folder holds the five Atalanta "SUMMARY OF TEST PATTERN GENERATION RESULTS" screens. They are the primary evidence for every number in the `atpg-benchmarks` module.

| File | Circuit | Compaction |
|---|---|---|
| `c880_atalanta_summary.png`  | C880  | REVERSE + SHUFFLE |
| `c3540_atalanta_summary.png` | C3540 | REVERSE + SHUFFLE |
| `c5315_atalanta_summary.png` | C5315 | REVERSE + SHUFFLE |
| `c6288_atalanta_summary.png` | C6288 | REVERSE + SHUFFLE |
| `c7552_atalanta_summary.png` | C7552 | NONE |

## How they were prepared
- Extracted at native resolution from the embedded images of the original course report (Task 1).
- **Cropped only.** The tool banner above the summary and the shell prompt below it were removed, because the prompt showed a user ID and a lab server hostname. No pixel inside the summary was altered. The C6288 image had no banner or prompt and is unmodified.
- The commands visible in the removed prompt lines are documented in [`docs/evidence-audit.md`](../../../docs/evidence-audit.md#task-1-iscas-85-benchmark-atpg-atalanta): `atalanta -N -t c7552.test c7552.bench` after C880, and `atalanta -t c6288.test -D 2 c6288.bench` after C7552.

## Transcription
All values were transcribed to [`../atalanta_summary.csv`](../atalanta_summary.csv) and checked digit by digit against these images. [`derive_metrics.py`](../../scripts/derive_metrics.py) then confirms that the transcribed fault counts reproduce each reported coverage value.

The original report is not included, because it contains personal and institutional information.
