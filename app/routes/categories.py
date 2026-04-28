"""
categories.py - 分類管理路由
Blueprint 名稱: categories
URL 前綴: /categories
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

from app.models.category import Category
from app.models.transaction import Transaction

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


@categories_bp.route('/')
def index():
    """分類列表

    顯示所有預設與自訂分類（含內嵌新增表單）。
    """
    categories = Category.get_all()
    return render_template('categories/index.html', categories=categories)


@categories_bp.route('/', methods=['POST'])
def create():
    """建立分類

    接收表單資料、驗證後新增分類，成功則重導向至列表頁。
    """
    name = request.form.get('name', '').strip()
    type_ = request.form.get('type', '').strip()

    # 驗證資料
    errors = []
    if not name:
        errors.append('請輸入分類名稱。')

    if type_ not in ('income', 'expense'):
        errors.append('請選擇分類類型（收入或支出）。')

    # 驗證失敗
    if errors:
        for error in errors:
            flash(error, 'danger')
        categories = Category.get_all()
        return render_template('categories/index.html', categories=categories, form=request.form)

    # 驗證通過 → 寫入 DB
    try:
        Category.create(name, type_)
        flash('分類新增成功！', 'success')
    except Exception as e:
        flash(f'新增失敗：{e}', 'danger')

    return redirect(url_for('categories.index'))


@categories_bp.route('/<int:id>/edit')
def edit(id):
    """編輯分類頁面

    顯示編輯分類的表單，若找不到分類回傳 404。
    """
    category = Category.get_by_id(id)
    if not category:
        abort(404)

    return render_template('categories/edit.html', category=category)


@categories_bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    """更新分類

    接收修改資料、驗證後更新 DB，成功則重導向至列表頁。
    """
    category = Category.get_by_id(id)
    if not category:
        abort(404)

    name = request.form.get('name', '').strip()
    type_ = request.form.get('type', '').strip()

    # 驗證資料
    errors = []
    if not name:
        errors.append('請輸入分類名稱。')

    if type_ not in ('income', 'expense'):
        errors.append('請選擇分類類型（收入或支出）。')

    # 驗證失敗
    if errors:
        for error in errors:
            flash(error, 'danger')
        return render_template('categories/edit.html', category=category, form=request.form)

    # 驗證通過 → 更新 DB
    try:
        Category.update(id, name, type_)
        flash('分類更新成功！', 'success')
    except Exception as e:
        flash(f'更新失敗：{e}', 'danger')

    return redirect(url_for('categories.index'))


@categories_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """刪除分類

    刪除分類，若仍有關聯的收支紀錄則禁止刪除。
    """
    category = Category.get_by_id(id)
    if not category:
        abort(404)

    # 檢查是否有關聯的收支紀錄
    related_transactions = Transaction.get_by_category(id)
    if related_transactions:
        flash(f'無法刪除「{category["name"]}」，仍有 {len(related_transactions)} 筆關聯的收支紀錄。', 'danger')
        return redirect(url_for('categories.index'))

    try:
        Category.delete(id)
        flash('分類已刪除。', 'success')
    except Exception as e:
        flash(f'刪除失敗：{e}', 'danger')

    return redirect(url_for('categories.index'))
