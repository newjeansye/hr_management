from flask import Blueprint, jsonify, request
from backend.models.project_model import (
    get_project_list, 
    add_project, 
    update_project, 
    delete_project, 
    get_project_by_id, 
)

project_bp = Blueprint('project_bp', __name__)

@project_bp.route('/projects', methods=['GET'])
def list_projects():
    """获取项目列表，支持搜索。"""
    search_query = request.args.get('query', default='') 
    data = get_project_list(search_query) 
    return jsonify({"code": 200, "data": data or []})

@project_bp.route('/projects', methods=['POST'])
def create_project():
    """创建新项目。"""
    data = request.get_json()
    if not data or not data.get('project_name'):
        return jsonify({"code": 400, "message": "缺少必要字段: project_name"}), 400
        
    project_id = add_project(data)
    if project_id:
        return jsonify({"code": 201, "message": "项目创建成功", "project_id": project_id}), 201
    else:
        return jsonify({"code": 500, "message": "项目创建失败"}), 500

@project_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project_api(project_id):
    """获取单个项目详情。"""
    data = get_project_by_id(project_id)
    if data:
        return jsonify({"code": 200, "data": data})
    else:
        return jsonify({"code": 404, "message": f"项目 ID:{project_id} 不存在"}), 404

@project_bp.route('/projects/<int:project_id>', methods=['PUT'])
def update_project_api(project_id):
    """更新项目信息。"""
    data = request.get_json()
    if update_project(project_id, data):
        return jsonify({"code": 200, "message": f"项目 ID:{project_id} 更新成功"})
    else:
        return jsonify({"code": 500, "message": "项目更新失败或 ID 不存在"}), 500

@project_bp.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project_api(project_id):
    """删除项目。"""
    if delete_project(project_id):
        return '', 204
    else:
        return jsonify({"code": 500, "message": "项目删除失败或 ID 不存在"}), 500