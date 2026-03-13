<template>
  <div class="project-container">
    <el-card class="styled-card">
      <template #header>
        <div class="card-header">
          <span class="title">项目交付看板</span>
          <el-button class="round-btn" type="primary" @click="handleCreate">
            <el-icon><Plus /></el-icon>新增项目
          </el-button>
        </div>
      </template>

      <div class="search-bar">
        <el-input 
          v-model="searchQuery" 
          placeholder="搜索项目名称或 ID..." 
          class="oval-input"
          clearable
          @keyup.enter="handleSearch"
        >
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
        <el-button class="oval-btn search-submit" @click="handleSearch">查询</el-button>
        <el-button class="oval-btn reset-btn" @click="resetSearch">重置</el-button>
        <el-button class="oval-btn refresh-btn" @click="fetchProjects">刷新</el-button>
      </div>
      
      <el-table 
        :data="projectList" 
        class="custom-table"
        v-loading="loading"
        border
        stripe
      >
        <el-table-column prop="project_id" label="ID" width="80" align="center" fixed />
        <el-table-column prop="project_name" label="项目名称" width="200">
          <template #default="{ row }">
            <span class="project-title">{{ row.project_name }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="manager_name" label="负责人" width="120" />
        <el-table-column label="周期" width="240">
          <template #default="{ row }">
            <span class="date-text">{{ row.start_date }}</span> 
            <span style="margin: 0 4px; color: #999;">至</span>
            <span class="date-text">{{ row.end_date }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="120" align="center">
          <template #default="{ row }">
            <el-tag :class="'status-' + row.status" effect="dark" round>
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="goToDetail(row.project_id)">详情</el-button>
            <el-button link type="warning" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form :model="projectForm" label-width="100px" class="styled-form">
        <el-form-item label="项目名称" required>
          <el-input v-model="projectForm.project_name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="项目经理">
          <el-select v-model="projectForm.manager_id" placeholder="指派经理" style="width: 100%" clearable>
            <el-option v-for="e in employeeOptions" :key="e.employee_id" :label="e.name" :value="e.employee_id" />
          </el-select>
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="开始日期">
              <el-date-picker v-with="100" v-model="projectForm.start_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结束日期">
              <el-date-picker v-model="projectForm.end_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="项目状态">
          <el-select v-model="projectForm.status" style="width: 100%">
            <el-option label="待开始" value="待开始" />
            <el-option label="进行中" value="进行中" />
            <el-option label="已完成" value="已完成" />
            <el-option label="已暂停" value="已暂停" />
          </el-select>
        </el-form-item>
        <el-form-item label="项目描述">
          <el-input v-model="projectForm.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false" round>取消</el-button>
        <el-button type="primary" @click="handleSave" round>确认保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Search, Plus } from '@element-plus/icons-vue';
import { getProjectList, createProject, updateProject, deleteProject } from '@/api/project';
import { getEmployeeList } from '@/api/employee';

const router = useRouter();
const dialogVisible = ref(false);
const dialogTitle = ref('新增项目');
const projectList = ref([]);
const employeeOptions = ref([]);
const loading = ref(true);
const searchQuery = ref('');

const initialForm = { project_id: null, project_name: '', manager_id: null, start_date: null, end_date: null, status: '待开始', description: '' };
const projectForm = ref({ ...initialForm });

const fetchProjects = async (query = '') => {
  loading.value = true;
  try {
    const res = await getProjectList(query);
    const data = Array.isArray(res) ? res : (res.data || []);
    projectList.value = data.map(p => ({
      ...p,
      start_date: p.start_date ? String(p.start_date).substring(0, 10) : 'N/A',
      end_date: p.end_date ? String(p.end_date).substring(0, 10) : 'N/A',
    }));
  } finally { loading.value = false; }
};

const fetchEmployees = async () => {
  const res = await getEmployeeList();
  employeeOptions.value = Array.isArray(res) ? res : (res.data || []);
};

const handleSearch = () => fetchProjects(searchQuery.value.trim());
const resetSearch = () => { searchQuery.value = ''; fetchProjects(); };

const handleCreate = () => {
  dialogTitle.value = '🚀 开启新项目';
  projectForm.value = { ...initialForm };
  dialogVisible.value = true;
};

const handleEdit = (row) => {
  dialogTitle.value = '✨ 编辑项目信息';
  projectForm.value = JSON.parse(JSON.stringify(row));
  dialogVisible.value = true;
};

const handleSave = async () => {
  if (!projectForm.value.project_name) return ElMessage.warning('项目名称是必填项');
  try {
    const id = projectForm.value.project_id;
    id ? await updateProject(id, projectForm.value) : await createProject(projectForm.value);
    ElMessage.success('操作成功');
    dialogVisible.value = false;
    fetchProjects();
  } catch (e) { ElMessage.error('保存失败'); }
};

const handleDelete = (row) => {
  ElMessageBox.confirm(`确定删除项目 ${row.project_name} 吗?`, '风险提示', { type: 'error' }).then(async () => {
    await deleteProject(row.project_id);
    ElMessage.success('已删除');
    fetchProjects();
  });
};

const goToDetail = (id) => router.push({ name: 'ProjectDetail', params: { id } });

onMounted(() => {
  fetchProjects();
  fetchEmployees();
});
</script>

<style scoped>
.project-container { padding: 25px; background-color: #f0f7ff; min-height: 100vh; }

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
  width: 280px;
}

.oval-btn { border-radius: 25px; padding: 0 25px; transition: all 0.3s; font-weight: bold; }
.search-submit { background-color: #3a8ee6; color: white; border: none; }
.refresh-btn { background-color: #fff; color: #3a8ee6; border: 1.5px solid #3a8ee6; }

.custom-table { border: 1px solid #dcdfe6; border-radius: 8px; }
.custom-table :deep(th) { background-color: #eaf4ff !important; color: #333; font-weight: bold; }

.project-title { font-weight: bold; color: #2c3e50; }
.date-text { color: #555; font-size: 0.9rem; }

/* 状态标签配色 */
.status-待开始 { --el-tag-bg-color: #909399; }
.status-进行中 { --el-tag-bg-color: #409eff; }
.status-已完成 { --el-tag-bg-color: #67c23a; }
.status-已暂停 { --el-tag-bg-color: #e6a23c; }

.round-btn { border-radius: 20px; font-weight: bold; }
</style>