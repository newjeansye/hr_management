import { createRouter, createWebHistory } from 'vue-router';
import EmployeeManagement from '@/views/EmployeeManagement.vue';
import DepartmentManagement from '@/views/DepartmentManagement.vue';
import ProjectManagement from '@/views/ProjectManagement.vue'; 
import EmployeeDetail from '@/views/EmployeeDetail.vue'; 
import DepartmentDetail from '@/views/DepartmentDetail.vue'; 
import ProjectDetail from '@/views/ProjectDetail.vue'; 

const routes = [
    {
        path: '/',
        redirect: '/employee',
    },
    { 
        path: '/employee',
        name: 'EmployeeManagement',
        component: EmployeeManagement,
        meta: { title: '员工管理' },
    },
    {
        path: '/employee/:id',
        name: 'EmployeeDetail',
        component: EmployeeDetail,
        meta: { title: '员工详情' },
    },
    { 
        path: '/department',
        name: 'DepartmentManagement',
        component: DepartmentManagement,
        meta: { title: '部门管理' },
    },
    {
        path: '/department/:id',
        name: 'DepartmentDetail',
        component: DepartmentDetail,
        meta: { title: '部门详情' },
    },
    { 
        path: '/project',
        name: 'ProjectManagement',
        component: ProjectManagement,
        meta: { title: '项目管理' },
    },
    {
        path: '/project/:id',
        name: 'ProjectDetail',
        component: ProjectDetail,
        meta: { title: '项目详情' },
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;