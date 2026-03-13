from flask_sqlalchemy import SQLAlchemy

# 全局 SQLAlchemy 实例
db = SQLAlchemy()

def init_db(app):
    """初始化数据库连接"""
    db.init_app(app)