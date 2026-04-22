from . import get_db_connection
import sqlite3

class Event:
    @staticmethod
    def create(name, event_date, description=None):
        """
        新增一筆活動記錄
        參數:
            name (str): 活動名稱
            event_date (str): 活動日期
            description (str): 活動描述
        回傳:
            int: 新增的活動 ID
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO events (name, event_date, description) VALUES (?, ?, ?)',
                (name, event_date, description)
            )
            event_id = cursor.lastrowid
            conn.commit()
            return event_id
        except sqlite3.Error as e:
            print(f"Error creating event: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有活動記錄
        回傳:
            list: 包含所有活動的 sqlite3.Row 列表
        """
        try:
            conn = get_db_connection()
            events = conn.execute('SELECT * FROM events ORDER BY event_date ASC').fetchall()
            return events
        except sqlite3.Error as e:
            print(f"Error getting all events: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_by_id(event_id):
        """
        取得單筆活動記錄
        參數:
            event_id (int): 活動 ID
        回傳:
            sqlite3.Row: 單筆活動資料，若找不到則回傳 None
        """
        try:
            conn = get_db_connection()
            event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
            return event
        except sqlite3.Error as e:
            print(f"Error getting event by id: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def update(event_id, data):
        """
        更新一筆活動記錄
        參數:
            event_id (int): 活動 ID
            data (dict): 包含 name, event_date, description 的字典
        回傳:
            bool: 是否更新成功
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE events SET name = ?, event_date = ?, description = ? WHERE id = ?',
                (data.get('name'), data.get('event_date'), data.get('description'), event_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating event: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete(event_id):
        """
        刪除一筆活動記錄
        參數:
            event_id (int): 活動 ID
        回傳:
            bool: 是否刪除成功
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM events WHERE id = ?', (event_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting event: {e}")
            return False
        finally:
            if conn:
                conn.close()
