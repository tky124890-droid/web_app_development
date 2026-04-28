"""
app/routes/__init__.py - 路由模組初始化
負責匯出所有 Blueprint，供 app/__init__.py 註冊使用。
"""
from app.routes.main import main_bp
from app.routes.transactions import transactions_bp
from app.routes.categories import categories_bp
from app.routes.accounts import accounts_bp
