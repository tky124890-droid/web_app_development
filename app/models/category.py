import datetime
from . import get_db_connection

class Category:
    @staticmethod
    def create(name, type_):
        conn = get_db_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.execute(
            'INSERT INTO categories (name, type, created_at) VALUES (?, ?, ?)',
            (name, type_, now)
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        categories = conn.execute('SELECT * FROM categories').fetchall()
        conn.close()
        return [dict(cat) for cat in categories]

    @staticmethod
    def get_by_id(category_id):
        conn = get_db_connection()
        category = conn.execute('SELECT * FROM categories WHERE id = ?', (category_id,)).fetchone()
        conn.close()
        return dict(category) if category else None

    @staticmethod
    def update(category_id, name, type_):
        conn = get_db_connection()
        conn.execute(
            'UPDATE categories SET name = ?, type = ? WHERE id = ?',
            (name, type_, category_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(category_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM categories WHERE id = ?', (category_id,))
        conn.commit()
        conn.close()
