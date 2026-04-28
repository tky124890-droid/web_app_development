"""
accounts.py - 帳戶管理路由
Blueprint 名稱: accounts
URL 前綴: /accounts
"""
from flask import Blueprint, render_template, request, redirect, url_for

accounts_bp = Blueprint('accounts', __name__, url_prefix='/accounts')


@accounts_bp.route('/')
def index():
    """帳戶列表

    - 輸入: 無
    - 處理邏輯:
        1. 呼叫 Account.get_all() 取得所有帳戶
        2. 對每個帳戶，計算目前餘額 = 初始餘額 + 該帳戶收入總計 - 該帳戶支出總計
    - 輸出: 渲染 templates/accounts/index.html
    """
    pass


@accounts_bp.route('/', methods=['POST'])
def create():
    """建立帳戶

    - 輸入: 表單欄位 — name, initial_balance
    - 處理邏輯:
        1. 從 request.form 取得 name 與 initial_balance
        2. 驗證資料（名稱不得為空、初始餘額須為有效數字）
        3. 驗證通過：呼叫 Account.create(name, initial_balance) 寫入 DB
        4. 重導向至 /accounts
    - 錯誤處理:
        - 資料驗證失敗 → 重新渲染列表頁，帶入錯誤訊息
    """
    pass


@accounts_bp.route('/<int:id>/edit')
def edit(id):
    """編輯帳戶頁面

    - 輸入: URL 參數 id（帳戶 ID）
    - 處理邏輯:
        1. 呼叫 Account.get_by_id(id) 取得特定帳戶
    - 輸出: 渲染 templates/accounts/edit.html
    - 錯誤處理:
        - 找不到帳戶 → 回傳 404
    """
    pass


@accounts_bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    """更新帳戶

    - 輸入: URL 參數 id；表單欄位 — name, initial_balance
    - 處理邏輯:
        1. 呼叫 Account.get_by_id(id) 確認帳戶存在
        2. 從 request.form 取得 name 與 initial_balance
        3. 驗證資料
        4. 驗證通過：呼叫 Account.update(id, name, initial_balance) 更新 DB
        5. 重導向至 /accounts
    - 錯誤處理:
        - 找不到帳戶 → 回傳 404
        - 資料驗證失敗 → 重新渲染編輯表單，帶入錯誤訊息
    """
    pass


@accounts_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """刪除帳戶

    - 輸入: URL 參數 id
    - 處理邏輯:
        1. 呼叫 Account.get_by_id(id) 確認帳戶存在
        2. 呼叫 Account.delete(id) 刪除帳戶
        3. 重導向至 /accounts
    - 錯誤處理:
        - 找不到帳戶 → 回傳 404
        - 帳戶仍有關聯的收支紀錄 → 顯示錯誤訊息，禁止刪除
    """
    pass
