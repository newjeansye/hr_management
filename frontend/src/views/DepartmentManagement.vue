<template>
  <div class="department-container">
    <el-card class="styled-card">
      <template #header>
        <div class="card-header">
          <span class="title">部门架构管理</span>
          <el-button class="round-btn" type="primary" @click="openDialog('add')">
            <el-icon><Plus /></el-icon>新增部门
          </el-button>
        </div>
      </template>

      <div class="search-bar">
        <el-input 
          v-model="searchQuery" 
          placeholder="搜索部门名称或 ID..." 
          class="oval-input"
          clearable
          @keyup.enter="handleSearch"
        >
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
        <el-button class="oval-btn search-submit" @click="handleSearch">查询</el-button>
        <el-button class="oval-btn reset-btn" @click="resetSearch">重置</el-button>
      </div>
      
      <el-table 
        :data="departmentList" 
        class="custom-table"
        v-loading="loading"
        border
        stripe
      >
        <el-table-column prop="department_id" label="ID" width="80" align="center" />
        <el-table-column prop="department_name" label="部门名称" width="180">
           <template #default="{ row }">
            <span style="font-weight: bold; color: #2c3e50">{{ row.department_name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="负责人" width="150">
          <template #default="{ row }">
            {{ row.manager_name || '未设置' }}
          </template>
        </el-table-column>
        <el-table-column label="上级部门" width="150">
          <template #default="{ row }">
            <el-tag v-if="row.parent_id" type="info" size="small" effect="plain">
              {{ getParentName(row.parent_id) }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="职能描述" min-width="200" show-overflow-tooltip />
        
        <el-table-column label="操作" width="220" align="center" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="goToDetail(row)">详情</el-button>
            <el-button link type="warning" @click="openDialog('edit', row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑部门' : '新增部门'" width="600px">
      <el-form :model="form" label-width="100px" class="styled-form">
        <el-form-item label="部门名称" required>
          <el-input v-model="form.department_name" placeholder="请输入部门名称" />
        </el-form-item>
        <el-form-item label="部门经理">
          <el-select v-model="form.manager_id" placeholder="指派经理" style="width: 100%" clearable>
            <el-option 
              v-for="e in employeeOptions" 
              :key="e.employee_id" 
              :label="e.name" 
              :value="e.employee_id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="上级部门">
          <el-select v-model="form.parent_department_id" placeholder="选择上级部门" style="width: 100%" clearable>
            <el-option 
              v-for="d in departmentList.filter(item => item.department_id !== form.department_id)" 
              :key="d.department_id" 
              :label="d.department_name" 
              :value="d.department_id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="职能描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false" round>取消</el-button>
        <el-button type="primary" @click="handleSubmit" round>{{ isEdit ? '保存更改' : '立即创建' }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'; 
import { ElMessage, ElMessageBox } from 'element-plus';
import { Search, Plus } from '@element-plus/icons-vue'; 
import { getDepartmentList, createDepartment, updateDepartment, deleteDepartment } from '@/api/department';
import { getEmployeeList } from '@/api/employee';

const router = useRouter(); 
const departmentList = ref([]);
const employeeOptions = ref([]); 
const loading = ref(false);
const dialogVisible = ref(false);
const isEdit = ref(false);
const searchQuery = ref(''); 
const form = ref({});

onMounted(() => {
  fetchEmployees();
  fetchDepartments();
});

const getParentName = (id) => {
  const dept = departmentList.value.find(d => d.department_id === id);
  return dept ? dept.department_name : 'N/A';
};

const fetchEmployees = async () => {
  employeeOptions.value = await getEmployeeList();
};

const fetchDepartments = async (query = '') => {
  loading.value = true;
  try {
    departmentList.value = await getDepartmentList(query);
  } finally { loading.value = false; }
};

const handleSearch = () => fetchDepartments(searchQuery.value.trim());
const resetSearch = () => { searchQuery.value = ''; fetchDepartments(); };

const openDialog = (type, row = {}) => {
  isEdit.value = type === 'edit';
  if (isEdit.value) {
    form.value = { ...row, parent_department_id: row.parent_id };
  } else {
    form.value = { department_name: '', description: '', manager_id: null, parent_department_id: null };
  }
  dialogVisible.value = true;
};

const handleSubmit = async () => {
  if (!form.value.department_name) return ElMessage.warning('请输入部门名称');
  const payload = {
      department_name: form.value.department_name,
      description: form.value.description,
      manager_id: form.value.manager_id,
      parent_id: form.value.parent_department_id
  };
  try {
    isEdit.value ? await updateDepartment(form.value.department_id, payload) : await createDepartment(payload);
    ElMessage.success('操作成功');
    dialogVisible.value = false;
    fetchDepartments();
  } catch (e) { ElMessage.error('操作失败'); }
};

const handleDelete = (row) => {
  ElMessageBox.confirm(`确定删除部门 ${row.department_name}？`, '警告', { type: 'warning' }).then(async () => {
    await deleteDepartment(row.department_id);
    ElMessage.success('已删除');
    fetchDepartments();
  });
};

const goToDetail = (row) => router.push({ name: 'DepartmentDetail', params: { id: row.department_id } });
</script>

<style scoped>
.department-container { padding: 25px; background-color: #f0f7ff; min-height: 100vh; }

.styled-card {
  border: 2px solid #3a8ee6;
  border-radius: 15px;
  overflow: hidden;
}

.card-header { display: flex; justify-content: space-between; align-items: center; }
.title { font-size: 1.2rem; font-weight: bold; color: #3a8ee6; }

.search-bar { display: flex; gap: 12px; margin-bottom: 25px; }

.oval-input :deep(.el-input__wrapper) {
  border-radius: 25px !important;
  border: 1.5px solid #3a8ee6 !important;
  padding-left: 15px;
  width: 300px;
}

.oval-btn { border-radius: 25px; padding: 0 25px; transition: all 0.3s; }
.search-submit { background-color: #3a8ee6; color: white; border: none; }
.search-submit:hover { background-color: #66b1ff; box-shadow: 0 4px 12px rgba(58,142,230,0.3); }

.custom-table { border: 1px solid #dcdfe6; border-radius: 8px; }
.custom-table :deep(th) { background-color: #eaf4ff !important; color: #333; font-weight: bold; }

.round-btn { border-radius: 20px; font-weight: bold; }
</style>