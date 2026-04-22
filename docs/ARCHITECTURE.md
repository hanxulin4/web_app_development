# 系統架構文件 (Architecture)

## 1. 技術架構說明

本專案為「活動報名系統」，依照 PRD 的需求，為了快速開發與達成輕量部署的目標，我們採用以下技術架構：

- **後端框架**：**Python + Flask**
  - 使用 Python 輕量級的 Web 框架 Flask。因為不需要過度龐大複雜的設定，非常適合拿來快速打造 MVP 的頁面路徑與 API。
- **前端與模板引擎**：**Jinja2**
  - 我們**不採用前後端分離**，而是由 Flask 路由直接搭配 Jinja2 模板將動態資料塞到 HTML 內並一同渲染給瀏覽器。能夠省下撰寫前端 API 請求 (如 fetch/axios) 及跨域 (CORS) 問題的成本。
- **資料庫**：**SQLite**
  - 不架設額外的資料庫伺服器，直接在資料夾底下產生實體的關聯式資料庫檔案（`.db`），作為單純且立即可用的資料庫首選。

### Flask MVC 模式說明
在這樣的架構下，各元件的職責區分如下：
- **Model（資料模型）**：負責與 SQLite 互動，例如：建立活動表單、新增報名者資料、計算男女總數，專注處理資料邏輯。
- **View（視圖 / 模板）**：專指 `templates/` 資料夾裡的 HTML。負責呈現活動列表、報名表與後台儀表板，將資料美化呈現給主辦方和報名者。
- **Controller（控制器 / 路由）**：即 Flask 的 `routes.py`。負責當橋樑，接收瀏覽器傳來的資料（例如表單送出），傳給 Model 儲存，然後決定要呼叫哪一個 View 畫面回應給使用者。

---

## 2. 專案資料夾結構

以下為建議的專案資料夾結構與用途說明：

```text
web_app_development/
│
├── app/                      # 應用程式主要功能資料夾
│   ├── __init__.py           # Flask App 初始化與套件設定 (綁定 DB)
│   ├── models.py             # 資料庫模型結構設定 (定義 Activity, Registration 等資料表)
│   ├── routes.py             # 網站的主幹，定義各大 URL 頁面處理邏輯
│   ├── static/               # 靜態資源檔案
│   │   ├── css/              # 樣式表 (包含共用的排版語法)
│   │   ├── js/               # 前端腳本 (如：提示視窗互動)
│   │   └── img/              # 圖片資源
│   └── templates/            # Jinja2 HTML 模板
│       ├── base.html         # 共用的版型骨架 (載入共用的 Head、Navbar)
│       ├── create_event.html # 頁面：建立活動
│       ├── event_form.html   # 頁面：給報名者的報名表單
│       └── dashboard.html    # 頁面：主辦方後台總覽 (顯示人數統記與名單)
│
├── instance/                 # 用來放不進入版本控制的執行期資料
│   └── database.db           # SQLite 實體資料庫，系統自動生成在此處
│
├── docs/                     # 專案文件存放區
│   ├── PRD.md                # 產品需求文件
│   └── ARCHITECTURE.md       # 系統架構文件 (本文件)
│
├── app.py                    # 專案主入口，執行此檔案即可啟動本地伺服器
└── requirements.txt          # Python 依賴的套件清單 (例如 flask)
```

---

## 3. 元件關係圖

以下展示使用者（報名者或主辦方）操作系統時的資料流與元件互動。

```mermaid
flowchart TD
    Browser[瀏覽器 \n(參加者填單 / 主辦方檢視)]
    
    subgraph 伺服器端 Flask APP (伺服器核心)
        Route[Flask Route \n(Controller)]
        Model[Models \n(業務與計算)]
        Template[Jinja2 \n(View)]
    end
    
    DB[(SQLite \ndatabase.db)]

    %% 處理流程
    Browser -- "1. 請求 URL / 提交表單資料" --> Route
    Route -- "2. 驗證資料並請求資料庫操作" --> Model
    Model -- "3. 透過 Python 執行 SQL" --> DB
    DB -- "4. 回傳讀寫結果 / 統計數據" --> Model
    Model -- "5. 將結果交給路由" --> Route
    Route -- "6. 決定渲染哪個頁面，夾帶數據" --> Template
    Template -- "7. 建立含資料的 HTML" --> Route
    Route -- "8. 回傳 HTTP Response" --> Browser
```

---

## 4. 關鍵設計決策

1. **不採用前後端分離，專注於 Flask + Jinja2 打包渲染**
   - **原因**：為了符合快速、輕量的 MVP 需求。活動報名系統核心是以表單送出與儀表板為主，不需要繁雜的前端路由管理，這省去了前端環境建立的繁衍時間，使工程師能集中處理邏輯。

2. **使用單一 `routes.py` 作為 Controllers**
   - **原因**：現階段功能相對單純，若提前引入 Flask Blueprint 反而會增加初學團隊的閱卷成本。將功能全部宣告於單一個 `routes.py`，能更直覺找到某一個 URL 的邏輯在哪。未來的「匯出清單」、「信件功能」若讓檔案過於肥大，再予以重構。

3. **統一將 SQLite 資料庫放置在 `instance/` 資料夾內**
   - **原因**：保護真實的報名者個資與主辦單位活動資料可以隨時被 `gitignore`。此外讓專案主體 `app/` 對於資料庫檔案解耦，方便佈署時可以依照環境產生新的 db 檔。

4. **採用後端計算來產出「性別統計」與「報名數量」**
   - **原因**：我們在 Model / Route 取資料時，將利用 SQL 的 `COUNT` 等語法或是從後端 List 加總。避免「將完整的全部資料拋給前端讓 JS 計算」，以防止資料過大影響效能，同時確保非主辦方透過瀏覽器檢視到未經授權的個人隱私資料。
