<template>
  <div class="project-detail-container">
    <el-page-header @back="$router.back()" :content="pageTitle" class="mb-4">
      <template #content>
        <span class="text-large font-600 mr-3">{{ pageTitle }}</span>
      </template>
    </el-page-header>

    <el-card class="box-card" v-loading="loading">
      <el-descriptions
        :column="3"
        border
        size="large"
        title="项目基础信息"
        class="project-info-table mb-5"
      >
        <el-descriptions-item label="项目 ID">{{ project.project_id || 'N/A' }}</el-descriptions-item>
        <el-descriptions-item label="项目名称">{{ project.project_name || 'N/A' }}</el-descriptions-item>
        <el-descriptions-item label="项目状态">
          <el-tag :type="getStatusTagType(project.status)" size="small">{{ project.status || 'N/A' }}</el-tag>
        </el-descriptions-item>

        <el-descriptions-item label="项目经理">
          <el-tag size="small">{{ project.manager_name || '未指定' }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="开始日期">{{ project.start_date || 'N/A' }}</el-descriptions-item>
        <el-descriptions-item label="结束日期">{{ project.end_date || 'N/A' }}</el-descriptions-item>
        
        <el-descriptions-item label="项目描述" :span="3">{{ project.description || '无描述' }}</el-descriptions-item>
      </el-descriptions>

      <div class="member-section mt-5">
        <div class="member-header">
          <h3>项目成员列表 (共 {{ projectMembers.length }} 人)</h3>
          <el-button type="primary" size="small" :icon="Plus" @click="openAddMemberDialog">添加成员</el-button>
        </div>
        
        <el-table :data="projectMembers" border stripe>
          <el-table-column prop="employee_id" label="员工 ID" width="100"></el-table-column>
          <el-table-column prop="name" label="姓名" width="120"></el-table-column>
          <el-table-column prop="role" label="项目角色" width="150"></el-table-column>
          <el-table-column prop="contribution" label="贡献度 (%)" width="120"></el-table-column>
          <el-table-column prop="performance_rating" label="绩效评级" min-width="120"></el-table-column>
          <el-table-column label="操作" width="180" fixed="right">
            <template #default="{ row }">
              <el-button size="small" link type="primary" @click="openEditMemberDialog(row)">编辑</el-button>
              <el-button size="small" type="danger" link @click="handleRemoveMember(row)">移除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-empty v-if="projectMembers.length === 0 && !loading" description="该项目当前没有成员" />
      </div>
    </el-card>

    <div v-if="error" class="error-message">
      <el-alert :title="error" type="error" show-icon :closable="false" />
    </div>

    <el-dialog v-model="addMemberDialogVisible" title="添加项目成员" width="40%">
      <el-form label-width="100px">
        <el-form-item label="选择员工">
          <el-select
            v-model="newMemberId"
            placeholder="请选择员工"
            style="width: 100%;"
            filterable
            clearable
          >
            <el-option
              v-for="employee in availableEmployees"
              :key="employee.employee_id"
              :label="`${employee.name} (${employee.department_name})`"
              :value="employee.employee_id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="项目角色">
          <el-input v-model="newMemberRole" placeholder="例如：开发人员/测试人员"></el-input>
        </el-form-item>
        
        <el-form-item label="贡献度 (%)">
          <el-input-number
            v-model="newMemberContribution"
            :min="0"
            :max="100"
            :precision="2"
            controls-position="right"
            style="width: 100%;"
          ></el-input-number>
        </el-form-item>
        
        <el-form-item label="绩效评级">
          <el-input-number
            v-model.number="newMemberRating"
            :min="1"
            :max="10"
            :precision="0"
            controls-position="right"
            style="width: 100%;"
            placeholder="输入 1-10 评分 (可选)"
          ></el-input-number>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="addMemberDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAddMember" :loading="memberLoading">确认添加</el-button>
      </template>
    </el-dialog>
    
    <el-dialog v-model="editMemberDialogVisible" :title="`编辑成员: ${editMemberForm.name}`" width="40%">
      <el-form :model="editMemberForm" ref="editMemberFormRef" label-width="100px">
        <el-form-item label="员工 ID">
          <el-input :model-value="editMemberForm.employee_id" disabled></el-input>
        </el-form-item>
        <el-form-item
          label="项目角色"
          prop="role"
          :rules="[{ required: true, message: '角色不能为空' }]"
        >
          <el-input v-model="editMemberForm.role" placeholder="例如：开发人员/测试人员"></el-input>
        </el-form-item>
        <el-form-item
          label="贡献度 (%)"
          prop="contribution"
          :rules="[{ required: true, message: '贡献度不能为空' }]"
        >
          <el-input-number
            v-model="editMemberForm.contribution"
            :min="0"
            :max="100"
            :precision="2"
            controls-position="right"
            style="width: 100%;"
          ></el-input-number>
        </el-form-item>
        
        <el-form-item label="绩效评级" prop="performance_rating">
          <el-input-number
            v-model.number="editMemberForm.performance_rating"
            :min="1"
            :max="10"
            :precision="0"
            controls-position="right"
            style="width: 100%;"
            placeholder="输入 1-10 评分"
          ></el-input-number>
        </el-form-item>
        
      </el-form>
      <template #footer>
        <el-button @click="editMemberDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleEditMember" :loading="memberLoading">保存修改</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus } from '@element-plus/icons-vue';
// 假设您在 '@/api/project' 中定义了获取项目详情和成员管理的函数
import {
    getProjectById,
    getProjectMembers,
    addProjectMember,
    deleteProjectMember
} from '@/api/project';
// 假设您在 '@/api/employee' 中定义了获取所有员工的函数
import { getEmployeeList } from '@/api/employee';

const route = useRoute();

// 从路由参数获取项目 ID
const projectId = ref(route.params.id);
const project = ref({});
const projectMembers = ref([]);
const allEmployees = ref([]); // 所有员工列表
const loading = ref(false);
const memberLoading = ref(false);
const error = ref('');

// 【新增/修改】添加成员的状态变量
const addMemberDialogVisible = ref(false);
const newMemberId = ref(null);
const newMemberRole = ref('成员');
const newMemberContribution = ref(0.0); // 新增贡献度
const newMemberRating = ref(null); // 新增绩效评级

// 🎯 新增编辑成员状态变量和表单引用
const editMemberDialogVisible = ref(false);
const editMemberForm = ref({
    employee_id: null,
    name: '', // 仅用于显示
    role: '',
    contribution: 0.0,
    performance_rating: null,
});
const editMemberFormRef = ref(null); // 用于表单校验

// Computed properties for display logic
const pageTitle = computed(() => `项目详情: ${project.value.project_name || '加载中...'}`);

// 过滤出当前不在项目中的员工，作为添加选项
const availableEmployees = computed(() => {
    const memberIds = new Set(projectMembers.value.map(m => m.employee_id));
    return allEmployees.value.filter(e => !memberIds.has(e.employee_id));
});

// 状态标签颜色
const getStatusTagType = (status) => {
    switch (status) {
        case '进行中': return 'success';
        case '已完成': return 'primary';
        case '已暂停': return 'warning';
        default: return 'info';
    }
};

// --- Data Fetching Logic ---

// 获取所有员工列表 (用于添加成员的下拉框)
const fetchAllEmployees = async () => {
    try {
        const res = await getEmployeeList();
        allEmployees.value = Array.isArray(res) ? res : (Array.isArray(res.data) ? res.data : []);
    } catch (err) {
        console.error('获取所有员工失败:', err);
    }
}

// 获取项目详情和成员列表
const fetchProjectData = async () => {
    if (!projectId.value) {
        error.value = "缺少项目 ID 参数";
        return;
    }

    loading.value = true;
    error.value = '';
    try {
        // 1. Fetch Project Details
        const projectData = await getProjectById(projectId.value);
        
        project.value = {
            project_id: projectData.project_id || projectId.value,
            project_name: projectData.project_name || '加载失败',
            manager_name: projectData.manager_name || 'N/A',
            status: projectData.status || '待开始',
            start_date: projectData.start_date ? projectData.start_date.substring(0, 10) : 'N/A',
            end_date: projectData.end_date ? projectData.end_date.substring(0, 10) : 'N/A',
            description: projectData.description || '无详细描述。',
            // ... 其他字段
        };

        // 2. Fetch Project Members
        const membersData = await getProjectMembers(projectId.value);
        
        // 确保使用正确的字段名 (name)
        projectMembers.value = (Array.isArray(membersData) ? membersData : []).map(m => ({
            ...m,
            // 确保有一个 name 字段用于表格和弹窗显示，如果后端返回的是 name
            employee_name: m.name || m.employee_name,
            name: m.name || m.employee_name, // 确保 name 存在
            // 确保 performance_rating 在前端显示时是数字或 null
            performance_rating: m.performance_rating !== undefined && m.performance_rating !== null
                                ? Number(m.performance_rating)
                                : null,
        }));

    } catch (err) {
        console.error('Failed to fetch project details:', err);
        error.value = `数据加载失败：${err.message || '请检查 API 接口和网络连接。'}`;
        ElMessage.error(error.value);
    } finally {
        loading.value = false;
    }
};

// --- Member Management Logic ---

// 【修改】打开添加成员对话框，增加重置贡献度和评级
const openAddMemberDialog = () => {
    newMemberId.value = null;
    newMemberRole.value = '成员'; // 重置角色默认值
    newMemberContribution.value = 0.0; // 重置贡献度
    newMemberRating.value = null; // 重置绩效评级
    addMemberDialogVisible.value = true;
}

// 【修改】添加成员，发送贡献度和评级
const handleAddMember = async () => {
    if (!newMemberId.value) {
        ElMessage.warning('请选择要添加的员工');
        return;
    }

    memberLoading.value = true;
    try {
        // 关键：构造包含所有字段的 JSON 对象
        const memberData = {
            employee_id: newMemberId.value,
            role: newMemberRole.value || '成员',
            contribution: newMemberContribution.value,
            performance_rating: newMemberRating.value
        };
        
        await addProjectMember(projectId.value, memberData);
        ElMessage.success('成员添加成功！');

        addMemberDialogVisible.value = false;
        await fetchProjectData(); // 刷新项目成员列表
    } catch (error) {
        console.error('添加成员失败:', error);
        
        const errorMessage = error.response?.data?.message || error.message || '请检查后端接口。';
        ElMessage.error(`添加成员失败: ${errorMessage}`);
    } finally {
        memberLoading.value = false;
    }
}

// 🎯 新增：打开编辑成员对话框 (保持不变)
const openEditMemberDialog = (member) => {
    // 复制当前成员的数据到表单，防止直接修改列表数据
    editMemberForm.value = {
        employee_id: member.employee_id,
        name: member.name, // 成员姓名
        role: member.role,
        // 确保 contribution 是数字类型
        contribution: parseFloat(member.contribution) || 0.0,
        // 确保 performance_rating 是数字或 null
        performance_rating: member.performance_rating || null,
    };
    // 重置校验状态
    editMemberFormRef.value?.clearValidate();
    editMemberDialogVisible.value = true;
};

// 🎯 新增：处理编辑成员的逻辑 (保持不变)
const handleEditMember = async () => {
    // 1. 触发表单校验
    if (!editMemberFormRef.value) return;
    await editMemberFormRef.value.validate(async (valid) => {
        if (valid) {
            memberLoading.value = true;
            try {
                // 构造后端期望的 JSON 对象 (POST /api/projects/<id>/members)
                const memberData = {
                    employee_id: editMemberForm.value.employee_id,
                    role: editMemberForm.value.role,
                    contribution: editMemberForm.value.contribution,
                    // 核心：直接发送绑定的 number 或 null，后端处理 INT 类型
                    performance_rating: editMemberForm.value.performance_rating
                };
                
                // 核心：使用 addProjectMember (POST) 接口实现更新逻辑
                await addProjectMember(projectId.value, memberData);

                ElMessage.success(`成员 ${editMemberForm.value.name} 信息更新成功！`);
                editMemberDialogVisible.value = false;
                await fetchProjectData(); // 刷新项目成员列表
            } catch (error) {
                console.error('更新成员信息失败:', error);
                const errorMessage = error.response?.data?.message || error.message || '请检查 API 接口。';
                ElMessage.error(`更新失败: ${errorMessage}`);
            } finally {
                memberLoading.value = false;
            }
        }
    });
};


// 移除成员 (保持不变)
const handleRemoveMember = (row) => {
    ElMessageBox.confirm(`确定要将员工 ${row.name} 从项目中移除吗?`, '警告', {
        confirmButtonText: '确定移除',
        cancelButtonText: '取消',
        type: 'warning',
    }).then(async () => {
        try {
            // 使用 deleteProjectMember(projectId, employeeId)
            await deleteProjectMember(projectId.value, row.employee_id);
            ElMessage.success('成员移除成功！');
            await fetchProjectData(); // 刷新项目成员列表
        } catch (error) {
            console.error('移除成员失败:', error);
            // 改进错误消息显示：捕获后端 400 响应中的具体信息
            const errorMessage = error.response?.data?.message || error.message || '请检查后端接口。';
            ElMessage.error(`移除失败: ${errorMessage}`);
        }
    }).catch(() => {});
}


onMounted(() => {
    fetchAllEmployees(); // 确保先加载所有员工
    fetchProjectData();
});
</script>

<style scoped>
.project-detail-container {
    padding: 20px;
    background-color: #f5f7fa;
    min-height: calc(100vh - 50px);
}

.box-card {
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.project-info-table :deep(.el-descriptions__title) {
    font-size: 18px;
    font-weight: 600;
}

.member-section {
    margin-top: 30px;
}

.member-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 5px;
    border-bottom: 2px solid #ebeef5;
}

.member-header h3 {
    margin: 0;
    color: #303133;
}

.error-message {
    margin-top: 20px;
}
</style>