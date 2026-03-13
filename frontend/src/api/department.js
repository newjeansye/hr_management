import request from './request'; 

const API_PREFIX = '/departments'; 
const getData = (res) => res.data;

export function getDepartmentList(query) { 
    const params = query ? { query } : {};
    return request({ 
        url: API_PREFIX, 
        method: 'get',
        params
    }).then(getData); 
}

export function getDepartmentById(id) { 
    return request({ url: `${API_PREFIX}/${id}`, method: 'get' }).then(getData);
}

export function getDepartmentEmployees(id) { 
    return request({ url: `${API_PREFIX}/${id}/employees`, method: 'get' }).then(getData);
}

export function createDepartment(data) {
    return request({ url: API_PREFIX, method: 'post', data }).then(getData);
}

export function updateDepartment(id, data) {
    return request({ url: `${API_PREFIX}/${id}`, method: 'put', data }).then(getData);
}

export function deleteDepartment(id) {
    return request({ url: `${API_PREFIX}/${id}`, method: 'delete' }).then(getData);
}