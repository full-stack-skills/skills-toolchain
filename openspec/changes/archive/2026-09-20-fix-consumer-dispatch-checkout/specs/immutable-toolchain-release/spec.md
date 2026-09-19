## MODIFIED Requirements

### Requirement: Toolchain release evidence is complete
每个工具链版本 MUST 具有同名 Git tag 与 GitHub Release；下游通知 MUST checkout 后从受审查的 consumer 清单读取当前仓库身份，MUST 尝试全部目标，并在任一目标失败时报告失败。

#### Scenario: New version is published
- **WHEN** 新版本进入主分支且版本 tag 尚不存在
- **THEN** 工作流创建不可变 tag、GitHub Release，并尝试向清单中的每个当前仓库发送 dispatch
