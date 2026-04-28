"""
app/models/__init__.py - 資料庫連線與初始化模組
負責管理 SQLite 資料庫的連線建立與資料表結構初始化。
"""
import sqlite3
import os

# 資料庫檔案將儲存於專案根目錄下的 instance/database.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(INSTANCE_DIR, 'database.db')


def get_db_connection():
    """取得 SQLite 資料庫連線。

    自動建立 instance 目錄（若不存在），並啟用外鍵約束。
    回傳的連線使用 sqlite3.Row 作為 row_factory，
    讓查詢結果可以透過欄位名稱（key）取值。

    Returns:
        sqlite3.Connection: 資料庫連線物件。

    Raises:
        sqlite3.Error: 當資料庫連線失敗時拋出。
    """
    try:
        if not os.path.exists(INSTANCE_DIR):
            os.makedirs(INSTANCE_DIR)

        conn = sqlite3.connect(DB_PATH)
        # 讓回傳的資料具有 dict 的特性，方便透過 key 存取欄位
        conn.row_factory = sqlite3.Row
        # 啟用外鍵約束，確保 FOREIGN KEY 關聯生效
        conn.execute('PRAGMA foreign_keys = ON')
        return conn
    except sqlite3.Error as e:
        print(f'[DB Error] 無法連線到資料庫: {e}')
        raise


def init_db():
    """初始化資料庫表結構。

    讀取 database/schema.sql 並執行建表語法。
    使用 IF NOT EXISTS，因此重複執行不會覆蓋既有資料。

    Raises:
        FileNotFoundError: 當 schema.sql 檔案不存在時。
        sqlite3.Error: 當 SQL 執行失敗時。
    """
    schema_path = os.path.join(BASE_DIR, 'database', 'schema.sql')
    if not os.path.exists(schema_path):
        print(f'[DB Warning] 找不到 schema 檔案: {schema_path}')
        return

    try:
        conn = get_db_connection()
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print('[DB Info] 資料庫初始化完成。')
    except sqlite3.Error as e:
        print(f'[DB Error] 資料庫初始化失敗: {e}')
        raise
