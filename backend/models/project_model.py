from .db import execute_query 
from datetime import date, datetime 

PROJECT_FIELDS_LIST = ['project_id', 'project_name', 'description', 'status', 'start_date', 'end_date', 'manager_name']
PROJECT_FIELDS_DETAIL = ['project_id', 'project_name', 'description', 'status', 'start_date', 'end_date', 'manager_id', 'manager_name']

def format_project_row(row, keys):
    """将 SQL 元组转换为格式化字典。"""
    if not row or len(row) != len(keys):
        return None
        
    data = dict(zip(keys, row))
    for key in ['start_date', 'end_date']:
        if data.get(key) and isinstance(data[key], (date, datetime)):
            data[key] = data[key].isoformat()
        elif data.get(key) is None:
            data[key] = None
    return data

def get_project_list(search_query=None):
    """获取项目列表，支持 ID 或名称搜索。"""
    query = """
    SELECT p.project_id, p.project_name, p.description, p.status, 
           p.start_date, p.end_date, e.name AS manager_name
    FROM projects p
    LEFT JOIN employees e ON p.manager_id = e.employee_id
    """
    where_clauses, params = [], []
    
    if search_query:
        try:
            project_id = int(search_query)
            where_clauses.append("p.project_id = %s") 
            params.append(project_id)
        except ValueError:
            where_clauses.append("p.project_name ILIKE %s") 
            params.append(f"%{search_query}%")
            
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
        
    query += " ORDER BY p.project_id DESC;"
    rows = execute_query(query, tuple(params), fetch_all=True)
    
    return [formatted for row in (rows or []) if (formatted := format_project_row(row, PROJECT_FIELDS_LIST))]

def get_project_by_id(project_id):
    """获取单个项目详情。"""
    query = """
    SELECT p.project_id, p.project_name, p.description, p.status, 
           p.start_date, p.end_date, p.manager_id, e.name AS manager_name
    FROM projects p
    LEFT JOIN employees e ON p.manager_id = e.employee_id
    WHERE p.project_id = %s;
    """
    row = execute_query(query, (project_id,), fetch_one=True)
    return format_project_row(row, PROJECT_FIELDS_DETAIL) if row else None

def add_project(data):
    """创建新项目。"""
    def safe_get(key, default=None):
        val = data.get(key, default)
        return None if val in [None, ''] else val

    project_name = safe_get('project_name')
    if not project_name:
        raise ValueError("项目名称不能为空")

    query = """
    INSERT INTO projects (project_name, manager_id, description, status, start_date, end_date)
    VALUES (%s, %s, %s, %s, %s, %s) RETURNING project_id;
    """
    params = (
        project_name, safe_get('manager_id'), safe_get('description'),
        safe_get('status', '待开始') or '待开始', safe_get('start_date'), safe_get('end_date')
    )
    
    result = execute_query(query, params, fetch_one=True)
    if result: return result[0]
    raise Exception("数据库插入失败")

def update_project(project_id, data):
    """动态更新项目信息。"""
    allowed_fields = ['project_name', 'description', 'manager_id', 'status', 'start_date', 'end_date']
    set_clauses, params = [], []
    
    for key in allowed_fields:
        if key in data:
            val = data[key]
            set_clauses.append(f"{key} = %s")
            params.append(None if val in [None, ''] else val)
    
    if not set_clauses: return True
        
    query = f"UPDATE projects SET {', '.join(set_clauses)} WHERE project_id = %s;"
    params.append(project_id)
    
    rows_affected = execute_query(query, tuple(params))
    if rows_affected is False or rows_affected is None:
        raise Exception("数据库更新操作失败")
    return rows_affected > 0

def delete_project(project_id):
    """删除项目记录。"""
    query = "DELETE FROM projects WHERE project_id = %s;"
    
    if rows_affected is False or rows_affected is None:
        raise Exception("数据库删除操作失败")
    return rows_affected > 0