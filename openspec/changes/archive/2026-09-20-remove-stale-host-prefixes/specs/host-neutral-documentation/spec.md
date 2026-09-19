## ADDED Requirements

### Requirement: Public identities are host-neutral
跨宿主工具链文档 MUST 使用当前仓库名，并且 MUST NOT 用单一宿主前缀命名跨宿主插件。

#### Scenario: User follows a consumer reference
- **WHEN** 用户阅读工具链 README 或 overview skill
- **THEN** 文档列出支持的宿主并引用当前可用的仓库路径
