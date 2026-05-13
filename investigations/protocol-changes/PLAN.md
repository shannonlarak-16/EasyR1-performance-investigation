# Performance Analysis: Protocol Changes Investigation

This document tracks the investigation of performance regressions potentially introduced by commit `098931530606d22f867fd121b1dcb3225a43661f` ("[misc] fix data proto (#458)") in `verl/protocol.py`.

## Hypothesis

The default value of `non_blocking` in `DataProto.to()` was flipped from `True` to `False`, forcing synchronous host<->device copies and stalling the GPU on every offload step.

## Affected Files (from commit `098931530606d22f867fd121b1dcb3225a43661f`)

| File | Changes |
|------|---------|
| `verl/protocol.py` | +6 / -4 - default `non_blocking=False` |
| `examples/config.yaml` | +2 / -2 - defaults paired with offload |

## Test Plan

### 1. Micro-benchmark (`DataProto.to`)
- Allocate a 1 GB `DataProto` on CPU
- Time `data.to('cuda', non_blocking=True)` vs `non_blocking=False` x 1000 iterations
- Expected: `non_blocking=False` is 2-5x slower because each transfer serializes a CUDA event

### 2. End-to-end GRPO step
- Reproduce the configuration reported in upstream issue #39:
  - Qwen2.5-VL-7B
  - 8 images per sample, 800 samples x 10 epochs
  - 8 x A100 80 GB, `tensor_parallel_size=2`
  - `worker.actor.offload.offload_params=true`, `worker.actor.offload.offload_optimizer=true`
- Compare:
  - `HEAD~1` (parent of commit `098931530606d22f867fd121b1dcb3225a43661f`)
  - `HEAD` (commit `098931530606d22f867fd121b1dcb3225a43661f`)
  - `HEAD` with a one-line revert restoring `non_blocking=True`

### 3. Profiling
- Run `nvidia-smi dmon -s u` to capture GPU utilization
- Run `nsys profile` for one global step to confirm the GPU stall pattern

## Acceptance Criteria

- [ ] Demonstrate >=1.5x wall-clock improvement when restoring `non_blocking=True` on the issue-#39 workload
- [ ] Confirm correctness (no NaNs, identical converged loss) when flipping back
- [ ] Update sub-issue #4 with measurements
- [ ] If confirmed, propose either:
  - (a) Restore `non_blocking=True` and add explicit `torch.cuda.synchronize()` only where required
  - (b) Make the default configurable via `examples/config.yaml`

## Related

- Tracking issue #1 - Performance Regression Analysis: Data Protocol Changes
- Sub-issue #4 - Test Performance Impact: non blocking false by default
- Upstream commit: https://github.com/hiyouga/EasyR1/commit/098931530606d22f867fd121b1dcb3225a43661f
- Upstream user reports: hiyouga/EasyR1#39, hiyouga/EasyR1#41
