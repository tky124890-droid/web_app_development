"""
categories.py - 分類管理路由
Blueprint 名稱: categories
URL 前綴: /categories
"""
from flask import Blueprint, render_template, request, redirect, url_for

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


@categories_bp.route('/')
def index():
    """分類列表

    - 輸入: 無
    - 處理邏輯:
        1. 呼叫 Category.get_all() 取得所有分類
    - 輸出: 渲染 templates/categories/index.html
    """
    pass


@categories_bp.route('/', methods=['POST'])
def create():
    """建立分類

    - 輸入: 表單欄位 — name, type (income/expense)
    - 處理邏輯:
        1. 從 request.form 取得 name 與 type
        2. 驗證資料（名稱不得為空、type 須為 income 或 expense）
        3. 驗證通過：呼叫 Category.create(name, type_) 寫入 DB
        4. 重導向至 /categories
    - 錯誤處理:
        - 資料驗證失敗 → 重新渲染列表頁，帶入錯誤訊息
    """
    pass


@categories_bp.route('/<int:id>/edit')
def edit(id):
    """編輯分類頁面

    - 輸入: URL 參數 id（分類 ID）
    - 處理邏輯:
        1. 呼叫 Category.get_by_id(id) 取得特定分類
    - 輸出: 渲染 templates/categories/edit.html
    - 錯誤處理:
        - 找不到分類 → 回傳 404
    """
    pass


@categories_bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    """更新分類

    - 輸入: URL 參數 id；表單欄位 — name, type
    - 處理邏輯:
        1. 呼叫 Category.get_by_id(id) 確認分類存在
        2. 從 request.form 取得 name 與 type
        3. 驗證資料
        4. 驗證通過：呼叫 Category.update(id, name, type_) 更新 DB
        5. 重導向至 /categories
    - 錯誤處理:
        - 找不到分類 → 回傳 404
        - 資料驗證失敗 → 重新渲染編輯表單，帶入錯誤訊息
    """
    pass


@categories_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """刪除分類

    - 輸入: URL 參數 id
    - 處理邏輯:
        1. 呼叫 Category.get_by_id(id) 確認分類存在
        2. 呼叫 Category.delete(id) 刪除分類
        3. 重導向至 /categories
    - 錯誤處理:
        - 找不到分類 → 回傳 404
        - 分類仍有關聯的收支紀錄 → 顯示錯誤訊息，禁止刪除
    """
    pass
