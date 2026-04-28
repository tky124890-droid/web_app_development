"""
app/models/account.py - 帳戶模型
負責 accounts 資料表的所有 CRUD 操作。
"""
import datetime
import sqlite3
from . import get_db_connection


class Account:
    """帳戶/錢包的資料模型，提供新增、查詢、更新與刪除功能。"""

    @staticmethod
    def create(name, initial_balance=0.0):
        """新增一個帳戶。

        Args:
            name (str): 帳戶名稱，如「現金」、「中國信託」。
            initial_balance (float): 初始餘額，預設為 0.0。

        Returns:
            int: 新建帳戶的 ID。

        Raises:
            sqlite3.Error: 當資料庫寫入失敗時。
            ValueError: 當名稱為空時。
        """
        if not name or not name.strip():
            raise ValueError('帳戶名稱不得為空')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.datetime.now().isoformat()
            cursor.execute(
                'INSERT INTO accounts (name, initial_balance, created_at) VALUES (?, ?, ?)',
                (name.strip(), float(initial_balance), now)
            )
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        except sqlite3.Error as e:
            print(f'[Account Error] 新增失敗: {e}')
            raise
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """取得所有帳戶。

        Returns:
            list[dict]: 所有帳戶的字典列表，依建立時間排序。
        """
        try:
            conn = get_db_connection()
            accounts = conn.execute(
                'SELECT * FROM accounts ORDER BY created_at'
            ).fetchall()
            return [dict(acc) for acc in accounts]
        except sqlite3.Error as e:
            print(f'[Account Error] 查詢全部失敗: {e}')
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(account_id):
        """根據 ID 取得單筆帳戶。

        Args:
            account_id (int): 帳戶的 ID。

        Returns:
            dict or None: 帳戶的字典，找不到時回傳 None。
        """
        try:
            conn = get_db_connection()
            account = conn.execute(
                'SELECT * FROM accounts WHERE id = ?',
                (account_id,)
            ).fetchone()
            return dict(account) if account else None
        except sqlite3.Error as e:
            print(f'[Account Error] 查詢 ID={account_id} 失敗: {e}')
            return None
        finally:
            conn.close()

    @staticmethod
    def get_balance(account_id):
        """計算帳戶的目前餘額。

        目前餘額 = 初始餘額 + 該帳戶收入總計 - 該帳戶支出總計。

        Args:
            account_id (int): 帳戶的 ID。

        Returns:
            float: 帳戶目前餘額；若帳戶不存在，回傳 0.0。
        """
        try:
            conn = get_db_connection()
            # 取得初始餘額
            account = conn.execute(
                'SELECT initial_balance FROM accounts WHERE id = ?',
                (account_id,)
            ).fetchone()
            if not account:
                return 0.0

            initial_balance = account['initial_balance']

            # 計算收入總計
            income_row = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) as total FROM transactions WHERE account_id = ? AND type = 'income'",
                (account_id,)
            ).fetchone()

            # 計算支出總計
            expense_row = conn.execute(
                "SELECT COALESCE(SUM(amount), 0) as total FROM transactions WHERE account_id = ? AND type = 'expense'",
                (account_id,)
            ).fetchone()

            return initial_balance + income_row['total'] - expense_row['total']
        except sqlite3.Error as e:
            print(f'[Account Error] 計算帳戶 ID={account_id} 餘額失敗: {e}')
            return 0.0
        finally:
            conn.close()

    @staticmethod
    def update(account_id, name, initial_balance):
        """更新一筆帳戶。

        Args:
            account_id (int): 要更新的帳戶 ID。
            name (str): 新的帳戶名稱。
            initial_balance (float): 新的初始餘額。

        Raises:
            sqlite3.Error: 當資料庫更新失敗時。
            ValueError: 當名稱為空時。
        """
        if not name or not name.strip():
            raise ValueError('帳戶名稱不得為空')

        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE accounts SET name = ?, initial_balance = ? WHERE id = ?',
                (name.strip(), float(initial_balance), account_id)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f'[Account Error] 更新 ID={account_id} 失敗: {e}')
            raise
        finally:
            conn.close()

    @staticmethod
    def delete(account_id):
        """刪除一筆帳戶。

        注意：若該帳戶仍有關聯的收支紀錄，因外鍵約束將會刪除失敗。

        Args:
            account_id (int): 要刪除的帳戶 ID。

        Raises:
            sqlite3.Error: 當資料庫刪除失敗時（如外鍵約束衝突）。
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'DELETE FROM accounts WHERE id = ?',
                (account_id,)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f'[Account Error] 刪除 ID={account_id} 失敗: {e}')
            raise
        finally:
            conn.close()
