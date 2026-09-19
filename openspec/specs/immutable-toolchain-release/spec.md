# immutable-toolchain-release Specification

## Purpose
TBD - created by archiving change remove-stale-host-prefixes. Update Purpose after archive.
## Requirements
### Requirement: Published toolchain tags are immutable
发布工作流 MUST NOT 移动已经存在的版本 tag；同一 tag 指向不同 commit 时 MUST 失败并要求提升版本。

#### Scenario: Existing tag differs from main
- **WHEN** 当前版本 tag 已存在且不指向待发布 commit
- **THEN** 工作流失败且不覆盖远程 tag

### Requirement: Toolchain release evidence is complete
每个工具链版本 MUST 具有同名 Git tag 与 GitHub Release，并且下游通知 MUST 从受审查的 consumer 清单读取当前仓库身份。

#### Scenario: New version is published
- **WHEN** 新版本进入主分支且版本 tag 尚不存在
- **THEN** 工作流创建不可变 tag、GitHub Release，并向清单中的当前仓库发送 dispatch

