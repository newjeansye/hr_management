from flask import Flask, jsonify
from flask_cors import CORS
from .api.employee import employee_bp 
from .api.department import department_bp 
from .api.project import project_bp
from .api.project_members import project_members_bp

app = Flask(__name__)

# 数据库连接基础配置
app.config['DB_NAME'] = 'hr_management' 
app.config['DB_USER'] = 'test' 
app.config['DB_PASSWORD'] = '"Bigdata@123' 
app.config['DB_HOST'] = '127.0.0.1' 
app.config['DB_PORT'] = 26000

CORS(app) 

# 注册所有业务模块蓝图
app.register_blueprint(employee_bp, url_prefix='/api')
app.register_blueprint(department_bp, url_prefix='/api')
app.register_blueprint(project_bp, url_prefix='/api')
app.register_blueprint(project_members_bp, url_prefix='/api')

@app.route('/')
def home():
    return jsonify({
        "status": "ok", 
        "service": "HR Management Backend",
        "endpoints": [
            "/api/employees",
            "/api/departments",
            "/api/projects",
            "/api/projects/<id>/members"
        ]
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "code": 404, 
        "message": "API 路径不存在"
    }), 404

if __name__ == '__main__':
    app.run(
        debug=True, 
        host='0.0.0.0',
        port=5000 
    )