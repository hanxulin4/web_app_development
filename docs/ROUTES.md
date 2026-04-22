# 路由設計文件 (ROUTES)

本文件根據 PRD 與系統架構，規劃「活動報名系統」的所有路由、處理邏輯及對應的 Jinja2 模板。

---

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁（活動列表） | GET | `/` | `index.html` | 顯示所有即將到來的活動清單 |
| 建立活動頁面 | GET | `/events/create` | `create_event.html` | 顯示讓主辦方填寫活動資訊的表單 |
| 建立活動 | POST | `/events/create` | — | 接收表單，存入資料庫，並重導向至活動詳情頁 |
| 活動詳情頁 | GET | `/events/<int:id>` | `event_detail.html` | 顯示單一活動資訊、報名統計、報名表單及報名名單 |
| 報名活動 | POST | `/events/<int:id>` | — | 接收報名表單，存入資料庫，並重導向至報名成功頁面 |
| 報名成功頁 | GET | `/events/<int:id>/success` | `register_success.html` | 顯示報名成功的感謝與確認訊息 |

---

## 2. 每個路由的詳細說明

### 2.1 首頁（活動列表）
- **URL**: `GET /`
- **輸入**: 無
- **處理邏輯**: 呼叫 `Event.get_all()` 取得所有活動。
- **輸出**: 渲染 `index.html`，並將活動列表傳入模板。
- **錯誤處理**: 若無任何活動，則在模板中顯示「目前尚無活動，點擊建立第一個活動」。

### 2.2 建立活動頁面
- **URL**: `GET /events/create`
- **輸入**: 無
- **處理邏輯**: 準備渲染建立表單。
- **輸出**: 渲染 `create_event.html`。
- **錯誤處理**: 無特殊錯誤處理。

### 2.3 建立活動（處理）
- **URL**: `POST /events/create`
- **輸入**: 表單欄位包含 `name` (活動名稱), `event_date` (活動日期), `description` (活動描述)。
- **處理邏輯**: 
  1. 驗證 `name` 與 `event_date` 是否為空。
  2. 呼叫 `Event.create()` 將資料存入 SQLite。
- **輸出**: 重導向 (Redirect) 至 `GET /events/<id>`。
- **錯誤處理**: 若驗證失敗（如漏填必填欄位），重新渲染 `create_event.html` 並夾帶錯誤訊息 (Flash Message)。

### 2.4 活動詳情頁
- **URL**: `GET /events/<int:id>`
- **輸入**: URL 參數 `id` (活動 ID)。
- **處理邏輯**: 
  1. 呼叫 `Event.get_by_id(id)` 取得活動資訊。
  2. 呼叫 `Registration.get_stats_by_event(id)` 取得統計數據（男、女、總人數）。
  3. 呼叫 `Registration.get_by_event(id)` 取得目前的報名名單。
- **輸出**: 渲染 `event_detail.html`，並將上述資料全數傳入模板。
- **錯誤處理**: 若找不到對應 `id` 的活動，回傳 404 錯誤頁面或重導向至首頁並提示「找不到該活動」。

### 2.5 報名活動（處理）
- **URL**: `POST /events/<int:id>`
- **輸入**: 表單欄位包含 `name` (姓名), `gender` (性別), `contact_info` (聯絡資訊)。
- **處理邏輯**: 
  1. 驗證 `name` 與 `gender` 是否為空。
  2. 確認該活動是否存在 (`Event.get_by_id(id)`)。
  3. 呼叫 `Registration.create()` 將報名者存入 SQLite。
- **輸出**: 重導向 (Redirect) 至 `GET /events/<id>/success`。
- **錯誤處理**: 若驗證失敗，重新渲染 `event_detail.html` 並顯示錯誤提示。

### 2.6 報名成功頁
- **URL**: `GET /events/<int:id>/success`
- **輸入**: URL 參數 `id` (活動 ID)。
- **處理邏輯**: 呼叫 `Event.get_by_id(id)` 取得活動名稱，以便在成功頁面顯示「您已成功報名 XXX 活動」。
- **輸出**: 渲染 `register_success.html`。
- **錯誤處理**: 若找不到活動，重導向至首頁。

---

## 3. Jinja2 模板清單

所有模板皆存放在 `app/templates/` 中。

| 模板名稱 | 繼承自 | 說明 |
| :--- | :--- | :--- |
| `base.html` | (無) | 網站的共用骨架，包含 HTML 結構、`<head>`、導覽列 (Navbar) 與頁尾 (Footer) |
| `index.html` | `base.html` | 網站首頁，顯示所有活動列表 |
| `create_event.html` | `base.html` | 建立活動的表單頁面 |
| `event_detail.html` | `base.html` | 特定活動的詳情資訊、報名統計、名單列表以及報名表單 |
| `register_success.html`| `base.html` | 報名成功後的確認與感謝頁面 |
