"""
main.py - 首頁儀表板路由
Blueprint 名稱: main
URL 前綴: /
"""
from datetime import datetime
from flask import Blueprint, render_template

from app.models.account import Account
from app.models.transaction import Transaction
from app.models.category import Category

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """首頁儀表板

    顯示總餘額、當月收支統計與按分類彙總的支出比例。
    """
    # 1. 取得所有帳戶與收支紀錄
    accounts = Account.get_all()
    transactions = Transaction.get_all()

    # 2. 計算各帳戶目前餘額
    for account in accounts:
        account['balance'] = Account.get_balance(account['id'])

    # 3. 計算總餘額
    total_balance = sum(acc['balance'] for acc in accounts)

    # 4. 計算當月收入與支出
    now = datetime.now()
    current_month = now.strftime('%Y-%m')
    monthly_income = 0.0
    monthly_expense = 0.0

    for tx in transactions:
        if tx['date'].startswith(current_month):
            if tx['type'] == 'income':
                monthly_income += tx['amount']
            else:
                monthly_expense += tx['amount']

    # 5. 按分類彙總當月支出比例（供圓餅圖使用）
    expense_by_category = {}
    for tx in transactions:
        if tx['date'].startswith(current_month) and tx['type'] == 'expense':
            cat_name = tx.get('category_name', '未分類') or '未分類'
            expense_by_category[cat_name] = expense_by_category.get(cat_name, 0) + tx['amount']

    return render_template(
        'index.html',
        total_balance=total_balance,
        monthly_income=monthly_income,
        monthly_expense=monthly_expense,
        expense_by_category=expense_by_category,
        accounts=accounts,
        current_month=now.strftime('%Y 年 %m 月')
    )
