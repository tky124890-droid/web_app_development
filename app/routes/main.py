"""
main.py - 首頁儀表板路由
Blueprint 名稱: main
URL 前綴: /
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """首頁儀表板

    - 輸入: 無
    - 處理邏輯:
        1. 呼叫 Account.get_all() 取得所有帳戶
        2. 呼叫 Transaction.get_all() 取得所有收支紀錄
        3. 計算總餘額 = 各帳戶初始餘額 + 所有收入 - 所有支出
        4. 計算當月收入總計與支出總計
        5. 按分類彙總支出比例（供圓餅圖使用）
    - 輸出: 渲染 templates/index.html
    """
    pass
