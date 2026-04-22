import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """建立資料庫連線並回傳 connection 物件"""
    conn = sqlite3.connect(DATABASE_PATH)
    # 將回傳結果設定為類似 dict 的形式，方便用欄位名稱取值
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化資料庫表結構"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = f.read()
    
    conn = get_db_connection()
    conn.executescript(schema)
    conn.commit()
    conn.close()
