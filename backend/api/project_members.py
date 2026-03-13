from flask import Blueprint, jsonify, request
from backend.models.project_model import get_project_by_id 
from backend.models.project_members_model import (
    get_project_members_by_id,
    add_project_member,
    delete_project_member,
    is_member_in_project
)

project_members_bp = Blueprint('project_members_bp', __name__)

@project_members_bp.route('/projects/<int:project_id>/members', methods=['GET'])
def list_project_members_api(project_id):
    """获取指定项目的所有成员列表。"""
    if not get_project_by_id(project_id):
        return jsonify({"code": 404, "message": f"项目 ID:{project_id} 不存在"}), 404
        
    members_list = get_project_members_by_id(project_id)
    return jsonify({"code": 200, "data": members_list or []})

@project_members_bp.route('/projects/<int:project_id>/members', methods=['POST'])
def add_project_member_api(project_id):
    """为指定项目添加新成员或更新现有成员信息。"""
    try:
        data = request.get_json()
        if not data or not data.get('employee_id'):
            return jsonify({"code": 400, "message": "缺少必要字段: employee_id"}), 400
        
        if add_project_member(project_id, data):
            return jsonify({
                "code": 201, 
                "message": f"项目 {project_id} 成员 {data['employee_id']} 已处理"
            }), 201
        
        return jsonify({"code": 500, "message": "操作失败"}), 500

    except ValueError as e:
        return jsonify({"code": 400, "message": str(e)}), 400
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"code": 500, "message": "服务器内部错误"}), 500

@project_members_bp.route('/projects/<int:project_id>/members/<int:employee_id>', methods=['DELETE'])
def delete_project_member_api(project_id, employee_id):
    """从指定项目中移除一个成员。"""
    if not is_member_in_project(project_id, employee_id):
        return jsonify({"code": 404, "message": "该员工不是项目成员"}), 404
    
    if delete_project_member(project_id, employee_id):
        return '', 204
    
    return jsonify({"code": 500, "message": "移除成员失败"}), 500