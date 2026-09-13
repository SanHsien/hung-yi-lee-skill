# CLAUDE.md

請先完整閱讀並遵守 [`AGENTS.md`](AGENTS.md)。本檔只補充 Claude Code 的最小入口：

- 這是保留上游歷史的 fork；不要移除 `upstream`、原作者或 MIT License 授權標示。
- 核心腳本在 `scripts/`、知識庫在 `wiki/` 與 `raw/`，以上游為準。
- 提交前跑 `pwsh -NoProfile -File tools\dev_check.ps1`。不要把 gate 改成完整產品依賴安裝。
- 測試檔案、使用者專有文件、`.env` 一律不可提交。
- 使用繁體中文，直接交付可驗證結果，避免冗長背景鋪陳。
- PR、push、release 一律指向 `SanHsien/hung-yi-lee-skill`，嚴禁未經當次許可打向 `voidful/hung-yi-lee-skill`。
