"""
app/models/category.py - 分類模型
負責 categories 資料表的所有 CRUD 操作。
"""
import datetime
import sqlite3
from . import get_db_connection


class Category:
    """收支分類的資料模型，提供新增、查詢、更新與刪除功能。"""

    @staticmethod
    def create(name, type_):
        """新增一筆分類。

        Args:
            name (str): 分類名稱，如「餐飲」、「薪水」。
            type_ (str): 分類類型，'income'（收入）或 'expense'（支出）。

        Returns:
            int: 新建分類的 ID。

        Raises:
            sqlite3.Error: 當資料庫寫入失敗時。
            ValueError: 當名稱為空或類型不合法時。
        """
        if not name or not name.strip():
            raise ValueError('分類名稱不得為空')
        if type_ not in ('income', 'expense'):
            raise ValueError('分類類型必須為 income 或 expense')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.datetime.now().isoformat()
            cursor.execute(
                'INSERT INTO categories (name, type, created_at) VALUES (?, ?, ?)',
                (name.strip(), type_, now)
            )
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        except sqlite3.Error as e:
            print(f'[Category Error] 新增失敗: {e}')
            raise
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """取得所有分類。

        Returns:
            list[dict]: 所有分類的字典列表，依名稱排序。
        """
        try:
            conn = get_db_connection()
            categories = conn.execute(
                'SELECT * FROM categories ORDER BY type, name'
            ).fetchall()
            return [dict(cat) for cat in categories]
        except sqlite3.Error as e:
            print(f'[Category Error] 查詢全部失敗: {e}')
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(category_id):
        """根據 ID 取得單筆分類。

        Args:
            category_id (int): 分類的 ID。

        Returns:
            dict or None: 分類的字典，找不到時回傳 None。
        """
        try:
            conn = get_db_connection()
            category = conn.execute(
                'SELECT * FROM categories WHERE id = ?',
                (category_id,)
            ).fetchone()
            return dict(category) if category else None
        except sqlite3.Error as e:
            print(f'[Category Error] 查詢 ID={category_id} 失敗: {e}')
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_type(type_):
        """根據類型取得分類列表。

        Args:
            type_ (str): 分類類型，'income' 或 'expense'。

        Returns:
            list[dict]: 指定類型的分類列表。
        """
        try:
            conn = get_db_connection()
            categories = conn.execute(
                'SELECT * FROM categories WHERE type = ? ORDER BY name',
                (type_,)
            ).fetchall()
            return [dict(cat) for cat in categories]
        except sqlite3.Error as e:
            print(f'[Category Error] 查詢類型={type_} 失敗: {e}')
            return []
        finally:
            conn.close()

    @staticmethod
    def update(category_id, name, type_):
        """更新一筆分類。

        Args:
            category_id (int): 要更新的分類 ID。
            name (str): 新的分類名稱。
            type_ (str): 新的分類類型，'income' 或 'expense'。

        Raises:
            sqlite3.Error: 當資料庫更新失敗時。
            ValueError: 當名稱為空或類型不合法時。
        """
        if not name or not name.strip():
            raise ValueError('分類名稱不得為空')
        if type_ not in ('income', 'expense'):
            raise ValueError('分類類型必須為 income 或 expense')

        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE categories SET name = ?, type = ? WHERE id = ?',
                (name.strip(), type_, category_id)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f'[Category Error] 更新 ID={category_id} 失敗: {e}')
            raise
        finally:
            conn.close()

    @staticmethod
    def delete(category_id):
        """刪除一筆分類。

        注意：若該分類仍有關聯的收支紀錄，因外鍵約束將會刪除失敗。

        Args:
            category_id (int): 要刪除的分類 ID。

        Raises:
            sqlite3.Error: 當資料庫刪除失敗時（如外鍵約束衝突）。
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'DELETE FROM categories WHERE id = ?',
                (category_id,)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f'[Category Error] 刪除 ID={category_id} 失敗: {e}')
            raise
        finally:
            conn.close()
