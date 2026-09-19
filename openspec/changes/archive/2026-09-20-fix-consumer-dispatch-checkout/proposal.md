## Why

真实 `v1.0.1` 发布运行证明通知工作流没有 checkout，因此无法读取 consumer 清单；逐个 dispatch 还会在首个失败处提前退出。

## What Changes

- checkout 仓库后再读取 `docs/CONSUMERS.md`。
- 尝试所有 consumer 并汇总失败状态。
- 提升版本到 `1.0.2`，保持 `v1.0.1` 不变。

## Capabilities

### Modified Capabilities

- `immutable-toolchain-release`: 发布后的 consumer 通知可读取受审查清单并提供完整失败证据。
