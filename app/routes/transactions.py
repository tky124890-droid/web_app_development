"""
transactions.py - 收支紀錄管理路由
Blueprint 名稱: transactions
URL 前綴: /transactions
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

from app.models.transaction import Transaction
from app.models.category import Category
from app.models.account import Account

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')


@transactions_bp.route('/')
def index():
    """收支紀錄列表

    顯示所有收支紀錄（含分類名稱與帳戶名稱）。
    """
    transactions = Transaction.get_all()
    return render_template('transactions/index.html', transactions=transactions)


@transactions_bp.route('/new')
def new():
    """新增收支頁面

    顯示新增收支的填寫表單，載入分類與帳戶下拉選單。
    """
    categories = Category.get_all()
    accounts = Account.get_all()
    return render_template('transactions/new.html', categories=categories, accounts=accounts)


@transactions_bp.route('/', methods=['POST'])
def create():
    """建立收支紀錄

    接收表單資料、驗證後存入 DB，成功則重導向至列表頁。
    """
    # 從表單取得資料
    amount = request.form.get('amount', '').strip()
    type_ = request.form.get('type', '').strip()
    date = request.form.get('date', '').strip()
    description = request.form.get('description', '').strip()
    category_id = request.form.get('category_id', '').strip()
    account_id = request.form.get('account_id', '').strip()

    # 驗證資料
    errors = []
    if not amount:
        errors.append('請輸入金額。')
    else:
        try:
            amount_val = float(amount)
            if amount_val <= 0:
                errors.append('金額必須大於 0。')
        except ValueError:
            errors.append('金額必須為有效數字。')

    if type_ not in ('income', 'expense'):
        errors.append('請選擇收支類型。')

    if not date:
        errors.append('請選擇日期。')

    if not category_id:
        errors.append('請選擇分類。')

    if not account_id:
        errors.append('請選擇帳戶。')

    # 驗證失敗 → 重新渲染表單
    if errors:
        for error in errors:
            flash(error, 'danger')
        categories = Category.get_all()
        accounts = Account.get_all()
        return render_template(
            'transactions/new.html',
            categories=categories,
            accounts=accounts,
            form=request.form
        )

    # 驗證通過 → 寫入 DB
    try:
        Transaction.create(
            amount=float(amount),
            type_=type_,
            date=date,
            description=description,
            category_id=int(category_id),
            account_id=int(account_id)
        )
        flash('收支紀錄新增成功！', 'success')
    except Exception as e:
        flash(f'新增失敗：{e}', 'danger')

    return redirect(url_for('transactions.index'))


@transactions_bp.route('/<int:id>/edit')
def edit(id):
    """編輯收支頁面

    顯示編輯特定收支的表單，若找不到紀錄回傳 404。
    """
    transaction = Transaction.get_by_id(id)
    if not transaction:
        abort(404)

    categories = Category.get_all()
    accounts = Account.get_all()
    return render_template(
        'transactions/edit.html',
        transaction=transaction,
        categories=categories,
        accounts=accounts
    )


@transactions_bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    """更新收支紀錄

    接收修改資料、驗證後更新 DB，成功則重導向至列表頁。
    """
    # 確認紀錄存在
    transaction = Transaction.get_by_id(id)
    if not transaction:
        abort(404)

    # 從表單取得資料
    amount = request.form.get('amount', '').strip()
    type_ = request.form.get('type', '').strip()
    date = request.form.get('date', '').strip()
    description = request.form.get('description', '').strip()
    category_id = request.form.get('category_id', '').strip()
    account_id = request.form.get('account_id', '').strip()

    # 驗證資料
    errors = []
    if not amount:
        errors.append('請輸入金額。')
    else:
        try:
            amount_val = float(amount)
            if amount_val <= 0:
                errors.append('金額必須大於 0。')
        except ValueError:
            errors.append('金額必須為有效數字。')

    if type_ not in ('income', 'expense'):
        errors.append('請選擇收支類型。')

    if not date:
        errors.append('請選擇日期。')

    if not category_id:
        errors.append('請選擇分類。')

    if not account_id:
        errors.append('請選擇帳戶。')

    # 驗證失敗 → 重新渲染編輯表單
    if errors:
        for error in errors:
            flash(error, 'danger')
        categories = Category.get_all()
        accounts = Account.get_all()
        return render_template(
            'transactions/edit.html',
            transaction=transaction,
            categories=categories,
            accounts=accounts,
            form=request.form
        )

    # 驗證通過 → 更新 DB
    try:
        Transaction.update(
            transaction_id=id,
            amount=float(amount),
            type_=type_,
            date=date,
            description=description,
            category_id=int(category_id),
            account_id=int(account_id)
        )
        flash('收支紀錄更新成功！', 'success')
    except Exception as e:
        flash(f'更新失敗：{e}', 'danger')

    return redirect(url_for('transactions.index'))


@transactions_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """刪除收支紀錄

    刪除特定收支紀錄，重導向至列表頁。
    """
    transaction = Transaction.get_by_id(id)
    if not transaction:
        abort(404)

    try:
        Transaction.delete(id)
        flash('收支紀錄已刪除。', 'success')
    except Exception as e:
        flash(f'刪除失敗：{e}', 'danger')

    return redirect(url_for('transactions.index'))
