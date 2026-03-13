from flask import Blueprint, jsonify, request
from ..models.department_model import (
    get_department_list, 
    add_department, 
    update_department, 
    delete_department, 
    get_department_by_id,
    get_employees_by_department_id 
) 

department_bp = Blueprint('department_bp', __name__)

@department_bp.route('/departments', methods=['GET'])
def list_departments():
    """获取所有部门列表，支持通过 'query' 进行搜索。"""
    search_query = request.args.get('query', default='') 
    data = get_department_list(search_query) 
    return jsonify({"code": 200, "data": data or []})

@department_bp.route('/departments', methods=['POST'])
def create_department():
    """创建新部门。"""
    data = request.get_json()
    if not data or not data.get('department_name'):
        return jsonify({"code": 400, "message": "缺少必要字段: department_name"}), 400
        
    department_id = add_department(data)
    
    if department_id:
        return jsonify({"code": 201, "message": "部门创建成功", "department_id": department_id}), 201
    else:
        return jsonify({"code": 500, "message": "部门创建失败"}), 500

@department_bp.route('/departments/<int:department_id>', methods=['GET'])
def get_department_api(department_id):
    """根据 ID 获取单个部门详情。"""
    data = get_department_by_id(department_id)
    if data:
        return jsonify({"code": 200, "data": data})
    else:
        return jsonify({"code": 404, "message": f"部门 ID:{department_id} 不存在"}), 404

@department_bp.route('/departments/<int:department_id>', methods=['PUT'])
def update_department_api(department_id):
    """更新部门信息。"""
    data = request.get_json()
    if update_department(department_id, data):
        return jsonify({"code": 200, "message": f"部门 ID:{department_id} 更新成功"})
    else:
        return jsonify({"code": 500, "message": f"部门更新失败或 ID:{department_id} 不存在"}), 500

@department_bp.route('/departments/<int:department_id>', methods=['DELETE'])
def delete_department_api(department_id):
    """删除部门。"""
    if delete_department(department_id):
        return '', 204
    else:
        return jsonify({"code": 500, "message": "部门删除失败或 ID 不存在"}), 500

@department_bp.route('/departments/<int:department_id>/employees', methods=['GET'])
def list_department_employees_api(department_id):
    """获取指定部门的所有员工列表。"""
    if not get_department_by_id(department_id):
        return jsonify({"code": 404, "message": f"部门 ID:{department_id} 不存在"}), 404
        
    employees_list = get_employees_by_department_id(department_id)
    return jsonify({"code": 200, "data": employees_list or []})