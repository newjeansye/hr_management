<template>
  <div class="department-detail-container">
    <el-page-header @back="$router.back()" class="custom-header mb-4">
      <template #content>
        <span class="header-title">{{ pageTitle }}</span>
      </template>
    </el-page-header>

    <el-card class="styled-card" v-loading="loading">
      <el-descriptions
        :column="3"
        border
        size="large"
        title="🏛️ 部门基础档案"
        class="vibrant-descriptions mb-5"
      >
        <el-descriptions-item label="部门 ID">
          <span class="id-tag">{{ department.department_id || 'N/A' }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="部门名称">
          <b style="color: #1a2a3a">{{ department.department_name || '加载中...' }}</b>
        </el-descriptions-item>
        <el-descriptions-item label="上级部门">
          <el-tag v-if="department.parent_department_name" type="info" round effect="plain">
            {{ department.parent_department_name }}
          </el-tag>
          <span v-else>无</span>
        </el-descriptions-item>

        <el-descriptions-item label="部门经理">
          <el-tag effect="dark" class="manager-tag">{{ department.manager_name || '未指定' }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="团队规模">
          <el-tag type="success" round effect="light">{{ departmentEmployees.length }} 人</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="部门职能描述" :span="3">
          <p class="desc-text">{{ department.description || '暂无详细职能描述。' }}</p>
        </el-descriptions-item>
      </el-descriptions>

      <div class="employee-section mt-5">
        <div class="section-header">
          <div class="title-dot"></div>
          <h3>部门成员矩阵</h3>
        </div>
        
        <el-table :data="departmentEmployees" border stripe class="custom-table">
          <el-table-column prop="employee_id" label="工号" width="100" align="center" />
          <el-table-column prop="name" label="姓名" width="120">
            <template #default="{ row }">
              <span class="emp-name">{{ row.name }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="position" label="职位" width="150" />
          <el-table-column prop="hire_date" label="入职日期" width="150" align="center" />
          <el-table-column prop="email" label="邮箱" min-width="180" />
          <el-table-column label="状态" width="100" align="center">
            <template #default="{ row }">
              <el-tag :class="'status-tag-' + row.status" round effect="dark">{{ row.status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100" fixed="right" align="center">
            <template #default="{ row }">
              <el-button link type="primary" class="oval-link" @click="goToEmployeeDetail(row.employee_id)">查看档案</el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <el-empty v-if="departmentEmployees.length === 0 && !loading" description="该部门当前暂无成员" />
      </div>
    </el-card>

    <div v-if="error" class="error-msg-fixed">
      <el-alert :title="error" type="error" show-icon :closable="false" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { getDepartmentById, getDepartmentEmployees } from '@/api/department'; 

const route = useRoute();
const router = useRouter();
const departmentId = ref(route.params.id); 
const department = ref({});
const departmentEmployees = ref([]);
const loading = ref(false);
const error = ref('');

const pageTitle = computed(() => `部门详情: ${department.value.department_name || '...'}`);

const fetchDepartmentData = async () => {
  if (!departmentId.value) return;
  loading.value = true;
  try {
    const deptData = await getDepartmentById(departmentId.value);
    department.value = {
      ...deptData,
      parent_department_name: deptData.parent_department_name || '无',
      description: deptData.description || '无详细描述。'
    };
    const employeesData = await getDepartmentEmployees(departmentId.value);
    departmentEmployees.value = employeesData || [];
  } catch (err) {
    ElMessage.error('数据加载失败');
  } finally {
    loading.value = false;
  }
};

const goToEmployeeDetail = (id) => {
  router.push({ name: 'EmployeeDetail', params: { id } }).catch(() => {
    ElMessage.warning('详情路由未配置');
  });
}

onMounted(fetchDepartmentData);
</script>

<style scoped>
.department-detail-container { padding: 30px; background-color: #f0f7ff; min-height: 100vh; }

/* 页面头美化 */
.custom-header :deep(.el-page-header__left) { color: #3a8ee6; }
.header-title { font-size: 1.4rem; font-weight: 800; color: #1a2a3a; }

/* 卡片风格 */
.styled-card {
  border: 2px solid #3a8ee6;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(58, 142, 230, 0.1) !important;
}

/* 描述列表样式 */
.vibrant-descriptions :deep(.el-descriptions__title) { color: #3a8ee6; font-size: 1.1rem; }
.id-tag { background: #eef2f7; padding: 2px 8px; border-radius: 4px; font-family: monospace; }
.manager-tag { background: linear-gradient(90deg, #3a8ee6, #4facfe); border: none; }
.desc-text { color: #606266; line-height: 1.6; }

/* 成员列表头部 */
.section-header { display: flex; align-items: center; gap: 10px; margin: 30px 0 20px; border-bottom: 2px solid #eaf4ff; padding-bottom: 10px; }
.title-dot { width: 10px; height: 10px; background: #3a8ee6; border-radius: 50%; }
.section-header h3 { margin: 0; color: #2c3e50; font-size: 1.2rem; }

/* 表格与标签 */
.custom-table { border-radius: 12px; overflow: hidden; }
.custom-table :deep(th) { background-color: #f0f7ff !important; color: #4a5568; }
.emp-name { font-weight: bold; color: #3a8ee6; }

.status-tag-在职 { --el-tag-bg-color: #48bb78; }
.status-tag-离职 { --el-tag-bg-color: #f56c6c; }
.status-tag-试用期 { --el-tag-bg-color: #e6a23c; }

.oval-link { font-weight: bold; text-decoration: underline; }
.error-msg-fixed { margin-top: 20px; }
</style>