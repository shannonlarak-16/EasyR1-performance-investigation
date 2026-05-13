# EasyR1 - Performance Investigation Workspace

This repository is a dedicated workspace for investigating potential performance regressions introduced by commit [`098931530606d22f867fd121b1dcb3225a43661f`](https://github.com/hiyouga/EasyR1/commit/098931530606d22f867fd121b1dcb3225a43661f) ("[misc] fix data proto (#458)") in [hiyouga/EasyR1](https://github.com/hiyouga/EasyR1).

## Context
Upstream commit `098931530606d22f867fd121b1dcb3225a43661f` touched 5 files (22 line changes):
- `verl/protocol.py` (+6/-4)
- `examples/config.yaml` (+2/-2)
- `examples/qwen2_5_vl_32b_geo3k_grpo.sh` (-2)
- `verl/trainer/ray_trainer.py` (+2/-2)
- `verl/workers/fsdp_workers.py` (+1/-1)

## Investigation Tracks
| Branch | Focus |
|--------|-------|
| `investigate-protocol-changes` | Protocol-related perf issues |
| `investigate-batch-processing` | Batch processing perf issues |
| `investigate-memory-usage` | Memory utilization perf issues |

See tracking issue for details.
