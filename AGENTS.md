# AGENTS.md

給 Codex、Claude Code、Cursor、Antigravity 與其他自動化代理在本專案工作時的指引。產品與使用方式先讀 [`README.md`](README.md)；開發與驗收細節見 [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)。

## 專案定位

這是 [`voidful/hung-yi-lee-skill`](https://github.com/voidful/hung-yi-lee-skill) 的 MIT License fork。
核心價值是李宏毅老師 AI/ML 課程知識庫、教學風格 DNA、916 節點知識圖譜與 Agent Skill。

`origin` 是 `SanHsien/hung-yi-lee-skill`（預設分支 `main`），`upstream` 是原作者 repo（預設分支 `main`）。
保留上游作者、MIT License 與產品程式。本 fork 的維護差異記在 [`FORK.md`](FORK.md) 與 [`docs/DECISIONS.md`](docs/DECISIONS.md)。

主要開發與完整驗收環境是 **Windows 11 + PowerShell**。本 fork 為純 Windows 維護線，所有測試與工作流程均在 Windows 原生環境執行。

## 硬性邊界

- 不提交使用者輸入檔案、專有文件、API key、token、私鑰或 `.env`。
- 不推送到 `upstream`。上游同步先跑 `python tools/check_upstream_updates.py`，逐筆審查後再 merge / cherry-pick；不盲目覆蓋 fork 文件與 Windows gate。
- 不要把維護 gate 改成完整產品依賴安裝。維護環境（`requirements-dev.txt`）僅安裝 pytest 與 ruff。
- 不把 fork 包裝成原創產品，不移除上游作者、李宏毅老師或官方連結。

## 技術與資料流

- 核心腳本：`scripts/hungyi_kb.py`（知識庫 CLI、抓取、編譯、搜尋、分析）、`scripts/hungyi_graph.py`（知識圖譜引擎）。
- 原始資料：`raw/youtube/`（頻道清單、逐字稿快取）。
- 知識庫：`wiki/`（索引、主題、系列、圖譜視覺化）。
- 精選參考：`references/`（人設、哲學、研究、來源）。
- `tools/`：fork 維護工具（Windows gate、上游檢查、相對連結檢查、依賴新鮮度）。
- `tools/tests/`：維護契約測試。獨立於產品測試目錄。

## 開發原則

- 一般變更直接推 `origin/main`，不開功能分支、不開維護 PR。只有在需要他人審查、或改動風險高到值得先讓 CI 在 PR 上跑一輪時，才退回 **branch → PR → CI → merge**。
- 修 bug 先補可重現失敗測試，再做最小修正。
- 不為了套格式而大改上游程式；Ruff 只閘維護工具的 E9（語法）與 F（pyflakes）。
- 使用繁體中文回覆；使用者文件以繁中為主，公開入口同步維護 `README.en.md`。直接交付可驗證結果，避免冗長背景鋪陳。
- 一般變更提交前跑 `pwsh -NoProfile -File tools\dev_check.ps1` 作為驗證 gate；不要把 gate 改成完整產品依賴安裝。
- 提交訊息用 Conventional Commit。Dependabot 或外部 fork 的變更走 PR，讀 diff 並通過 CI 後再合併。
- `REVIEW.md` 是風險快照，不是每個一般 bug 的流水帳。
- 不 force-push `main`，不刪 `upstream` remote。

## 上游處理

1. `git fetch upstream main`
2. `python tools/check_upstream_updates.py --strict`
3. 逐筆判斷是否與繁中 README、Windows gate、發佈閘門或測試衝突。
4. 可同步的提交用 merge；只需要部分修正時 cherry-pick 或最小重做。
5. 跑 `pwsh -NoProfile -File tools\dev_check.ps1`
6. 採用／略過寫進 `docs/DECISIONS.md`，驗證後才推進 `tools/upstream_baseline.json`

Baseline 代表「已審查」，不代表「全部已合併」。

## 依賴新鮮度

每月的 `Dependency freshness` workflow 跑 `tools/check_dependency_freshness.py`，比對宣告與 PyPI 現行版。

紅燈只有兩種正當出口，兩種都要留下理由：

- **維持宣告**：在宣告那一行加 `# freshness-hold: <理由>`。
- **已延後**：在 `.github/dependency-deferrals.json` 加一筆
  `{"deferredLatest": "<當時看到的版本>", "reason": "<為什麼這次不升>"}`。

不要用調高下限的方式讓紅燈消失：宣告是相容性承諾，不是消音鍵。

## 驗證

```powershell
pwsh -NoProfile -File tools\bootstrap_dev.ps1
```

沒有實際跑過 Windows gate，不要宣稱本機開發環境已可用。

## 文件責任

- `README.md` / `README.en.md`：公開產品與 fork 入口。
- `FORK.md`：與上游的關係、差異、同步方式。
- `NOTICE.md`：授權與 attribution。
- `docs/UPSTREAM.md`：upstream remote 與審查清冊。
- `docs/DEVELOPMENT.md`：本機開發與驗收指令。
- `docs/DECISIONS.md`：長期取捨。
- `REVIEW.md`：全庫風險快照。
- `CONTRIBUTING.md` / `SECURITY.md`：本 fork 的貢獻與安全回報流程。

## 對外邊界：PR 只打本 fork

- **PR、push、release 一律指向 `SanHsien/hung-yi-lee-skill`。** 對上游 `voidful/hung-yi-lee-skill` 開 PR、push 或發 release 需要維護者在當次對話明確同意回貢；「fork 一份」「建開發環境」「比照其他 repo」都不是同意。
- 根因是機制不是粗心：`gh` 在 fork clone 的**預設 repo 就是上游**，裸跑 `gh pr create` 必然打上去。每個 clone 先跑一次 `gh repo set-default SanHsien/hung-yi-lee-skill`。
- 開 PR 仍明寫 `gh pr create --repo SanHsien/hung-yi-lee-skill --base <分支> --head <分支>`，並**讀輸出的 URL**，owner 必須是 `SanHsien`。不是就立刻 `gh pr close` 留言道歉說明，再對 origin 重開。

---

## 知識庫架構與維護規範 (Wiki Schema & Operations)

本專案同時遵循 LLM-wiki 模式，圍繞李宏毅老師的影片與相關研究建構持久、複利的知識庫：

### 1. 分層架構
- **Raw Sources (`raw/`)**：單一真相源。LLM 可讀取但不應就地修改（除非抓取刷新）。包含頻道 metadata 與逐字稿快取。
- **Wiki (`wiki/`)**：LLM 維護的 Markdown。包含結構、摘要、交叉參照與組織。
- **Schema (`AGENTS.md`, `SKILL.md`)**：定義維護規範與查詢標準。

### 2. 操作模式
- **Ingest**：新增頻道資料或逐字稿後重新編譯 wiki。
- **Query**：先讀 `wiki/index.md`，查詢逐字稿與主題頁面，回答以逐字稿為基礎。
- **Graph**：執行 `python scripts/hungyi_kb.py graph build`，持久化至 `wiki/graph/graph.json`，使用 `graph query` 與 `graph report` 進行導航。

### 3. 回答標準
- 傳承李宏毅老師的教學法（直覺先行、Black Box 到內部機制、陷阱提醒、具體類比），不冒充本人。
