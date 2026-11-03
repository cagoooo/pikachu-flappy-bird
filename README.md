# ⚡ 皮卡丘天空大冒險 Pika Sky Adventure

🌐 **線上使用：[皮卡丘天空大冒險](https://cagoooo.github.io/pikachu-flappy-bird/)**

> 📌 **建置版本：2026.06.23-12**（依據 `version.json`）

一款有質感、好玩、可直接上線的單檔 HTML **3D 皮卡丘 Flappy Bird** 課堂教學小遊戲。點擊畫面或按空白鍵讓皮卡丘起飛，閃過電線桿，每得 10 分切換一個新場景。

## ✨ 特色
- 🟡 圓潤立體皮卡丘（臉頰／耳朵／拍動翅膀／陰影立體感）
- 🌥️ **6 場景循環**：晴空 → 黃昏 → 星夜 → 極光 → 櫻花 → 深海，每 10 分換場景＋轉場動畫＋音效
- 🔊 WebAudio 合成音效（拍翅／得分／撞擊／換場），免外部檔、可離線
- 🏆 localStorage 最佳紀錄、結算畫面、再玩一次
- 📱 RWD 手機直式可玩、難度適中老少咸宜
- 🤖 開發者彩蛋：網址加 `?autopilot=1` 自動駕駛展示

## 🎮 線上遊玩
部署於 GitHub Pages（見 repo 右側 Pages 連結）。

## 🛠️ 技術
單一 `index.html`（HTML + Canvas 2D + WebAudio，零外部依賴、免 build）。

---
Made with ❤️ by 阿凱老師｜桃園市龍潭區石門國民小學

---

<!-- BEGIN:PROJECT_GUIDE -->
## 專案導覽

⚡ 皮卡丘天空大冒險 - 單檔 3D Flappy Bird 教學小遊戲 by 阿凱老師

- 專案定位：互動遊戲／遊戲化學習專案
- Repository：`cagoooo/pikachu-flappy-bird`
- 可見性：公開
- 主要技術：HTML
- 線上入口：<https://cagoooo.github.io/pikachu-flappy-bird/>

### 可以怎麼應用

- 課堂暖身、複習活動或學習站任務
- 校慶、闖關或社團活動中的互動挑戰
- 替換題庫、美術、音效與規則後，延伸成其他學科或主題遊戲

這些是依目前專案定位整理的延伸方向，不代表所有情境都已內建完成；實作前請先確認現有功能與資料格式。

### 技術與專案結構

- `README.md`
- `apple-touch-icon.png`
- `index.html`
- `scripts`

檔案結構會隨版本演進；若本節與程式碼不一致，以目前預設分支的原始碼為準。

### 本機執行

這是可直接由瀏覽器載入的靜態網站。可用任一靜態檔案伺服器預覽，例如：
```bash
python -m http.server 8000
```
接著開啟 `http://localhost:8000`。請避免直接以 `file://` 測試需要模組、請求或 Service Worker 的功能。

### 給 AI Agent 的接手指南

1. 先閱讀本 README、`AGENTS.md`（若有）、套件腳本與部署設定。
2. 先找出遊戲狀態、關卡／題庫資料與輸入控制的來源，再調整規則。
3. 更換素材時同步檢查授權、載入路徑、碰撞區域與不同螢幕比例。
4. 修改後至少驗證開始、遊玩、計分／勝負、重新開始，以及手機與桌面版面。
5. 不要捏造尚未存在的功能；README 與實作有落差時，應同時更新文件。
6. 提交前只納入本次任務檔案，並記錄實際執行過的驗證。

### 安全與資料注意事項

- 不要提交 `.env`、服務帳號、API 金鑰、token、學生個資或正式環境匯出資料。
- 使用 Firebase、Supabase、Google API 或其他雲端服務時，請建立自己的測試專案並套用最小權限。
- 若要公開衍生作品，請先確認程式碼、圖片、音訊、字型與教材內容的授權。

### 貢獻與客製化

歡迎依教學現場、活動或工作流程需求進行 fork／客製化。建議在變更說明中交代使用情境、主要修改、測試方式，以及是否影響資料格式或部署設定。
<!-- END:PROJECT_GUIDE -->

<!-- akai-edu-tools:backlink -->

---

## 🔗 阿凱老師教育工具集

這個專案是[阿凱老師教育工具集](https://cagoooo.github.io/Akai/)的 **#112 皮卡丘天空大冒險**，由桃園市龍潭區石門國民小學阿凱老師開發。

- 工具介紹頁：[https://cagoooo.github.io/Akai/tool/112/](https://cagoooo.github.io/Akai/tool/112/)
- 線上使用：[https://cagoooo.github.io/pikachu-flappy-bird/](https://cagoooo.github.io/pikachu-flappy-bird/)
- 教學情境文章：[https://cagoooo.github.io/Akai/blog/pikachu-sky-adventure-112-flappy-bird-game/](https://cagoooo.github.io/Akai/blog/pikachu-sky-adventure-112-flappy-bird-game/)
- 全部工具（上百個教育工具與原始碼）：[https://cagoooo.github.io/Akai/](https://cagoooo.github.io/Akai/)

想改造成自己的版本？到上面的教學情境文章，按左下角「複製 AI 開發提示詞」，貼給 ChatGPT、Claude、Gemini 等 AI 助手，就能參考這份原始碼開始規劃。
