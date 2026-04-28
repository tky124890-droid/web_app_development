"""
app/models/transaction.py - 收支紀錄模型
負責 transactions 資料表的所有 CRUD 操作。
"""
import datetime
import sqlite3
from . import get_db_connection


class Transaction:
    """收支紀錄的資料模型，提供新增、查詢、更新與刪除功能。"""

    @staticmethod
    def create(amount, type_, date, description, category_id, account_id):
        """新增一筆收支紀錄。

        Args:
            amount (float): 交易金額，須大於 0。
            type_ (str): 收支類型，'income'（收入）或 'expense'（支出）。
            date (str): 交易日期，格式為 YYYY-MM-DD。
            description (str): 備註說明，可為空字串。
            category_id (int): 分類 ID，關聯至 categories 資料表。
            account_id (int): 帳戶 ID，關聯至 accounts 資料表。

        Returns:
            int: 新建紀錄的 ID。

        Raises:
            sqlite3.Error: 當資料庫寫入失敗時。
            ValueError: 當金額不合法時。
        """
        if amount <= 0:
            raise ValueError('金額必須大於 0')
        if type_ not in ('income', 'expense'):
            raise ValueError('類型必須為 income 或 expense')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.datetime.now().isoformat()
            cursor.execute(
                '''INSERT INTO transactions 
                   (amount, type, date, description, category_id, account_id, created_at) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (amount, type_, date, description, category_id, account_id, now)
            )
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        except sqlite3.Error as e:
            print(f'[Transaction Error] 新增失敗: {e}')
            raise
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """取得所有收支紀錄，包含分類名稱與帳戶名稱。

        透過 LEFT JOIN 關聯 categories 與 accounts 資料表，
        結果依交易日期與 ID 降冪排列（最新的在前面）。

        Returns:
            list[dict]: 所有收支紀錄的字典列表。
        """
        try:
            conn = get_db_connection()
            query = '''
                SELECT t.*, c.name as category_name, a.name as account_name
                FROM transactions t
                LEFT JOIN categories c ON t.category_id = c.id
                LEFT JOIN accounts a ON t.account_id = a.id
                ORDER BY t.date DESC, t.id DESC
            '''
            transactions = conn.execute(query).fetchall()
            return [dict(t) for t in transactions]
        except sqlite3.Error as e:
            print(f'[Transaction Error] 查詢全部失敗: {e}')
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(transaction_id):
        """根據 ID 取得單筆收支紀錄。

        Args:
            transaction_id (int): 收支紀錄的 ID。

        Returns:
            dict or None: 收支紀錄的字典，找不到時回傳 None。
        """
        try:
            conn = get_db_connection()
            transaction = conn.execute(
                'SELECT * FROM transactions WHERE id = ?',
                (transaction_id,)
            ).fetchone()
            return dict(transaction) if transaction else None
        except sqlite3.Error as e:
            print(f'[Transaction Error] 查詢 ID={transaction_id} 失敗: {e}')
            return None
        finally:
            conn.close()

    @staticmethod
    def update(transaction_id, amount, type_, date, description, category_id, account_id):
        """更新一筆收支紀錄。

        Args:
            transaction_id (int): 要更新的紀錄 ID。
            amount (float): 新的交易金額，須大於 0。
            type_ (str): 新的收支類型，'income' 或 'expense'。
            date (str): 新的交易日期，格式為 YYYY-MM-DD。
            description (str): 新的備註說明。
            category_id (int): 新的分類 ID。
            account_id (int): 新的帳戶 ID。

        Raises:
            sqlite3.Error: 當資料庫更新失敗時。
            ValueError: 當金額或類型不合法時。
        """
        if amount <= 0:
            raise ValueError('金額必須大於 0')
        if type_ not in ('income', 'expense'):
            raise ValueError('類型必須為 income 或 expense')

        try:
            conn = get_db_connection()
            conn.execute(
                '''UPDATE transactions 
                   SET amount = ?, type = ?, date = ?, description = ?, category_id = ?, account_id = ?
                   WHERE id = ?''',
                (amount, type_, date, description, category_id, account_id, transaction_id)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f'[Transaction Error] 更新 ID={transaction_id} 失敗: {e}')
            raise
        finally:
            conn.close()

    @staticmethod
    def delete(transaction_id):
        """刪除一筆收支紀錄。

        Args:
            transaction_id (int): 要刪除的紀錄 ID。

        Raises:
            sqlite3.Error: 當資料庫刪除失敗時。
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'DELETE FROM transactions WHERE id = ?',
                (transaction_id,)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f'[Transaction Error] 刪除 ID={transaction_id} 失敗: {e}')
            raise
        finally:
            conn.close()

    @staticmethod
    def get_by_account(account_id):
        """取得特定帳戶的所有收支紀錄。

        Args:
            account_id (int): 帳戶 ID。

        Returns:
            list[dict]: 該帳戶的所有收支紀錄。
        """
        try:
            conn = get_db_connection()
            transactions = conn.execute(
                'SELECT * FROM transactions WHERE account_id = ? ORDER BY date DESC',
                (account_id,)
            ).fetchall()
            return [dict(t) for t in transactions]
        except sqlite3.Error as e:
            print(f'[Transaction Error] 查詢帳戶 ID={account_id} 的紀錄失敗: {e}')
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_category(category_id):
        """取得特定分類的所有收支紀錄。

        Args:
            category_id (int): 分類 ID。

        Returns:
            list[dict]: 該分類的所有收支紀錄。
        """
        try:
            conn = get_db_connection()
            transactions = conn.execute(
                'SELECT * FROM transactions WHERE category_id = ? ORDER BY date DESC',
                (category_id,)
            ).fetchall()
            return [dict(t) for t in transactions]
        except sqlite3.Error as e:
            print(f'[Transaction Error] 查詢分類 ID={category_id} 的紀錄失敗: {e}')
            return []
        finally:
            conn.close()
