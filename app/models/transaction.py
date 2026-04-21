import datetime
from . import get_db_connection

class Transaction:
    @staticmethod
    def create(amount, type_, date, description, category_id, account_id):
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
        conn.close()
        return last_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        query = '''
            SELECT t.*, c.name as category_name, a.name as account_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            LEFT JOIN accounts a ON t.account_id = a.id
            ORDER BY t.date DESC, t.id DESC
        '''
        transactions = conn.execute(query).fetchall()
        conn.close()
        return [dict(t) for t in transactions]

    @staticmethod
    def get_by_id(transaction_id):
        conn = get_db_connection()
        transaction = conn.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,)).fetchone()
        conn.close()
        return dict(transaction) if transaction else None

    @staticmethod
    def update(transaction_id, amount, type_, date, description, category_id, account_id):
        conn = get_db_connection()
        conn.execute(
            '''UPDATE transactions 
               SET amount = ?, type = ?, date = ?, description = ?, category_id = ?, account_id = ?
               WHERE id = ?''',
            (amount, type_, date, description, category_id, account_id, transaction_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(transaction_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
        conn.commit()
        conn.close()
