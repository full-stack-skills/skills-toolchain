## Decision

保留确实指向特定宿主的产品名称，但移除把跨宿主插件错误命名为 Codex 专属插件的表述和仓库路径。

consumer 身份只维护在 `docs/CONSUMERS.md`，通知工作流不再复制一份容易漂移的硬编码列表。版本 tag 一旦存在于不同 commit，发布必须失败并要求提升版本。
