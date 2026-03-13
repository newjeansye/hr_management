import sys
from .db import execute_query
from psycopg2 import errors as pg_errors
from decimal import Decimal

def get_project_members_by_id(project_id):
    """获取项目成员列表及其角色、贡献度和评分。"""
    query = """
    SELECT e.employee_id, e.name AS employee_name, pm.role, pm.contribution, pm.performance_rating  
    FROM public.project_members pm
    JOIN public.employees e ON pm.employee_id = e.employee_id
    WHERE pm.project_id = %s
    ORDER BY pm.role;
    """
    rows = execute_query(query, (project_id,), fetch_all=True)
    if not rows: return []

    keys = ['employee_id', 'employee_name', 'role', 'contribution', 'performance_rating']
    results = []
    for row in rows:
        if len(row) == len(keys):
            data = dict(zip(keys, row))
            # 处理 PostgreSQL Decimal 类型转换
            data['contribution'] = float(data['contribution']) if data.get('contribution') is not None else 0.0
            results.append(data)
    return results

def add_project_member(project_id, member_data):
    """向项目添加成员或更新现有成员信息 (Upsert)。"""
    member_id = member_data.get('employee_id')
    if not member_id:
        raise ValueError("employee_id 不能为空")
    
    try:
        member_id = int(member_id)
        role = member_data.get('role', '成员')
        contribution = float(member_data.get('contribution', 0.0))
        rating_value = member_data.get('performance_rating')
        performance_rating = float(rating_value) if rating_value not in [None, ''] else None
    except (TypeError, ValueError):
        raise ValueError("输入数据格式错误（ID需为整数，贡献/评分需为数字）")

    # 1. 尝试更新
    update_query = """
    UPDATE project_members 
    SET role = %s, contribution = %s, performance_rating = %s  
    WHERE project_id = %s AND employee_id = %s;
    """
    update_params = (role, contribution, performance_rating, project_id, member_id)
    update_result = execute_query(update_query, update_params) 
    
    if update_result is True or (isinstance(update_result, int) and update_result > 0):
        return True 
    
    # 2. 更新未成功（记录不存在），执行插入
    insert_query = """
    INSERT INTO project_members (project_id, employee_id, role, contribution, performance_rating)
    VALUES (%s, %s, %s, %s, %s);
    """
    insert_params = (project_id, member_id, role, contribution, performance_rating)

    try:
        execute_query(insert_query, insert_params)
        return True
    except pg_errors.ForeignKeyViolation:
        raise ValueError("提供的员工ID或项目ID在数据库中不存在")
    except Exception as e:
        if "duplicate key" in str(e).lower():
            raise Exception(f"成员 {member_id} 已存在但更新失败")
        raise Exception(f"数据库操作失败: {e}")

def is_member_in_project(project_id, employee_id):
    """检查员工是否为该项目成员。"""
    query = "SELECT 1 FROM project_members WHERE project_id = %s AND employee_id = %s;"
    return execute_query(query, (project_id, employee_id), fetch_one=True) is not None

def delete_project_member(project_id, employee_id):
    """从项目中移除成员。"""
    query = "DELETE FROM project_members WHERE project_id = %s AND employee_id = %s;"
    rows_affected = execute_query(query, (project_id, employee_id))
    return rows_affected > 0 if isinstance(rows_affected, int) else False