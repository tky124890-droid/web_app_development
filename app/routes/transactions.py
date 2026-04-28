"""
transactions.py - 收支紀錄管理路由
Blueprint 名稱: transactions
URL 前綴: /transactions
"""
from flask import Blueprint, render_template, request, redirect, url_for

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')


@transactions_bp.route('/')
def index():
    """收支紀錄列表

    - 輸入: 無
    - 處理邏輯:
        1. 呼叫 Transaction.get_all() 取得所有收支紀錄
           （已含 JOIN 的分類名稱與帳戶名稱）
    - 輸出: 渲染 templates/transactions/index.html
    """
    pass


@transactions_bp.route('/new')
def new():
    """新增收支頁面

    - 輸入: 無
    - 處理邏輯:
        1. 呼叫 Category.get_all() 取得所有分類（供下拉選單）
        2. 呼叫 Account.get_all() 取得所有帳戶（供下拉選單）
    - 輸出: 渲染 templates/transactions/new.html
    """
    pass


@transactions_bp.route('/', methods=['POST'])
def create():
    """建立收支紀錄

    - 輸入: 表單欄位 — amount, type, date, description, category_id, account_id
    - 處理邏輯:
        1. 從 request.form 取得所有欄位
        2. 驗證資料（金額須大於 0、日期格式正確、type 須為 income 或 expense）
        3. 驗證通過：呼叫 Transaction.create(...) 寫入 DB
        4. 重導向至 /transactions
    - 錯誤處理:
        - 資料驗證失敗 → 重新渲染表單，帶入錯誤訊息
    """
    pass


@transactions_bp.route('/<int:id>/edit')
def edit(id):
    """編輯收支頁面

    - 輸入: URL 參數 id（交易紀錄 ID）
    - 處理邏輯:
        1. 呼叫 Transaction.get_by_id(id) 取得特定紀錄
        2. 呼叫 Category.get_all() 取得所有分類
        3. 呼叫 Account.get_all() 取得所有帳戶
    - 輸出: 渲染 templates/transactions/edit.html
    - 錯誤處理:
        - 找不到紀錄 → 回傳 404
    """
    pass


@transactions_bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    """更新收支紀錄

    - 輸入: URL 參數 id；表單欄位 — amount, type, date, description, category_id, account_id
    - 處理邏輯:
        1. 呼叫 Transaction.get_by_id(id) 確認紀錄存在
        2. 從 request.form 取得所有欄位
        3. 驗證資料
        4. 驗證通過：呼叫 Transaction.update(id, ...) 更新 DB
        5. 重導向至 /transactions
    - 錯誤處理:
        - 找不到紀錄 → 回傳 404
        - 資料驗證失敗 → 重新渲染編輯表單，帶入錯誤訊息
    """
    pass


@transactions_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """刪除收支紀錄

    - 輸入: URL 參數 id
    - 處理邏輯:
        1. 呼叫 Transaction.get_by_id(id) 確認紀錄存在
        2. 呼叫 Transaction.delete(id) 刪除紀錄
        3. 重導向至 /transactions
    - 錯誤處理:
        - 找不到紀錄 → 回傳 404
    """
    pass
