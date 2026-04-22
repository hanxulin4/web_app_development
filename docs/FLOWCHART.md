# 流程圖文件（Flowchart）— 活動報名系統

本文件根據 `docs/PRD.md` 與 `docs/ARCHITECTURE.md`，以 Mermaid 語法視覺化「活動報名系統」的使用者操作流程與系統內部資料流動。

---

## 1. 使用者流程圖（User Flow）

此流程圖涵蓋兩條主要路徑：**主辦者（建立活動、查看統計）** 與 **報名者（報名參加活動）**。

```mermaid
flowchart LR
    Start([使用者開啟網站]) --> Home["首頁<br>活動列表"]

    Home --> Action{要做什麼？}

    %% ===== 主辦者路線 =====
    Action -->|建立新活動| CreatePage["建立活動頁面<br>GET /events/create"]
    CreatePage --> FillEvent["填寫活動名稱<br>選擇活動日期<br>填寫活動描述"]
    FillEvent --> SubmitEvent["送出建立表單<br>POST /events/create"]
    SubmitEvent --> Validate{資料驗證}
    Validate -->|失敗| CreatePage
    Validate -->|成功| EventCreated["活動建立成功<br>重導至活動詳情頁"]

    %% ===== 報名者路線 =====
    Action -->|查看活動| EventDetail["活動詳情頁<br>GET /events/id"]
    EventCreated --> EventDetail

    EventDetail --> ViewInfo["查看活動資訊<br>名稱 / 日期 / 描述"]
    EventDetail --> ViewStats["查看報名統計<br>總人數 / 男女人數"]
    EventDetail --> ViewList["查看報名名單<br>姓名 / 性別 / 時間"]
    EventDetail --> Register["填寫報名表單<br>姓名 / 性別"]

    Register --> SubmitReg["送出報名<br>POST /events/id"]
    SubmitReg --> RegValidate{資料驗證}
    RegValidate -->|失敗| EventDetail
    RegValidate -->|成功| Success(["報名成功頁面<br>GET /events/id/success"])
```

### 流程說明

1. **首頁**：所有使用者進入網站後，看到活動列表
2. **建立活動**：主辦者點擊「建立活動」按鈕，填寫活動資訊並送出
3. **活動詳情**：使用者點擊活動或透過分享連結進入，可以查看活動資訊、報名統計，也可以直接報名
4. **報名流程**：填寫姓名與性別後送出，成功後跳轉至感謝頁面

---

## 2. 系統序列圖（Sequence Diagram）

### 2.1 建立活動流程

```mermaid
sequenceDiagram
    actor User as 主辦者
    participant Browser as 瀏覽器
    participant Route as Flask Route
    participant Model as Event Model
    participant DB as SQLite

    User->>Browser: 點擊「建立活動」
    Browser->>Route: GET /events/create
    Route-->>Browser: 回傳建立活動表單頁面

    User->>Browser: 填寫活動名稱、日期、描述，按下送出
    Browser->>Route: POST /events/create (表單資料)

    Route->>Route: 驗證表單資料（名稱、日期不可空白）

    alt 驗證失敗
        Route-->>Browser: 回傳錯誤訊息，重新顯示表單
    else 驗證成功
        Route->>Model: 呼叫建立活動函式
        Model->>DB: INSERT INTO events (name, date, description)
        DB-->>Model: 回傳新活動 ID
        Model-->>Route: 回傳建立結果
        Route-->>Browser: HTTP 302 重導至 /events/{id}
        Browser-->>User: 顯示活動詳情頁面
    end
```

### 2.2 報名活動流程

```mermaid
sequenceDiagram
    actor User as 報名者
    participant Browser as 瀏覽器
    participant Route as Flask Route
    participant Model as Registration Model
    participant DB as SQLite

    User->>Browser: 透過連結開啟活動頁面
    Browser->>Route: GET /events/{id}
    Route->>Model: 查詢活動資訊與報名統計
    Model->>DB: SELECT 活動資訊 + COUNT 統計
    DB-->>Model: 回傳活動資料與統計數字
    Model-->>Route: 回傳結果
    Route-->>Browser: 渲染活動詳情頁（含報名表單）

    User->>Browser: 填寫姓名、選擇性別，按下「報名」
    Browser->>Route: POST /events/{id} (姓名、性別)

    Route->>Route: 驗證表單資料（姓名、性別不可空白）

    alt 驗證失敗
        Route-->>Browser: 回傳錯誤訊息，重新顯示表單
    else 驗證成功
        Route->>Model: 呼叫新增報名函式
        Model->>DB: INSERT INTO registrations (event_id, name, gender)
        DB-->>Model: 寫入成功
        Model-->>Route: 回傳結果
        Route-->>Browser: HTTP 302 重導至 /events/{id}/success
        Browser-->>User: 顯示「報名成功」感謝頁面
    end
```

### 2.3 查看報名統計流程

```mermaid
sequenceDiagram
    actor User as 主辦者/使用者
    participant Browser as 瀏覽器
    participant Route as Flask Route
    participant Model as Model
    participant DB as SQLite

    User->>Browser: 開啟活動詳情頁
    Browser->>Route: GET /events/{id}
    Route->>Model: 查詢活動資訊
    Model->>DB: SELECT * FROM events WHERE id = ?
    DB-->>Model: 回傳活動資料

    Route->>Model: 查詢報名統計
    Model->>DB: SELECT gender, COUNT(*) FROM registrations WHERE event_id = ? GROUP BY gender
    DB-->>Model: 回傳男女人數統計

    Route->>Model: 查詢報名名單
    Model->>DB: SELECT name, gender, created_at FROM registrations WHERE event_id = ?
    DB-->>Model: 回傳報名名單

    Model-->>Route: 彙整所有資料
    Route-->>Browser: 渲染活動詳情頁（含統計與名單）
    Browser-->>User: 顯示總人數、男性人數、女性人數、報名名單
```

---

## 3. 功能清單對照表

以下列出每個功能對應的 URL 路徑與 HTTP 方法：

| 功能             | 說明                                 | URL 路徑               | HTTP 方法   |
| ---------------- | ------------------------------------ | ---------------------- | ----------- |
| 首頁（活動列表） | 顯示所有活動清單，按日期排序         | `/`                    | `GET`       |
| 建立活動頁面     | 顯示建立活動的表單                   | `/events/create`       | `GET`       |
| 建立活動處理     | 接收表單資料，建立新活動             | `/events/create`       | `POST`      |
| 活動詳情頁       | 顯示活動資訊、報名統計、報名表單     | `/events/<id>`         | `GET`       |
| 報名處理         | 接收報名資料，新增報名記錄           | `/events/<id>`         | `POST`      |
| 報名成功頁       | 顯示報名成功的確認訊息               | `/events/<id>/success` | `GET`       |

> **註**：`<id>` 為活動的唯一識別碼（資料庫自動產生的整數 ID）。使用者透過分享的連結（如 `http://localhost:5000/events/3`）即可直接進入特定活動的報名頁面。
