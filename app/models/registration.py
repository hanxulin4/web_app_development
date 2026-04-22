from . import get_db_connection
import sqlite3

class Registration:
    @staticmethod
    def create(event_id, name, gender, contact_info=None):
        """
        新增一筆報名記錄
        參數:
            event_id (int): 關聯的活動 ID
            name (str): 報名者姓名
            gender (str): 性別
            contact_info (str, optional): 聯絡資訊
        回傳:
            int: 新增的報名 ID，若失敗則回傳 None
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO registrations (event_id, name, gender, contact_info) VALUES (?, ?, ?, ?)',
                (event_id, name, gender, contact_info)
            )
            reg_id = cursor.lastrowid
            conn.commit()
            return reg_id
        except sqlite3.Error as e:
            print(f"Error creating registration: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有報名記錄 (一般依據活動查詢較多，此供整體管理使用)
        回傳:
            list: 包含所有報名的 sqlite3.Row 列表
        """
        try:
            conn = get_db_connection()
            registrations = conn.execute('SELECT * FROM registrations ORDER BY created_at ASC').fetchall()
            return registrations
        except sqlite3.Error as e:
            print(f"Error getting all registrations: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_by_id(reg_id):
        """
        取得單筆報名記錄
        參數:
            reg_id (int): 報名 ID
        回傳:
            sqlite3.Row: 單筆報名資料，若找不到則回傳 None
        """
        try:
            conn = get_db_connection()
            registration = conn.execute('SELECT * FROM registrations WHERE id = ?', (reg_id,)).fetchone()
            return registration
        except sqlite3.Error as e:
            print(f"Error getting registration by id: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def update(reg_id, data):
        """
        更新一筆報名記錄
        參數:
            reg_id (int): 報名 ID
            data (dict): 包含 name, gender, contact_info 的字典
        回傳:
            bool: 是否更新成功
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE registrations SET name = ?, gender = ?, contact_info = ? WHERE id = ?',
                (data.get('name'), data.get('gender'), data.get('contact_info'), reg_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating registration: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete(reg_id):
        """
        刪除一筆報名記錄
        參數:
            reg_id (int): 報名 ID
        回傳:
            bool: 是否刪除成功
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM registrations WHERE id = ?', (reg_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting registration: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_by_event(event_id):
        """
        取得特定活動的所有報名名單
        參數:
            event_id (int): 關聯的活動 ID
        回傳:
            list: 名單列表
        """
        try:
            conn = get_db_connection()
            registrations = conn.execute(
                'SELECT * FROM registrations WHERE event_id = ? ORDER BY created_at ASC',
                (event_id,)
            ).fetchall()
            return registrations
        except sqlite3.Error as e:
            print(f"Error getting registrations by event: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_stats_by_event(event_id):
        """
        取得特定活動的報名統計資訊（男女人數與總數）
        參數:
            event_id (int): 關聯的活動 ID
        回傳:
            dict: 包含 total, male, female 人數的字典
        """
        try:
            conn = get_db_connection()
            total = conn.execute('SELECT COUNT(*) as count FROM registrations WHERE event_id = ?', (event_id,)).fetchone()['count']
            male_count = conn.execute('SELECT COUNT(*) as count FROM registrations WHERE event_id = ? AND gender = "男"', (event_id,)).fetchone()['count']
            female_count = conn.execute('SELECT COUNT(*) as count FROM registrations WHERE event_id = ? AND gender = "女"', (event_id,)).fetchone()['count']
            return {'total': total, 'male': male_count, 'female': female_count}
        except sqlite3.Error as e:
            print(f"Error getting stats: {e}")
            return {'total': 0, 'male': 0, 'female': 0}
        finally:
            if conn:
                conn.close()
