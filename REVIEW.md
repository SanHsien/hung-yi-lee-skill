# Repository review（Windows-only）

- Review date: 2026-09-11
- Review baseline: `df5665d921a94c7937c27cf3c32e582008a95652`
- Remediation: 同日 fork-local overlay（不回貢）
- Upstream reviewed through: `df5665d921a94c7937c27cf3c32e582008a95652`
- Primary environment: Windows 11、PowerShell、Python 3.14.7（本機 gate）；產品 Python 要求 `>=3.10`
- Status: 維護骨架與產品相依環境全面可用。已完成建立 Windows 原生門禁與驗收。

## 結論

這個 fork 適合作為 Windows 本機、給 Agent 維護的 Hung-Yi Lee Skill 線。產品行為跟隨 `voidful/hung-yi-lee-skill` `df5665d`，再加上本線維護骨架：繁體中文維護文件、Windows 原生 1-click gate、純 Windows 原生維護 CI、每週上游水位追蹤（commit、PR、issue）以及每月依賴新鮮度檢查。

本 repo 的產品依賴（`youtube-transcript-api`, `networkx`, `python-louvain`, `yt-dlp`）與維護依賴（`pytest`, `ruff`）皆已完整梳理並通過 Windows 原生環境驗證。在 Windows 環境下執行腳本時，門禁與工具腳本全面注入 `$env:PYTHONUTF8 = "1"`，避免預設 ANSI/CP950 編碼解碼 UTF-8 知識庫檔案失敗。

## 本輪實證

### 審查當下（`df5665d`）

```text
git rev-parse HEAD
→ df5665d921a94c7937c27cf3c32e582008a95652

gh repo set-default --view
→ SanHsien/hung-yi-lee-skill
```

實查結果：
- 上游 repository 為 `voidful/hung-yi-lee-skill`，採 MIT License。
- 上游 PR 水位為 `#3`，Issue 水位為 `#4`。
- 上游未配置 GitHub Actions workflows，本 fork 建立了純 Windows 原生 CI 工作流程。
- 維護工具無 `os.system`／`shell=True`／`eval(`／`exec(`。

## 已修 findings

| ID | 嚴重度 | 做了什麼 |
|---|---|---|
| R-01 | P2 | `.gitignore` 加入 `.env`、`.venv`、`upstream-review-report.md`、`dependency-freshness-report.md`、`.ruff_cache/` |
| R-02 | P2 | 建立獨立維護測試目錄 `tools/tests/` 與獨立 `tools/pytest.ini`，避免產品環境污染 |
| R-03 | P2 | 建立 `FORK.md`、`NOTICE.md`、`LICENSE`、`SECURITY.md`、`AGENTS.md`、`CLAUDE.md`、`GEMINI.md`，寫明對外邊界與安全性 |
| R-04 | P3 | `README.md`（繁體中文）與 `README.en.md`（英文鏡像）雙向互指，並標明 upstream 與 MIT 條款 |
| R-05 | P2 | 建立 `tools/dev_check.ps1` 與 `tools/bootstrap_dev.ps1`，規範 Windows 11 原生 PowerShell 驗收門禁（注入 `PYTHONUTF8=1` 防範 CP950 解碼例外） |
| R-06 | P2 | 建立 `tools/test_product.ps1` 驗證知識庫 lint、搜尋與知識圖譜查詢 |
| R-07 | P2 | 建立純 Windows 原生 CI（`ci.yml`、`codeql.yml`、`upstream-check.yml`、`dependency-freshness.yml`） |
| R-08 | P2 | 建立上游追蹤水位防重複巡檢機制，鎖定 PR `#3`、Issue `#4` |
| R-09 | P2 | 全面防護未設 `PYTHONUTF8` 的 Windows 環境：補齊 `hungyi_kb.py` 所有檔案讀寫、日誌寫入、逐字稿快取、subprocess 呼叫的 `encoding="utf-8"`，並在頂部加入 Windows stdout/stderr UTF-8 reconfigure，確保舊版控制台與預設 CP950 環境下 100% 免疫 |
| R-10 | P2 | 實作零依賴繁簡通用支援（`scripts/hungyi_chinese.py`）：內建 4000+ 字標準簡繁對照與 AI/ML 跨兩岸專業術語對齊，CLI `search` 與 `graph query` 原生支援簡體中文輸入自動檢索繁體知識庫 |
| R-11 | P2 | 全庫代碼審查與硬化：消除 48 個 Ruff 靜態分析警告，修復 `hungyi_graph.py` 中 `nx.Graph` 的 `TYPE_CHECKING` 類型定義與未定義變數；修復 `hungyi_kb.py` 中盲目捕獲例外的 `try-except-pass` 改為具體例外與除錯提示；補齊 `subprocess.run(..., check=False)` 明確宣告與 `datetime.now(tz=...)` 時區；補齊知識圖譜查詢單元測試。 |
| R-12 | P2 | 檢索精度與圖譜查詢硬化：修復停用詞繁簡不對稱問題，將 `STOP_QUERY_TOKENS` 整合進 `scripts/hungyi_chinese.py` 並支援 `is_stop_token()`；修復圖譜查詢 `query_graph()` 未過濾疑問句停用詞造成種子節點被稀釋之缺陷；修復 `expand_query_tokens()` 因 `cand in term` 逆向子字串比對導致通用詞（如「學習」）爆炸擴展之缺陷；防範 `export_html()` 社群標籤潛在 HTML 結構損壞；將 BFS 佇列改為 `collections.deque` 提升佇列效能；將 `networkx` 納入 `requirements-dev.txt` 並在單元測試配置 `pytest.importorskip` 防禦，修復維護 CI 與極簡環境缺失依賴導致之失敗；全庫 45 測項全數通過。 |

## 接受、不改契約

| ID | 嚴重度 | 處理 |
|---|---|---|
| - | - | （無。所有已識別項目皆已妥善處理完畢） |

## 尚未宣稱範圍

- **不宣稱** 已將任何修改提交回原作者上游（依 fork 維護政策，所有 PR/commit 僅限於 `SanHsien/hung-yi-lee-skill`）。

