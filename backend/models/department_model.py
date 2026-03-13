from .db import execute_query

def format_department_data(rows):
    """将数据库行元组转换为字典格式，包含部门层级字段。"""
    if not rows:
        return []

    results = []
    keys = [
        'department_id', 'department_name', 'description', 
        'manager_id', 'manager_name', 'parent_id' 
    ] 
    
    for row in rows:
        if row and len(row) >= len(keys):
            data = dict(zip(keys, row[:len(keys)]))
            results.append(data)
            
    return results

def get_department_list(query=''):
    """获取部门列表，支持按 ID（数字）或名称（模糊）搜索。"""
    base_query = """
    SELECT 
        d.department_id, d.department_name, d.description, d.manager_id, 
        e.name AS manager_name, d.parent_id 
    FROM departments d
    LEFT JOIN employees e ON d.manager_id = e.employee_id
    """
    
    where_clauses = []
    params = []
    
    if query:
        try:
            department_id = int(query)
            where_clauses.append("d.department_id = %s") 
            params.append(department_id)
        except ValueError:
            where_clauses.append("d.department_name ILIKE %s") 
            params.append(f"%{query}%")

    if where_clauses:
        base_query += " WHERE " + " AND ".join(where_clauses)
        
    base_query += " ORDER BY d.department_id DESC;"
    
    rows = execute_query(base_query, tuple(params), fetch_all=True)
    return format_department_data(rows)

def add_department(data):
    """新增部门记录。"""
    query = """
    INSERT INTO departments (department_name, description, manager_id, parent_id)
    VALUES (%s, %s, %s, %s) RETURNING department_id;
    """
    manager_id = data.get('manager_id') if data.get('manager_id') not in [None, ''] else None
    parent_id = data.get('parent_id') if data.get('parent_id') not in [None, ''] else None
    
    params = (
        data.get('department_name'),
        data.get('description'),
        manager_id,
        parent_id
    )
    result = execute_query(query, params, fetch_one=True)
    return result[0] if result else None

def update_department(department_id, data):
    """动态构造 SQL 更新部门字段。"""
    set_clauses = []
    params = []
    allowed_fields = ['department_name', 'description', 'manager_id', 'parent_id']
    
    for field in allowed_fields:
        if field in data:
            value = data[field]
            if value in [None, '']:
                value = None
            set_clauses.append(f"{field} = %s") 
            params.append(value)

    if not set_clauses: 
        return True

    query = f"UPDATE departments SET {', '.join(set_clauses)} WHERE department_id = %s;"
    params.append(department_id)
    return execute_query(query, tuple(params))

def delete_department(department_id):
    """删除部门。"""
    query = "DELETE FROM departments WHERE department_id = %s;"
    return execute_query(query, (department_id,))

def get_department_by_id(department_id):
    """获取单个部门详情。"""
    query = """
    SELECT 
        d.department_id, d.department_name, d.description, d.manager_id, 
        e.name AS manager_name, d.parent_id 
    FROM departments d
    LEFT JOIN employees e ON d.manager_id = e.employee_id
    WHERE d.department_id = %s;
    """
    row = execute_query(query, (department_id,), fetch_one=True)
    formatted_data = format_department_data([row]) if row else []
    return formatted_data[0] if formatted_data else None

def get_employees_by_department_id(department_id):
    """获取指定部门下的所有员工及其状态。"""
    query = """
    SELECT 
        employee_id, name, position, email, phone, hire_date, status
    FROM employees
    WHERE department_id = %s
    ORDER BY employee_id;
    """
    rows = execute_query(query, (department_id,), fetch_all=True)
    if not rows:
        return []

    keys = ['employee_id', 'name', 'position', 'email', 'phone', 'hire_date', 'status']
    results = []
    for row in rows:
        if len(row) == len(keys):
            data = dict(zip(keys, row))
            if data.get('hire_date'):
                data['hire_date'] = str(data['hire_date'])
            results.append(data)
    return results