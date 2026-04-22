from . import get_db_connection

class Registration:
    @staticmethod
    def create(event_id, name, gender, contact_info=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO registrations (event_id, name, gender, contact_info) VALUES (?, ?, ?, ?)',
            (event_id, name, gender, contact_info)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_event(event_id):
        """取得特定活動的所有報名名單"""
        conn = get_db_connection()
        registrations = conn.execute(
            'SELECT * FROM registrations WHERE event_id = ? ORDER BY created_at ASC',
            (event_id,)
        ).fetchall()
        conn.close()
        return registrations

    @staticmethod
    def get_stats_by_event(event_id):
        """取得特定活動的報名統計資訊（男女人數與總數）"""
        conn = get_db_connection()
        
        # 取得總人數
        total = conn.execute(
            'SELECT COUNT(*) as count FROM registrations WHERE event_id = ?', 
            (event_id,)
        ).fetchone()['count']
        
        # 取得男女人數
        male_count = conn.execute(
            'SELECT COUNT(*) as count FROM registrations WHERE event_id = ? AND gender = "男"', 
            (event_id,)
        ).fetchone()['count']
        
        female_count = conn.execute(
            'SELECT COUNT(*) as count FROM registrations WHERE event_id = ? AND gender = "女"', 
            (event_id,)
        ).fetchone()['count']
        
        conn.close()
        
        return {
            'total': total,
            'male': male_count,
            'female': female_count
        }
