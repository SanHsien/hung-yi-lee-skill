# 維護決策

## 2026-09-11：建立 Windows-first 維護型 fork

**決定**：fork `voidful/hung-yi-lee-skill`，保留 MIT License 與完整歷史。本線預設分支用 `main`。本線聚焦繁中文件、Windows 開發 gate、Windows CI，以及逐筆審查的上游追蹤。

**理由**：`hung-yi-lee-skill` 是一套高品質的李宏毅老師 AI/機器學習課程知識庫、教學風格 DNA 與知識圖譜蒸餾 Skill。本 fork 補足 Windows 11 原生開發／驗收骨架、繁體中文維護入口，以及可審計的上游追蹤機制。

**限制**：

- 不把 fork 包裝成原創專案，不移除原作者 voidful、李宏毅老師與官方連結。
- 不發佈 PyPI 取代官方管道。
- 維護 gate 不預設安裝重型套件。
- 上游更新必須逐筆審查。

## 2026-09-11：依賴新鮮度追蹤

**決定**：`tools/check_dependency_freshness.py` 納管 `requirements-dev.txt` 與 `requirements.txt`。

**理由**：本 repo 的產品依賴（`youtube-transcript-api`, `networkx`, `python-louvain`, `yt-dlp`）與維護依賴（`pytest`, `ruff`）清單簡潔，納入每月新鮮度檢查以確保相容性。

## 2026-09-11：上游檢查涵蓋 Commit、PR 與 Issue 三面向

**決定**：`check_upstream_updates.py` 以 `--state all` 收集上游 PR 與 Issue，並追蹤 Commit SHA。`gh` 失敗時 fail closed（exit 2）。

**理由**：未合併即關閉的 PR 與待處理的 Issue 同樣可能揭露重要缺陷或需求。排程報告必須確保「未檢查」與「沒有新變更」截然分明。

## 2026-09-11：日常直接推 main

**決定**：日常維護修改在本機跑 `tools\dev_check.ps1` 後直接推 `origin/main`。Dependabot 與外部貢獻仍走 PR，合併前讀 diff。

**理由**：對齊 SanHsien 體系其他維護 fork 的治理規範。

## 2026-09-11：上游分支、PR 與 Issue 首次盤點結論

**決定**：
1. **上游分支**：僅 `upstream/main` 一個分支，無其他歷史或草稿分支。本 fork 唯一長期跟隨分支為 `upstream/main`。
2. **上游 PR（共 3 筆）**：
   - `#1` CLOSED：feat: add Hung-Yi Lee classic teaching style README（已由後續 commit 整合）。
   - `#2` MERGED：Fix requirements for a working fresh install（已合併進 main）。
   - `#3` MERGED：Fix CJK-collapsing concept node ids in the graph builder（已合併進 main）。
   - 當前無 open PR。
3. **上游 Issue（共 1 筆）**：
   - `#4` OPEN：「你真是个人才:)」，屬於社群正面回饋／留言，無代碼或架構改動需求，維持狀態。
4. **水位鎖定**：`tools/upstream_baseline.json` 鎖定 Commit `df5665d921a94c7937c27cf3c32e582008a95652`、PR 水位 `3`、Issue 水位 `4`。

**理由**：
- 確立乾淨的審查基準線，增量檢查未來僅需處理大於 `#4` 的新項目或 `df5665d` 之後的新 Commit。

## 2026-09-11：Windows 原生編碼免疫與零依賴繁簡通用支援

**決定**：
1. **Windows 原生編碼硬化**：在 `scripts/hungyi_kb.py` 中全量補齊所有檔案讀寫（`load_json`、`save_json`、`write_transcript_markdown`、`transcript_stats`、`write_markdown`、`append_log_entry`、`transcript_snippets`、`parse_transcript_lines`、`lint`）的 `encoding="utf-8"`，並在讀取時加入 `errors="replace"`；頂部加入標準 Windows `sys.stdout`/`sys.stderr` 的 UTF-8 自動 reconfigure。即使在完全未設 `PYTHONUTF8=1` 的舊版控制台或預設 CP950 環境下執行，也 100% 不崩潰。
2. **零外部依賴繁簡對齊（`scripts/hungyi_chinese.py`）**：以內建純字串與查表形式收錄 OpenCC 核心 4,012 個標準簡繁字元對照，並加入機器學習／人工智慧跨兩岸專業術語同義詞庫（如「神经网络」對齊「類神經網路」、「强化学习」對齊「增強式學習」）。搜尋（`search`）與知識圖譜查詢（`graph query`）自動進行雙向擴展，繁簡輸入皆能精準檢索。

**理由**：
- Windows 11 原生 PowerShell/CMD 預設採用系統代碼頁（如繁體中文版為 CP950），若缺乏 UTF-8 顯式宣告，讀取繁中 UTF-8 檔案或印出簡體字時直接擲出 `UnicodeDecodeError` / `UnicodeEncodeError`。
- 知識庫與逐字稿本體為繁體中文，使用者使用簡體字查詢時容易面臨完全無命中的困擾；採用內建零外部依賴設計可避免安裝繁重 C 擴充套件，維持極度輕量與高可靠度。

## 2026-09-11：全庫代碼審查與靜態分析硬化

**決定**：
1. **消除全庫 48 處 Ruff 警告**：
   - `scripts/hungyi_graph.py`：導入 `TYPE_CHECKING` 條件塊並引入 `import networkx as nx`，將原本使用字串註解 `"nx.Graph"` 改為直接使用 `nx.Graph`，解決動態導入導致模組級未定義變數問題；移除未使用之 `math` 與 `t2s` 導入；清理靜態字串之 `f-string` 宣告；優化字典純取值迭代（`PERF102`）。
   - `scripts/hungyi_chinese.py`：移除未使用的 `import re`。
   - `scripts/hungyi_kb.py`：將盲目捕獲所有例外的 `except Exception: pass` 縮窄為明確的 `(json.JSONDecodeError, OSError, KeyError)` 並加入 debug 警示；更新 `Iterable` 自 `collections.abc` 引入；明確補上 `subprocess.run(..., check=False)`；日誌時間戳補上 `tz=timezone.utc`；移除無 placeholder 的 `f-string` 與冗餘空字串 `print`。
   - `tools/tests/test_upstream_updates.py`：移除未使用的 `# noqa: I001`。
2. **擴充圖譜查詢單元測試**：在 `tools/tests/test_kb_helpers.py` 新增 `test_graph_query_and_token_matching`，針對繁體與簡體中文字詞在知識圖譜中的節點匹配邏輯提供自動化測試保障。

**理由**：
- 消除潛在的靜態分析隱患與未定義變數，確保 IDE、靜態分析器與運行時期行為高度一致。
- 遵循不盲目吞例外原則，在讀取持久化圖譜損毀時給出提示而非靜默失敗。

## 2026-09-12：檢索精度硬化、繁簡停用詞對齊與圖譜查詢優化

**決定**：
1. **停用詞庫繁簡對稱與中央化**：將原本散落在 `hungyi_kb.py` 的繁體停用詞移至 `scripts/hungyi_chinese.py:STOP_QUERY_TOKENS`，並擴充收錄簡體疑問詞（如「什么是」、「怎么」、「如何」、「为什么」等），提供 `is_stop_token()` 判斷函式，確保兩岸用語之停用詞過濾行為 100% 對稱。
2. **知識圖譜種子詞停用詞過濾**：在 `scripts/hungyi_graph.py:query_graph()` 中對查詢 token 進行 `is_stop_token()` 過濾，避免使用者以自然語言提問（如「什麼是Transformer」）時，「什麼是」被誤當成核心概念節點進行全圖 BFS 搜尋，造成無關節點稀釋檢索結果。
3. **消除同義詞逆向過度擴展（Over-expansion）缺陷**：修復 `expand_query_tokens()` 中 `cand in term` 的比對缺陷。原本的子字串比對會導致簡短通用詞（如「學習」）只要出現在任何專業術語複合詞中（如「對比學習」、「強化學習」、「聯邦學習」），就會一口氣被擴展成 28 種不相關的複合術語，造成檢索泛濫。移除 `cand in term` 後，僅保留 `term in cand`，維持複合名詞（如「深度學習架構」）正確帶出同義詞，同時保持通用詞純粹。
4. **知識圖譜 HTML 導出跳脫防護**：在 `scripts/hungyi_graph.py:export_html()` 中將社區標籤以 `html.escape()` 跳脫，避免自訂或特殊標籤造成 vis.js HTML 生成結構損壞或潛在 XSS 漏洞。
5. **BFS 佇列效能升級**：將 `query_graph()` 內的 BFS 探索佇列從 `list.pop(0)`（O(N) 時間複雜度）改為 `collections.deque.popleft()`（O(1) 時間複雜度）。
6. **測試覆蓋擴展**：在 `tools/tests/test_kb_helpers.py` 中新增繁簡停用詞對齊、同義詞不過度擴展、圖譜查詢停用詞過濾等 3 組單元測試，總測項自 42 項提升至 45 項。
7. **維護 CI 與測試依賴對齊**：將純 Python 依賴 `networkx>=3.4` 納入 `requirements-dev.txt`（附帶 `# freshness-hold: upstream compatibility floor`），同時在 `tools/tests/test_kb_helpers.py` 針對圖譜查詢測試配置 `pytest.importorskip("networkx")` 雙重防禦。徹底修復 CI 在未安裝產品全量依賴時跨 5 個 Python 版本（3.10-3.14）因 `ModuleNotFoundError: No module named 'networkx'` 報錯之問題。

**理由**：
- 提升自然語言輸入時李宏毅知識庫與知識圖譜查詢的準確度與穩健性，避免無效停用詞與過度泛化名詞破壞搜尋體驗。
- 確保維護 CI 工作流（Windows Python 3.10~3.14）與本機最小維護環境一致且 100% 綠燈通過。
- 遵循高標準程式碼品質與防禦性設計原則。


