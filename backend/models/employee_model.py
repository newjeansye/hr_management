from .db import execute_query
from decimal import Decimal 
from datetime import date, datetime 

EMPLOYEE_FIELDS = [
    'employee_id', 'name', 'gender', 'birth_date', 'id_card', 
    'phone', 'email', 'hire_date', 'position', 'job_level', 
    'department_id', 'status' 
]
EMPLOYEE_JOINED_FIELDS = EMPLOYEE_FIELDS + ['department_name']
EMPLOYEE_INSERT_FIELDS = [
    'name', 'gender', 'birth_date', 'id_card', 
    'phone', 'email', 'hire_date', 'position', 'job_level', 
    'department_id', 'status' 
]
EMPLOYEE_UPDATE_FIELDS = EMPLOYEE_INSERT_FIELDS

def format_employee_data(rows):
    """统一格式化员工行数据为字典列表。"""
    if not rows: return []
    results = []
    keys = EMPLOYEE_JOINED_FIELDS
    
    for row in rows:
        if row and len(row) == len(keys): 
            data = dict(zip(keys, row))
            for key in ['birth_date', 'hire_date']:
                if data.get(key): data[key] = str(data[key]) 
            results.append(data)
    return results

def get_select_sql():
    """生成包含 e.* 属性和 d.department_name 的 SQL 片段。"""
    e_fields = [f'e.{field}' for field in EMPLOYEE_FIELDS if field != 'employee_id']
    select_fields = ['e.employee_id'] + e_fields + ['d.department_name']
    return ', '.join(select_fields)

def get_employee_list(query=''):
    """获取员工列表，支持 ID 精确搜索或姓名/邮箱模糊搜索。"""
    select_fields = get_select_sql()
    base_query = f"SELECT {select_fields} FROM employees e LEFT JOIN departments d ON e.department_id = d.department_id"
    
    where_clauses = []
    params = []
    
    if query:
        try:
            employee_id = int(query)
            where_clauses.append("e.employee_id = %s") 
            params.append(employee_id)
        except ValueError:
            where_clauses.append("(e.name ILIKE %s OR e.email ILIKE %s)") 
            search_pattern = f"%{query}%"
            params.extend([search_pattern, search_pattern])

    if where_clauses:
        base_query += " WHERE " + " AND ".join(where_clauses)
    base_query += " ORDER BY e.employee_id;"
    
    raw_results = execute_query(base_query, tuple(params), fetch_all=True)
    return format_employee_data(raw_results)

def get_employee_by_id(employee_id):
    """根据 ID 获取单个员工详细信息。"""
    query = f"SELECT {get_select_sql()} FROM employees e LEFT JOIN departments d ON e.department_id = d.department_id WHERE e.employee_id = %s;"
    row = execute_query(query, (employee_id,), fetch_one=True)
    if not row: return None
    formatted = format_employee_data([row])
    return formatted[0] if formatted else None

def add_employee(data):
    """新增员工，返回新生成的 employee_id。"""
    insert_fields = [field for field in EMPLOYEE_INSERT_FIELDS if field != 'status']
    query = f"INSERT INTO employees ({', '.join(insert_fields)}) VALUES ({', '.join(['%s'] * len(insert_fields))}) RETURNING employee_id;"
    
    params = (
        data.get('name'), data.get('gender'),
        str(data.get('birth_date')) if data.get('birth_date') else None,
        data.get('id_card'), data.get('phone'), data.get('email'),
        str(data.get('hire_date')) if data.get('hire_date') else None,
        data.get('position'), data.get('job_level'),
        int(data.get('department_id')) if data.get('department_id') else None
    )
    
    result = execute_query(query, params, fetch_one=True)
    return result[0] if result else None

def update_employee(employee_id, data):
    """动态构建 SQL 更新员工信息。"""
    set_clauses = []
    params = []
    
    for field in EMPLOYEE_UPDATE_FIELDS:
        if field in data:
            value = data[field]
            if value == '': value = None
            if field == 'department_id': value = int(value) if value is not None else None
            if field in ['birth_date', 'hire_date'] and value: value = str(value)
            
            set_clauses.append(f"{field} = %s") 
            params.append(value)

    if not set_clauses: return True

    query = f"UPDATE employees SET {', '.join(set_clauses)} WHERE employee_id = %s;"
    params.append(employee_id)
    rows_affected = execute_query(query, tuple(params))
    return rows_affected > 0

def delete_employee(employee_id):
    """物理删除员工。"""
    query = "DELETE FROM employees WHERE employee_id = %s;"
    return execute_query(query, (employee_id,))

def get_projects_by_employee_id(employee_id):
    """查询员工参与的项目及其在项目中的角色。"""
    query = """
    SELECT p.project_id, p.project_name, p.status, p.start_date, p.end_date,
           pm.role, pm.contribution, e_mgr.name AS manager_name
    FROM project_members pm
    JOIN projects p ON pm.project_id = p.project_id
    LEFT JOIN employees e_mgr ON p.manager_id = e_mgr.employee_id
    WHERE pm.employee_id = %s ORDER BY p.project_id DESC;
    """
    rows = execute_query(query, (employee_id,), fetch_all=True)
    if not rows: return []

    keys = ['project_id', 'project_name', 'status', 'start_date', 'end_date', 'role', 'contribution', 'manager_name']
    results = []
    for row in rows:
        if len(row) == len(keys):
            data = dict(zip(keys, row))
            for key in ['start_date', 'end_date']:
                if data.get(key): data[key] = str(data[key])
            results.append(data)
    return results