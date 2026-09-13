# 安全政策

## 支援範圍

安全修正以本 fork 的最新 `main` 為主；上游版本的問題也會視需要回報原作者。

## 私下回報

若發現針對本 fork 維護骨架或衍生程式的安全漏洞，請使用 GitHub Security Advisories 的 **Report a vulnerability** 私下回報：
<https://github.com/SanHsien/hung-yi-lee-skill/security/advisories/new>。
若該入口不可用，請透過 GitHub 個人檔案聯絡維護者，不要先建立公開 Issue。

若問題屬於上游核心邏輯，亦可向原作者 voidful 通報。

回報請包含影響範圍、重現步驟、受影響版本與最小必要證據。請勿在回報中附上真實 API key、token、個人機密文件或帳密。

## 特別注意

- **命令列工具與網路存取**：`scripts/hungyi_kb.py` 在執行 `sync-metadata` 與 `sync-transcripts` 時會調用外部工具（如 `yt-dlp`）與 YouTube 網路連線。在受限環境或自動化排程中請注意網路連線逾時與代理伺服器設定。
- **檔案路徑防護**：知識庫查詢與轉存時涉及 Markdown 檔案寫入（`outputs/query-briefs/`、`wiki/`），請防範路徑遍歷與非預期檔名覆蓋。
- **本專案範圍**：不要將真實個人資料、含憑證的設定檔或 API key 提交進 repository。
