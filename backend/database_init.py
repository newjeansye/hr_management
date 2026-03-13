import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import Config
from backend.database import init_db, db
from backend.models import Department, Employee, ProjectExperience, ProjectMember

def initialize_database():
    try:
        print("Initializing database connection...")
        app = init_db(Config) 
        
        with app.app_context():
            print("Creating all tables...")
            db.create_all()

            # 1. 部门数据填充
            if Department.query.count() == 0:
                dept_r_d = Department(department_name='研发部', description='负责核心技术研发')
                dept_hr = Department(department_name='人力资源部', description='负责招聘与福利')
                dept_mkt = Department(department_name='市场部', description='负责品牌推广')
                db.session.add_all([dept_r_d, dept_hr, dept_mkt])
                db.session.commit()
            else:
                dept_r_d = Department.query.filter_by(department_name='研发部').first()
                dept_hr = Department.query.filter_by(department_name='人力资源部').first()

            # 2. 员工数据填充
            if Employee.query.count() == 0:
                emp1 = Employee(
                    name='张三', department_id=dept_r_d.department_id, 
                    position='研发总监', hire_date=datetime(2020, 1, 15).date(),
                    gender='男', status='在职', phone='13812345678', 
                    email='zhangsan@example.com', salary=15000.00
                )
                emp2 = Employee(
                    name='李四', department_id=dept_hr.department_id, 
                    position='HR经理', hire_date=datetime(2021, 5, 20).date(),
                    gender='女', status='在职', phone='13987654321', 
                    email='lisi@example.com', salary=9000.00
                )
                db.session.add_all([emp1, emp2])
                db.session.commit()
            else:
                emp1 = Employee.query.filter_by(name='张三').first()

            # 3. 项目数据填充
            if ProjectExperience.query.count() == 0:
                proj1 = ProjectExperience(
                    project_name='新一代 ERP 系统', start_date=datetime(2023, 3, 1).date(),
                    project_status='进行中', budget=5000000.00, client='内部项目组'
                )
                db.session.add(proj1)
                db.session.commit()
            else:
                proj1 = ProjectExperience.query.filter_by(project_name='新一代 ERP 系统').first()

            # 4. 项目成员关联
            if ProjectMember.query.count() == 0 and proj1 and emp1:
                member1 = ProjectMember(
                    project_id=proj1.project_id, employee_id=emp1.employee_id, 
                    role='项目负责人 (PM)', start_date=datetime(2023, 3, 1).date()
                )
                db.session.add(member1)
                db.session.commit()

            print("\nDatabase initialization complete!")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        if db.session.is_active:
            db.session.rollback()

if __name__ == "__main__":
    initialize_database()