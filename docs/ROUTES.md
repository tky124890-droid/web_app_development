# 個人記帳簿系統 - 路由設計文件 (Routes)

本文件定義系統所有 Flask 路由的 URL 路徑、HTTP 方法、對應模板與處理邏輯，作為程式碼實作的依據。

---

## 1. 路由總覽表格

### 首頁 / 儀表板

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁儀表板 | GET | `/` | `templates/index.html` | 顯示總餘額、各帳戶餘額、收支圖表 |

### 收支紀錄 (Transactions)

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 收支紀錄列表 | GET | `/transactions` | `templates/transactions/index.html` | 顯示所有收支紀錄列表 |
| 新增收支頁面 | GET | `/transactions/new` | `templates/transactions/new.html` | 顯示新增收支的填寫表單 |
| 建立收支紀錄 | POST | `/transactions` | — | 接收表單資料，存入 DB，重導向至列表 |
| 編輯收支頁面 | GET | `/transactions/<id>/edit` | `templates/transactions/edit.html` | 顯示編輯特定收支的表單 |
| 更新收支紀錄 | POST | `/transactions/<id>/update` | — | 接收修改資料，更新 DB，重導向至列表 |
| 刪除收支紀錄 | POST | `/transactions/<id>/delete` | — | 刪除特定收支紀錄，重導向至列表 |

### 分類管理 (Categories)

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 分類列表 | GET | `/categories` | `templates/categories/index.html` | 顯示所有預設與自訂分類 |
| 建立分類 | POST | `/categories` | — | 接收表單資料，新增分類，重導向至列表 |
| 編輯分類頁面 | GET | `/categories/<id>/edit` | `templates/categories/edit.html` | 顯示編輯分類的表單 |
| 更新分類 | POST | `/categories/<id>/update` | — | 接收修改資料，更新 DB，重導向至列表 |
| 刪除分類 | POST | `/categories/<id>/delete` | — | 刪除分類，重導向至列表 |

### 帳戶管理 (Accounts)

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 帳戶列表 | GET | `/accounts` | `templates/accounts/index.html` | 顯示所有帳戶及其餘額 |
| 建立帳戶 | POST | `/accounts` | — | 接收表單資料，新增帳戶，重導向至列表 |
| 編輯帳戶頁面 | GET | `/accounts/<id>/edit` | `templates/accounts/edit.html` | 顯示編輯帳戶的表單 |
| 更新帳戶 | POST | `/accounts/<id>/update` | — | 接收修改資料，更新 DB，重導向至列表 |
| 刪除帳戶 | POST | `/accounts/<id>/delete` | — | 刪除帳戶，重導向至列表 |

---

## 2. 每個路由的詳細說明

### 2.1 首頁儀表板

#### `GET /`

- **輸入**：無
- **處理邏輯**：
  1. 呼叫 `Account.get_all()` 取得所有帳戶
  2. 呼叫 `Transaction.get_all()` 取得所有收支紀錄
  3. 計算總餘額 = 各帳戶初始餘額 + 所有收入 - 所有支出
  4. 計算當月收入總計與支出總計
  5. 按分類彙總支出比例（供圓餅圖使用）
- **輸出**：渲染 `templates/index.html`，傳入 `total_balance`、`monthly_income`、`monthly_expense`、`expense_by_category`、`accounts`
- **錯誤處理**：無特殊錯誤情境

---

### 2.2 收支紀錄 (Transactions)

#### `GET /transactions`

- **輸入**：無
- **處理邏輯**：
  1. 呼叫 `Transaction.get_all()` 取得所有收支紀錄（已含 JOIN 的分類名稱與帳戶名稱）
- **輸出**：渲染 `templates/transactions/index.html`，傳入 `transactions`
- **錯誤處理**：無特殊錯誤情境

#### `GET /transactions/new`

- **輸入**：無
- **處理邏輯**：
  1. 呼叫 `Category.get_all()` 取得所有分類（供下拉選單）
  2. 呼叫 `Account.get_all()` 取得所有帳戶（供下拉選單）
- **輸出**：渲染 `templates/transactions/new.html`，傳入 `categories`、`accounts`
- **錯誤處理**：無特殊錯誤情境

#### `POST /transactions`

- **輸入**：表單欄位 — `amount`、`type`（income/expense）、`date`、`description`、`category_id`、`account_id`
- **處理邏輯**：
  1. 從 `request.form` 取得所有欄位
  2. 驗證資料（金額須大於 0、日期格式正確、type 必須是 income 或 expense）
  3. 驗證通過：呼叫 `Transaction.create(...)` 寫入 DB
  4. 重導向至 `/transactions`
- **輸出**：`redirect(url_for('transactions.index'))`
- **錯誤處理**：
  - 資料驗證失敗 → 重新渲染 `transactions/new.html`，帶入錯誤訊息與使用者已填的資料

#### `GET /transactions/<id>/edit`

- **輸入**：URL 參數 `id`（交易紀錄 ID）
- **處理邏輯**：
  1. 呼叫 `Transaction.get_by_id(id)` 取得特定紀錄
  2. 呼叫 `Category.get_all()` 取得所有分類
  3. 呼叫 `Account.get_all()` 取得所有帳戶
- **輸出**：渲染 `templates/transactions/edit.html`，傳入 `transaction`、`categories`、`accounts`
- **錯誤處理**：
  - 找不到紀錄 → 回傳 404 錯誤頁面

#### `POST /transactions/<id>/update`

- **輸入**：URL 參數 `id`；表單欄位 — `amount`、`type`、`date`、`description`、`category_id`、`account_id`
- **處理邏輯**：
  1. 呼叫 `Transaction.get_by_id(id)` 確認紀錄存在
  2. 從 `request.form` 取得所有欄位
  3. 驗證資料
  4. 驗證通過：呼叫 `Transaction.update(id, ...)` 更新 DB
  5. 重導向至 `/transactions`
- **輸出**：`redirect(url_for('transactions.index'))`
- **錯誤處理**：
  - 找不到紀錄 → 回傳 404
  - 資料驗證失敗 → 重新渲染 `transactions/edit.html`，帶入錯誤訊息

#### `POST /transactions/<id>/delete`

- **輸入**：URL 參數 `id`
- **處理邏輯**：
  1. 呼叫 `Transaction.get_by_id(id)` 確認紀錄存在
  2. 呼叫 `Transaction.delete(id)` 刪除紀錄
  3. 重導向至 `/transactions`
- **輸出**：`redirect(url_for('transactions.index'))`
- **錯誤處理**：
  - 找不到紀錄 → 回傳 404

---

### 2.3 分類管理 (Categories)

#### `GET /categories`

- **輸入**：無
- **處理邏輯**：
  1. 呼叫 `Category.get_all()` 取得所有分類
- **輸出**：渲染 `templates/categories/index.html`，傳入 `categories`
- **錯誤處理**：無特殊錯誤情境

#### `POST /categories`

- **輸入**：表單欄位 — `name`、`type`（income/expense）
- **處理邏輯**：
  1. 從 `request.form` 取得 `name` 與 `type`
  2. 驗證資料（名稱不得為空、type 必須是 income 或 expense）
  3. 驗證通過：呼叫 `Category.create(name, type_)` 寫入 DB
  4. 重導向至 `/categories`
- **輸出**：`redirect(url_for('categories.index'))`
- **錯誤處理**：
  - 資料驗證失敗 → 重新渲染 `categories/index.html`，帶入錯誤訊息

#### `GET /categories/<id>/edit`

- **輸入**：URL 參數 `id`（分類 ID）
- **處理邏輯**：
  1. 呼叫 `Category.get_by_id(id)` 取得特定分類
- **輸出**：渲染 `templates/categories/edit.html`，傳入 `category`
- **錯誤處理**：
  - 找不到分類 → 回傳 404

#### `POST /categories/<id>/update`

- **輸入**：URL 參數 `id`；表單欄位 — `name`、`type`
- **處理邏輯**：
  1. 呼叫 `Category.get_by_id(id)` 確認分類存在
  2. 從 `request.form` 取得 `name` 與 `type`
  3. 驗證資料
  4. 驗證通過：呼叫 `Category.update(id, name, type_)` 更新 DB
  5. 重導向至 `/categories`
- **輸出**：`redirect(url_for('categories.index'))`
- **錯誤處理**：
  - 找不到分類 → 回傳 404
  - 資料驗證失敗 → 重新渲染 `categories/edit.html`，帶入錯誤訊息

#### `POST /categories/<id>/delete`

- **輸入**：URL 參數 `id`
- **處理邏輯**：
  1. 呼叫 `Category.get_by_id(id)` 確認分類存在
  2. 呼叫 `Category.delete(id)` 刪除分類
  3. 重導向至 `/categories`
- **輸出**：`redirect(url_for('categories.index'))`
- **錯誤處理**：
  - 找不到分類 → 回傳 404
  - 分類仍有關聯的收支紀錄 → 顯示錯誤訊息，禁止刪除

---

### 2.4 帳戶管理 (Accounts)

#### `GET /accounts`

- **輸入**：無
- **處理邏輯**：
  1. 呼叫 `Account.get_all()` 取得所有帳戶
  2. 對每個帳戶，計算目前餘額 = 初始餘額 + 該帳戶收入總計 - 該帳戶支出總計
- **輸出**：渲染 `templates/accounts/index.html`，傳入 `accounts`（含計算後餘額）
- **錯誤處理**：無特殊錯誤情境

#### `POST /accounts`

- **輸入**：表單欄位 — `name`、`initial_balance`
- **處理邏輯**：
  1. 從 `request.form` 取得 `name` 與 `initial_balance`
  2. 驗證資料（名稱不得為空、初始餘額須為有效數字）
  3. 驗證通過：呼叫 `Account.create(name, initial_balance)` 寫入 DB
  4. 重導向至 `/accounts`
- **輸出**：`redirect(url_for('accounts.index'))`
- **錯誤處理**：
  - 資料驗證失敗 → 重新渲染 `accounts/index.html`，帶入錯誤訊息

#### `GET /accounts/<id>/edit`

- **輸入**：URL 參數 `id`（帳戶 ID）
- **處理邏輯**：
  1. 呼叫 `Account.get_by_id(id)` 取得特定帳戶
- **輸出**：渲染 `templates/accounts/edit.html`，傳入 `account`
- **錯誤處理**：
  - 找不到帳戶 → 回傳 404

#### `POST /accounts/<id>/update`

- **輸入**：URL 參數 `id`；表單欄位 — `name`、`initial_balance`
- **處理邏輯**：
  1. 呼叫 `Account.get_by_id(id)` 確認帳戶存在
  2. 從 `request.form` 取得 `name` 與 `initial_balance`
  3. 驗證資料
  4. 驗證通過：呼叫 `Account.update(id, name, initial_balance)` 更新 DB
  5. 重導向至 `/accounts`
- **輸出**：`redirect(url_for('accounts.index'))`
- **錯誤處理**：
  - 找不到帳戶 → 回傳 404
  - 資料驗證失敗 → 重新渲染 `accounts/edit.html`，帶入錯誤訊息

#### `POST /accounts/<id>/delete`

- **輸入**：URL 參數 `id`
- **處理邏輯**：
  1. 呼叫 `Account.get_by_id(id)` 確認帳戶存在
  2. 呼叫 `Account.delete(id)` 刪除帳戶
  3. 重導向至 `/accounts`
- **輸出**：`redirect(url_for('accounts.index'))`
- **錯誤處理**：
  - 找不到帳戶 → 回傳 404
  - 帳戶仍有關聯的收支紀錄 → 顯示錯誤訊息，禁止刪除

---

## 3. Jinja2 模板清單

所有模板皆繼承 `base.html`，使用 `{% extends "base.html" %}` 語法。

| 模板路徑 | 繼承自 | 說明 |
| --- | --- | --- |
| `templates/base.html` | — | 共用版型（導覽列、頁尾、CSS/JS 引入） |
| `templates/index.html` | `base.html` | 首頁儀表板（總餘額、收支圓餅圖、月報表） |
| `templates/transactions/index.html` | `base.html` | 收支紀錄列表頁 |
| `templates/transactions/new.html` | `base.html` | 新增收支表單頁 |
| `templates/transactions/edit.html` | `base.html` | 編輯收支表單頁 |
| `templates/categories/index.html` | `base.html` | 分類管理列表頁（含內嵌新增表單） |
| `templates/categories/edit.html` | `base.html` | 編輯分類表單頁 |
| `templates/accounts/index.html` | `base.html` | 帳戶管理列表頁（含內嵌新增表單） |
| `templates/accounts/edit.html` | `base.html` | 編輯帳戶表單頁 |

---

## 4. Blueprint 架構

路由使用 Flask Blueprint 機制進行模組化分組，每個功能模組一個 Blueprint：

| Blueprint 名稱 | URL 前綴 | 檔案路徑 | 說明 |
| --- | --- | --- | --- |
| `main` | `/` | `app/routes/main.py` | 首頁儀表板 |
| `transactions` | `/transactions` | `app/routes/transactions.py` | 收支紀錄 CRUD |
| `categories` | `/categories` | `app/routes/categories.py` | 分類管理 CRUD |
| `accounts` | `/accounts` | `app/routes/accounts.py` | 帳戶管理 CRUD |
