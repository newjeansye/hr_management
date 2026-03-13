<template>
  <div class="employee-detail-container">
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
        title="👤 员工个人档案"
        class="vibrant-descriptions mb-5"
      >
        <el-descriptions-item label="员工 ID">
          <span class="id-tag">{{ employee.employee_id || 'N/A' }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="姓名">
          <b style="color: #1a2a3a">{{ employee.name || 'N/A' }}</b>
        </el-descriptions-item>
        <el-descriptions-item label="性别">{{ employee.gender || 'N/A' }}</el-descriptions-item>

        <el-descriptions-item label="所属部门">
          <el-tag effect="plain" round>{{ employee.department_name || '未分配' }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="当前职位">{{ employee.position || 'N/A' }}</el-descriptions-item>
        <el-descriptions-item label="在职状态">
          <el-tag :class="'status-tag-' + employee.status" round effect="dark">
            {{ employee.status || 'N/A' }}
          </el-tag>
        </el-descriptions-item>

        <el-descriptions-item label="入职日期">{{ employee.hire_date || 'N/A' }}</el-descriptions-item>
        <el-descriptions-item label="直属经理">
          <span class="manager-text">{{ employee.manager_name || '无' }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ employee.phone || 'N/A' }}</el-descriptions-item>

        <el-descriptions-item label="邮箱地址">{{ employee.email || 'N/A' }}</el-descriptions-item>
        <el-descriptions-item label="出生日期">{{ employee.birth_date || 'N/A' }}</el-descriptions-item>
        <el-descriptions-item label="身份证号">{{ employee.id_card || 'N/A' }}</el-descriptions-item>
      </el-descriptions>

      <div class="project-section mt-5">
        <div class="section-header">
          <div class="title-dot"></div>
          <h3>项目履历 ({{ employeeProjects.length }})</h3>
        </div>

        <el-table :data="employeeProjects" border stripe class="custom-table">
          <el-table-column prop="project_id" label="项目 ID" width="100" align="center" />
          <el-table-column prop="project_name" label="项目名称" min-width="180">
            <template #default="{ row }">
              <span class="project-name-link">{{ row.project_name }}</span>
            </template>
          </el-table-column>
          <el-table-column label="分配角色" width="150" align="center">
            <template #default="{ row }">
              <el-tag type="info" effect="light">{{ row.role }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="start_date" label="参与日期" width="130" align="center" />
          <el-table-column prop="end_date" label="预计结束" width="130" align="center" />
          <el-table-column label="项目状态" width="120" align="center">
            <template #default="{ row }">
              <el-tag :class="'proj-status-' + row.status" effect="dark" round>
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
        <el-empty v-if="employeeProjects.length === 0 && !loading" description="暂无项目参与记录" />
      </div>
    </el-card>

    <div v-if="error" class="error-msg-fixed">
      <el-alert :title="error" type="error" show-icon :closable="false" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import { getEmployeeById, getEmployeeProjects } from '@/api/employee';

const route = useRoute();
const employeeId = computed(() => route.params.id ? parseInt(route.params.id) : null);

const employee = ref({});
const employeeProjects = ref([]);
const loading = ref(false);
const error = ref('');

const pageTitle = computed(() => `员工详情: ${employee.value.name || '...'}`);

const fetchEmployeeData = async () => {
  if (!employeeId.value) return;
  
  loading.value = true;
  error.value = '';
  try {
    const employeeData = await getEmployeeById(employeeId.value);
    if (employeeData && employeeData.employee_id) {
      employee.value = employeeData; 
    }
    const projectsData = await getEmployeeProjects(employeeId.value);
    employeeProjects.value = projectsData || [];
  } catch (err) {
    error.value = err.message || '加载失败';
    ElMessage.error(error.value);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchEmployeeData);
</script>

<style scoped>
.employee-detail-container { padding: 30px; background-color: #f0f7ff; min-height: 100vh; }

.custom-header :deep(.el-page-header__left) { color: #3a8ee6; }
.header-title { font-size: 1.4rem; font-weight: 800; color: #1a2a3a; }

.styled-card {
  border: 2px solid #3a8ee6;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(58, 142, 230, 0.1) !important;
}

.vibrant-descriptions :deep(.el-descriptions__title) { color: #3a8ee6; font-size: 1.1rem; }
.id-tag { background: #eef2f7; padding: 2px 8px; border-radius: 4px; font-family: monospace; }
.manager-text { color: #3a8ee6; font-weight: 600; }

.section-header { display: flex; align-items: center; gap: 10px; margin: 30px 0 20px; border-bottom: 2px solid #eaf4ff; padding-bottom: 10px; }
.title-dot { width: 10px; height: 10px; background: #3a8ee6; border-radius: 50%; }
.section-header h3 { margin: 0; color: #2c3e50; font-size: 1.2rem; }

.custom-table { border-radius: 12px; overflow: hidden; }
.custom-table :deep(th) { background-color: #f0f7ff !important; color: #4a5568; }

.status-tag-在职 { --el-tag-bg-color: #48bb78; }
.status-tag-离职 { --el-tag-bg-color: #f56c6c; }
.status-tag-试用期 { --el-tag-bg-color: #e6a23c; }

.proj-status-进行中 { --el-tag-bg-color: #409eff; }
.proj-status-已完成 { --el-tag-bg-color: #67c23a; }
.proj-status-挂起 { --el-tag-bg-color: #909399; }

.project-name-link { font-weight: bold; color: #2c3e50; }
.error-msg-fixed { margin-top: 20px; }
</style>