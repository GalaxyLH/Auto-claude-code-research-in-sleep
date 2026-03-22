# Findings

> **Lightweight cross-stage discovery log.** Record non-obvious things you learn during experiments — anomalies, debug root causes, key decisions. This is NOT for formal results (use `EXPERIMENT_LOG.md`) or review feedback (use `AUTO_REVIEW.md`).
>
> **Why this file exists:** Experiments constantly produce small but important discoveries (a hyperparameter that's surprisingly sensitive, a loss combination that behaves unexpectedly, a baseline that's harder to reproduce than expected). Without a central log, these get lost in chat history or scattered across tool outputs — and the next session repeats the same mistakes.
>
> **Format:** Append new entries at the top (newest first). Keep each entry to 2-3 lines. This file is read on session recovery, so keep it lean.

## [YYYY-MM-DD] Topic
- Discovery or decision
- Related files / commands / evidence

## [YYYY-MM-DD] Example: Unexpected lr sensitivity
- lr=1e-4 diverges on dataset-X but works on dataset-Y; switched to 5e-5 for all
- See wandb run abc123, step 2000-3000

## [YYYY-MM-DD] Example: Baseline reproduction gap
- Paper reports 95.5 on dataset-X but we get 93.2 with their official code
- Root cause: different data preprocessing (center crop vs resize)
- Decision: use our preprocessing for fair comparison, note in paper

## [YYYY-MM-DD] Example: Debug root cause
- OOM on batch_size=32 with 4x GPU — traced to gradient accumulation doubling memory
- Fix: gradient checkpointing enabled, batch_size=32 now fits
