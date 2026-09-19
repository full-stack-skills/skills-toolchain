## Why

公开文档仍把多宿主消费方称为 Codex 插件，并引用已经不存在的 `codex-stitch-plugin` 路径，容易让用户误以为工具链只适配单一宿主。

## What Changes

- 明确列出 Codex、ZCode、Kimi 与 WorkBuddy 消费方。
- 将过时仓库名替换为当前的 `stitch-design-plugin`。
- 让通知工作流从受审查的 consumer 清单读取当前仓库身份。
- 禁止发布工作流强制移动版本 tag，并补正式 GitHub Release。
- 加固同步模板的远程分支获取与无标签 PR 创建。
- 按 TRACE 补齐 overview skill 的边界、流程、验证与失败处理。

## Capabilities

### New Capabilities

- `host-neutral-documentation`: 工具链公共文档使用当前、宿主中立的消费方身份。
- `immutable-toolchain-release`: 工具链发布 tag 不可移动，并具有一致的 Release 证据。
