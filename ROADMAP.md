# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-10-29 依 `main` `c971097f327c` 查的快照，開工前先重查 GitHub。

## 現況

這是保留上游課程知識庫與教學方法的 Windows 維護線，GitHub 標記為非 fork，但來源與維護責任仍依 fork 文件（`AGENTS.md:7-13`、`FORK.md:3-12`；2026-10-29 `gh` 查詢）。2026-10-29 快照 open PR、Dependabot／code scanning 告警均為 0，CI、CodeQL、Dependency freshness、Upstream check 最近結果為 success；issue 因停用而未查到，不代表沒有問題（2026-10-29 `gh` 查詢，`c971097f327c`）。深掃提出的詞級簡繁轉換已由後續提交處理，不再列為待辦（`6617c53` 至 `1145acf`；`scripts/hungyi_chinese.py:151-163`）。

## 近期：可以直接動手

| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 無：維持現狀 | 沒有已確認且尚未處理的阻擋項；不重做舊報告中的詞級轉換修復 | 開工重查 `gh pr list --repo SanHsien/hung-yi-lee-skill`、安全告警與 Actions；出現新項目才新增具體工作 | 維護者 | 2026-10-29 `gh` 查詢；`1145acf`；接續開發報告（2026-10-25）〈未完成線索〉 |

## 中期：等條件成立再做

| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 增量審查上游課程與程式變更 | 上游 commit／PR／issue 超過 `tools/upstream_baseline.json` 的已審水位，或 Upstream check 提醒 | 執行 `python tools/check_upstream_updates.py --strict`；逐筆讀 diff、採用／延後寫入決策；Windows gate 通過後才推進水位 | Codex | `tools/upstream_baseline.json:2-8`；`docs/UPSTREAM.md:23-32` |
| 重審依賴延後理由 | Dependency freshness 出現新版本，超過已記錄的 `deferredLatest` | 閱讀 release notes，以新版本跑 `pwsh -NoProfile -File tools/dev_check.ps1`；記錄採用或延後原因，不只調高下限 | Claude Sonnet | `docs/DECISIONS.md:90-100`；`AGENTS.md:54-64` |
| 擴充簡繁查詢詞級規則 | 真實查詢出現漏查或跨詞界誤轉，現有案例可重現 | 先加失敗案例，同驗目標詞、跨詞界句子、原 token 保留與圖譜查詢；維護 gate 及 `tools/test_product.ps1` 通過 | Codex | `scripts/hungyi_chinese.py:151-163`；`2439285`、`1145acf`；`docs/DEVELOPMENT.md`〈執行產品測試〉 |

## 刻意不做

| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 因 issue 停用而要求重新啟用 | 這是回報管道設定，不是已證實的產品缺陷 | 維護者需要公開追蹤回報時 |
| 重寫上游知識庫、冒充原作者或另發替代 PyPI 套件 | 保留來源、產品與授權邊界；決策見 `docs/DECISIONS.md:3-14` | 維護者提出明確產品需求且完成授權評估 |
| 為追最新版本提高相容下限，或把維護 gate 變成完整產品安裝 | 下限是相容承諾，產品測試另有入口 | 新功能確實依賴較新版本，或需要獨立產品驗收時 |

## 維護方式

每週沿用 `docs/UPSTREAM.md` 增量審查；baseline 是已審水位，不表示全數合併，沒有共同祖先不作為改寫歷史的理由。
每月查看 Dependency freshness；有變更才跑對應 Windows gate／產品測試，不為巡檢另造 release；其他文件只連結本路線圖。
