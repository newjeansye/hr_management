import request from './request'; 

const API_PREFIX = '/employees'; 
const getData = (res) => res.data; 

export function getEmployeeList(query) { 
    const params = query ? { query } : {};
    return request({ 
        url: API_PREFIX, 
        method: 'get',
        params 
    }).then(getData);
}

export function getEmployeeById(id) {
    return request({ url: `${API_PREFIX}/${id}`, method: 'get' }).then(getData);
}

export function createEmployee(data) {
    return request({ url: API_PREFIX, method: 'post', data }).then(getData);
}

export function updateEmployee(id, data) {
    return request({ url: `${API_PREFIX}/${id}`, method: 'put', data }).then(getData);
}

export function deleteEmployee(id) {
    return request({ url: `${API_PREFIX}/${id}`, method: 'delete' }).then(getData);
}

export function getEmployeeProjects(employeeId) {
    return request({ 
        url: `${API_PREFIX}/${employeeId}/projects`, 
        method: 'get' 
    }).then(getData);
}