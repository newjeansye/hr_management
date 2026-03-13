from flask import Blueprint, jsonify, request
from ..models.employee_model import (
    get_employee_list, 
    add_employee, 
    update_employee, 
    delete_employee,
    get_employee_by_id,
    get_projects_by_employee_id
)

employee_bp = Blueprint('employee_bp', __name__)

@employee_bp.route('/employees', methods=['GET'])
def list_employees():
    """获取员工列表，支持通过 'query' 参数搜索。"""
    search_query = request.args.get('query', default='') 
    data = get_employee_list(search_query) 
    return jsonify({"code": 200, "data": data or []})

@employee_bp.route('/employees', methods=['POST'])
def create_employee():
    """创建新员工。"""
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"code": 400, "message": "缺少必要字段: name"}), 400
        
    employee_id = add_employee(data)
    if employee_id:
        return jsonify({"code": 201, "message": "员工创建成功", "employee_id": employee_id}), 201
    else:
        return jsonify({"code": 500, "message": "员工创建失败"}), 500

@employee_bp.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee_api(employee_id):
    """根据 ID 获取单个员工详情。"""
    data = get_employee_by_id(employee_id)
    if data:
        return jsonify({"code": 200, "data": data})
    else:
        return jsonify({"code": 404, "message": f"员工 ID:{employee_id} 不存在"}), 404

@employee_bp.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee_api(employee_id):
    """更新员工信息。"""
    data = request.get_json()
    try:
        if update_employee(employee_id, data):
            return jsonify({"code": 200, "message": f"员工 ID:{employee_id} 更新成功"})
        else:
            return jsonify({"code": 404, "message": f"员工 ID:{employee_id} 不存在或数据无变化"}), 404
    except Exception as e:
        return jsonify({"code": 500, "message": f"员工更新失败: {str(e)}"}), 500

@employee_bp.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee_api(employee_id):
    """删除员工。"""
    if delete_employee(employee_id):
        return '', 204
    else:
        return jsonify({"code": 500, "message": "员工删除失败或 ID 不存在"}), 500

@employee_bp.route('/employees/<int:employee_id>/projects', methods=['GET'])
def list_employee_projects_api(employee_id):
    """获取指定员工参与的所有项目列表。"""
    projects_list = get_projects_by_employee_id(employee_id)
    return jsonify({"code": 200, "data": projects_list or []})