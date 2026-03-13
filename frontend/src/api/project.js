import request from './request'; 

const API_PREFIX = '/projects'; 
const getData = (res) => res.data;

export function getProjectList(query) {
    const params = query ? { query } : {};
    return request({ 
        url: API_PREFIX, 
        method: 'get',
        params 
    }).then(getData); 
}

export function getProjectById(id) {
    return request({ url: `${API_PREFIX}/${id}`, method: 'get' }).then(getData);
}

export function createProject(data) {
    return request({ url: API_PREFIX, method: 'post', data }).then(getData);
}

export function updateProject(id, data) {
    return request({ url: `${API_PREFIX}/${id}`, method: 'put', data }).then(getData);
}

export function deleteProject(id) {
    return request({ url: `${API_PREFIX}/${id}`, method: 'delete' }).then(getData); 
}

export function getProjectMembers(projectId) {
    return request({ 
        url: `${API_PREFIX}/${projectId}/members`, 
        method: 'get' 
    }).then(getData);
}

export function addProjectMember(projectId, data) {
    return request({ 
        url: `${API_PREFIX}/${projectId}/members`, 
        method: 'post', 
        data 
    }).then(getData);
}

export function deleteProjectMember(projectId, employeeId) {
    return request({ 
        url: `${API_PREFIX}/${projectId}/members/${employeeId}`, 
        method: 'delete' 
    }).then(getData);
}