from . import get_db_connection

class Event:
    @staticmethod
    def create(name, event_date, description=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO events (name, event_date, description) VALUES (?, ?, ?)',
            (name, event_date, description)
        )
        event_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return event_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        events = conn.execute('SELECT * FROM events ORDER BY event_date ASC').fetchall()
        conn.close()
        return events

    @staticmethod
    def get_by_id(event_id):
        conn = get_db_connection()
        event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
        conn.close()
        return event
