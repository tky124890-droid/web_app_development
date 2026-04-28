"""
accounts.py - 帳戶管理路由
Blueprint 名稱: accounts
URL 前綴: /accounts
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

from app.models.account import Account
from app.models.transaction import Transaction

accounts_bp = Blueprint('accounts', __name__, url_prefix='/accounts')


@accounts_bp.route('/')
def index():
    """帳戶列表

    顯示所有帳戶及其計算後的目前餘額（含內嵌新增表單）。
    """
    accounts = Account.get_all()

    # 為每個帳戶計算目前餘額
    for account in accounts:
        account['balance'] = Account.get_balance(account['id'])

    return render_template('accounts/index.html', accounts=accounts)


@accounts_bp.route('/', methods=['POST'])
def create():
    """建立帳戶

    接收表單資料、驗證後新增帳戶，成功則重導向至列表頁。
    """
    name = request.form.get('name', '').strip()
    initial_balance = request.form.get('initial_balance', '0').strip()

    # 驗證資料
    errors = []
    if not name:
        errors.append('請輸入帳戶名稱。')

    try:
        initial_balance_val = float(initial_balance)
    except ValueError:
        errors.append('初始餘額必須為有效數字。')
        initial_balance_val = 0.0

    # 驗證失敗
    if errors:
        for error in errors:
            flash(error, 'danger')
        accounts = Account.get_all()
        for account in accounts:
            account['balance'] = Account.get_balance(account['id'])
        return render_template('accounts/index.html', accounts=accounts, form=request.form)

    # 驗證通過 → 寫入 DB
    try:
        Account.create(name, initial_balance_val)
        flash('帳戶新增成功！', 'success')
    except Exception as e:
        flash(f'新增失敗：{e}', 'danger')

    return redirect(url_for('accounts.index'))


@accounts_bp.route('/<int:id>/edit')
def edit(id):
    """編輯帳戶頁面

    顯示編輯帳戶的表單，若找不到帳戶回傳 404。
    """
    account = Account.get_by_id(id)
    if not account:
        abort(404)

    return render_template('accounts/edit.html', account=account)


@accounts_bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    """更新帳戶

    接收修改資料、驗證後更新 DB，成功則重導向至列表頁。
    """
    account = Account.get_by_id(id)
    if not account:
        abort(404)

    name = request.form.get('name', '').strip()
    initial_balance = request.form.get('initial_balance', '0').strip()

    # 驗證資料
    errors = []
    if not name:
        errors.append('請輸入帳戶名稱。')

    try:
        initial_balance_val = float(initial_balance)
    except ValueError:
        errors.append('初始餘額必須為有效數字。')
        initial_balance_val = 0.0

    # 驗證失敗
    if errors:
        for error in errors:
            flash(error, 'danger')
        return render_template('accounts/edit.html', account=account, form=request.form)

    # 驗證通過 → 更新 DB
    try:
        Account.update(id, name, initial_balance_val)
        flash('帳戶更新成功！', 'success')
    except Exception as e:
        flash(f'更新失敗：{e}', 'danger')

    return redirect(url_for('accounts.index'))


@accounts_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """刪除帳戶

    刪除帳戶，若仍有關聯的收支紀錄則禁止刪除。
    """
    account = Account.get_by_id(id)
    if not account:
        abort(404)

    # 檢查是否有關聯的收支紀錄
    related_transactions = Transaction.get_by_account(id)
    if related_transactions:
        flash(f'無法刪除「{account["name"]}」，仍有 {len(related_transactions)} 筆關聯的收支紀錄。', 'danger')
        return redirect(url_for('accounts.index'))

    try:
        Account.delete(id)
        flash('帳戶已刪除。', 'success')
    except Exception as e:
        flash(f'刪除失敗：{e}', 'danger')

    return redirect(url_for('accounts.index'))
