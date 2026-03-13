import axios from 'axios';
import { ElMessage } from 'element-plus';

const service = axios.create({
    baseURL: '/api',
    timeout: 10000,
    headers: { 'Content-Type': 'application/json' }
});

service.interceptors.request.use(
    config => {
        const token = localStorage.getItem('userToken');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

service.interceptors.response.use(
    response => {
        const res = response.data;
        const httpStatus = response.status;
        const isSuccess = (res?.code == 200 || res?.code == 201 || httpStatus === 204);

        if (isSuccess) {
            return res;
        } else {
            const errorMessage = res?.message || '操作失败';
            
            if (res?.code == 401 || httpStatus === 401) {
                ElMessage({ message: '登录状态已过期，请重新登录！', type: 'warning' });
            } else {
                ElMessage({ message: errorMessage, type: 'error', duration: 5000 });
            }
            
            return Promise.reject(new Error(errorMessage));
        }
    },
    error => {
        let message = '网络连接失败';
        if (error.response) {
            const httpStatus = error.response.status;
            message = error.response.data?.message || error.response.statusText || `服务器错误: ${httpStatus}`;
        } else if (error.code === 'ECONNABORTED') {
            message = '请求超时';
        }

        ElMessage({ message: message, type: 'error', duration: 5000 });
        return Promise.reject(error);
    }
);

export default service;