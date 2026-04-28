"""
app/__init__.py - Flask 應用程式工廠
負責初始化 Flask 實例、載入設定、註冊 Blueprint 與初始化資料庫
"""
import os
from flask import Flask


def create_app():
    """建立並設定 Flask 應用程式實例"""
    app = Flask(__name__)

    # 載入密鑰設定（用於 session 與 flash message）
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # 初始化資料庫（建立資料表，若尚未存在）
    from app.models import init_db
    init_db()

    # 註冊 Blueprint
    from app.routes.main import main_bp
    from app.routes.transactions import transactions_bp
    from app.routes.categories import categories_bp
    from app.routes.accounts import accounts_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(accounts_bp)

    return app
