import psycopg2
from ..config import Config

def get_db_connection():
    """获取数据库连接，手动控制事务提交。"""
    try:
        conn = psycopg2.connect(**Config.DB_CONFIG)
        conn.autocommit = False 
        return conn
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

def execute_query(sql, params=None, fetch_one=False, fetch_all=False):
    """ vt
    通用 SQL 执行器。
    处理连接生命周期、SQL 注入防护、事务控制及结果返回。
    """
    conn = get_db_connection()
    if conn is None:
        return None if (fetch_one or fetch_all) else False

    cur = None
    try:
        cur = conn.cursor()
        cur.execute(sql, params)

        # 判定操作类型
        is_write = sql.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE'))
        
        # 处理结果抓取
        result = None
        if fetch_one:
            result = cur.fetchone()
        elif fetch_all:
            result = cur.fetchall()

        # 事务管理：写入操作必须提交
        if is_write:
            conn.commit()
        
        # 返回优先级：结果集 > 受影响行数 > 成功标识
        if fetch_one or fetch_all:
            return result
        return cur.rowcount if is_write else True

    except Exception as e:
        print(f"数据库操作失败: {e}")
        if conn:
            conn.rollback()
        return None if (fetch_one or fetch_all) else False
        
    finally:
        if cur: cur.close()
        if conn: conn.close()