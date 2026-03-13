<template>
  <div class="employee-container">
    <el-card class="styled-card">
      <template #header>
        <div class="card-header">
          <span class="title">员工管理系统</span>
          <el-button class="round-btn" type="primary" @click="openDialog('add')">
            <el-icon><Plus /></el-icon>新增员工
          </el-button>
        </div>
      </template>

      <div class="search-bar">
        <el-input 
          v-model="searchQuery" 
          placeholder="搜索姓名或 ID..." 
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
        :data="employeeList" 
        class="custom-table"
        v-loading="loading"
        border
        stripe
      >
        <el-table-column prop="employee_id" label="ID" width="80" align="center" />
        <el-table-column prop="name" label="姓名" width="120" font-weight="bold" />
        <el-table-column prop="department_name" label="部门" width="150" />
        <el-table-column prop="position" label="职位" width="150" />
        <el-table-column prop="email" label="邮箱" min-width="200" />
        <el-table-column label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="row.status === '在职' ? 'success' : 'info'" effect="light" round>
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" align="center" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="goToDetail(row)">详情</el-button>
            <el-button link type="warning" @click="openDialog('edit', row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑员工' : '新增员工'" width="600px" custom-class="styled-dialog">
      <el-form :model="form" label-width="100px" class="styled-form">
        <el-form-item label="姓名" required><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="部门" required>
          <el-select v-model="form.department_id" placeholder="选择部门" style="width: 100%">
            <el-option v-for="d in departmentOptions" :key="d.department_id" :label="d.department_name" :value="d.department_id" />
          </el-select>
        </el-form-item>
        <el-form-item label="职位"><el-input v-model="form.position" /></el-form-item>
        <el-form-item label="邮箱" required><el-input v-model="form.email" /></el-form-item>
        <el-form-item label="入职日期" required>
          <el-date-picker v-model="form.hire_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="状态" v-if="isEdit">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="在职" value="在职" /><el-option label="离职" value="离职" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false" round>取消</el-button>
        <el-button type="primary" @click="handleSubmit" round>{{ isEdit ? '更新保存' : '立即创建' }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus, Search } from '@element-plus/icons-vue';
import { getEmployeeList, createEmployee, updateEmployee, deleteEmployee } from '@/api/employee';
import { getDepartmentList } from '@/api/department';

const router = useRouter();
const employeeList = ref([]);
const departmentOptions = ref([]);
const loading = ref(false);
const dialogVisible = ref(false);
const isEdit = ref(false);
const searchQuery = ref('');
const form = ref({});

onMounted(() => {
  fetchDepartments();
  fetchEmployees();
});

const fetchDepartments = async () => {
  const res = await getDepartmentList();
  departmentOptions.value = res || [];
};

const fetchEmployees = async (q = '') => {
  loading.value = true;
  try {
    const data = await getEmployeeList(q);
    employeeList.value = data.map(e => ({
      ...e,
      department_id: Number(e.department_id),
      hire_date: e.hire_date?.substring(0, 10)
    }));
  } finally { loading.value = false; }
};

const handleSearch = () => fetchEmployees(searchQuery.value.trim());
const resetSearch = () => { searchQuery.value = ''; fetchEmployees(); };

const handleSubmit = async () => {
  if (!form.value.name || !form.value.email) return ElMessage.warning('请填写必填项');
  try {
    if (isEdit.value) {
      await updateEmployee(form.value.employee_id, form.value);
      ElMessage.success('更新成功');
    } else {
      await createEmployee(form.value);
      ElMessage.success('新增成功');
    }
    dialogVisible.value = false;
    fetchEmployees();
  } catch (e) { ElMessage.error('操作失败'); }
};

const handleDelete = (row) => {
  ElMessageBox.confirm(`确定删除 ${row.name}？`, '警告', { type: 'warning' }).then(async () => {
    await deleteEmployee(row.employee_id);
    ElMessage.success('已删除');
    fetchEmployees();
  });
};

const goToDetail = (row) => router.push({ name: 'EmployeeDetail', params: { id: row.employee_id } });

const openDialog = (type, row = {}) => {
  isEdit.value = type === 'edit';
  form.value = isEdit.value ? { ...row } : { gender: '男', status: '在职' };
  dialogVisible.value = true;
};
</script>

<style scoped>
.employee-container { padding: 25px; background-color: #f0f7ff; min-height: 100vh; }

/* 卡片与边框 */
.styled-card {
  border: 2px solid #3a8ee6; /* 蓝色深边框 */
  border-radius: 15px;
  overflow: hidden;
}

.card-header { display: flex; justify-content: space-between; align-items: center; }
.title { font-size: 1.2rem; font-weight: bold; color: #3a8ee6; }

/* 蓝色椭圆搜索框 */
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

/* 表格美化 */
.custom-table {
  border: 1px solid #dcdfe6;
  border-radius: 8px;
}
.custom-table :deep(th) { background-color: #eaf4ff !important; color: #333; font-weight: bold; }

/* 按钮样式 */
.round-btn { border-radius: 20px; font-weight: bold; }
</style>