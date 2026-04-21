import datetime
from . import get_db_connection

class Account:
    @staticmethod
    def create(name, initial_balance=0.0):
        conn = get_db_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO accounts (name, initial_balance, created_at) VALUES (?, ?, ?)',
            (name, initial_balance, now)
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        accounts = conn.execute('SELECT * FROM accounts').fetchall()
        conn.close()
        return [dict(acc) for acc in accounts]

    @staticmethod
    def get_by_id(account_id):
        conn = get_db_connection()
        account = conn.execute('SELECT * FROM accounts WHERE id = ?', (account_id,)).fetchone()
        conn.close()
        return dict(account) if account else None

    @staticmethod
    def update(account_id, name, initial_balance):
        conn = get_db_connection()
        conn.execute(
            'UPDATE accounts SET name = ?, initial_balance = ? WHERE id = ?',
            (name, initial_balance, account_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(account_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM accounts WHERE id = ?', (account_id,))
        conn.commit()
        conn.close()
