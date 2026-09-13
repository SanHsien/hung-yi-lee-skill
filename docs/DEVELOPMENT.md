# 開發環境

維護者與 AI 接手用的開發文件。產品使用方式在 [`README.md`](../README.md)；上游同步在 [`UPSTREAM.md`](UPSTREAM.md)；決策在 [`DECISIONS.md`](DECISIONS.md)。

## 架構

```text
scripts/
  ├── hungyi_kb.py             知識庫 CLI、抓取、編譯、搜尋、分析
  └── hungyi_graph.py          知識圖譜建置與社群劃分引擎
raw/
  └── youtube/                 原始頻道 metadata、逐字稿快取索引與 Markdown
wiki/
  ├── index.md                 知識庫導航入口
  ├── topic-map.md             主題地圖
  ├── query-playbook.md        查詢操作指引
  ├── graph/                   知識圖譜報告、JSON 與 HTML 視覺化
  ├── topics/                  8 大核心主題頁面
  └── series/                  系列課程頁面
references/                    精選參考（人設、哲學、研究方向、資料來源）
tools/                         fork 維護工具（Windows gate、上游檢查、相對連結檢查、依賴新鮮度）
  └── tests/                   維護契約測試
docs/                          fork 維護與治理文件
```

## 本機開發（Windows 11 原生）

### 維護骨架（必跑）

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements-dev.txt
$env:PYTHONUTF8 = "1"
pwsh -NoProfile -File tools\dev_check.ps1
```

等價一鍵指令：

```powershell
pwsh -NoProfile -File tools\bootstrap_dev.ps1
```

若需一併安裝產品執行依賴（包含知識圖譜與影片抓取套件）：

```powershell
pwsh -NoProfile -File tools\bootstrap_dev.ps1 -All
```

### 執行產品測試

本 repo 提供專用 Windows 原生產品測試腳本 `tools/test_product.ps1`：

```powershell
pwsh -NoProfile -File tools\test_product.ps1
```

## Canonical Gate

`tools\dev_check.ps1` 會依序執行：

1. `python -m compileall`（`tools`）
2. `ruff check`（E9 + F，僅檢查 `tools`）
3. `pytest tools/tests`（使用獨立的 `tools/pytest.ini`）
4. `python tools/check_links.py`（驗證所有維護文件相對連結）

CI 專注於 Windows 原生環境，在 `windows-latest` 執行完整 Python 3.10–3.14 矩陣並跑過 gate。推至 `main` 前請務必在本機跑過 gate。

## 依賴新鮮度

`tools/check_dependency_freshness.py` 納管 `requirements-dev.txt` 與 `requirements.txt`。

紅燈只有兩條誠實的出口：

| 出口 | 寫在哪 | 什麼時候用 |
| --- | --- | --- |
| `# freshness-hold: <理由>` | `requirements-dev.txt` 或 `requirements.txt` 行末 | 這個下限就是我們要的 |
| `.github/dependency-deferrals.json` 的 `deferredLatest` + `reason` | 獨立檔案 | 已看過、這個月不升；PyPI 超過該版本會恢復提醒 |

不要用調高下限讓報告變綠。

## 不要做的事

- 不要提交含有個人憑證、API key 或敏感資訊的檔案。
- 不要把 PR 指向上游 `voidful/hung-yi-lee-skill`。
