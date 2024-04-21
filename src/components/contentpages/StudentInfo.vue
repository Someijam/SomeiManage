<template>
    <div class="student-info-top">
        <a-typography-title :level="3">学生基本信息</a-typography-title>
        <div>
            <a-button type="primary" style="margin-inline-end: .5em;">
                <template #icon>
                    <ReloadOutlined />
                </template>
            </a-button>
            <a-button type="primary" style="margin-bottom: 8px" @click="show_drawer">+ 新的同学</a-button>
            <a-drawer title="添加新同学" :width="480" :open="open" :body-style="{ paddingBottom: '80px' }"
                :footer-style="{ textAlign: 'right' }" @close="onClose">
                <a-form :model="form" :rules="rules" layout="vertical">
                    <a-row :gutter="16">
                        <a-col :span="12">
                            <a-form-item label="姓名" name="add_s_name">
                                <a-input v-model:value="form.add_s_name" placeholder="刘伟" />
                            </a-form-item>
                        </a-col>
                        <a-col :span="12">
                            <a-form-item label="学号" name="add_s_no">
                                <a-input v-model:value="form.add_s_no" placeholder="202112000" />
                            </a-form-item>
                        </a-col>
                    </a-row>
                    <a-row :gutter="16">
                        <a-col :span="12">
                            <a-form-item label="性别" name="add_s_sex">
                                <a-radio-group v-model:value="form.add_s_sex">
                                    <a-radio-button value="男">男</a-radio-button>
                                    <a-radio-button value="女">女</a-radio-button>
                                </a-radio-group>
                            </a-form-item>
                        </a-col>
                        <a-col :span="12">
                            <a-form-item label="年龄" name="add_s_age">
                                <a-input v-model:value="form.add_s_age" placeholder="38" />
                            </a-form-item>
                        </a-col>
                    </a-row>
                    <a-row :gutter="16">
                        <a-col :span="12">
                            <a-form-item label="专业" name="add_s_dept">
                                <a-select v-model:value="form.add_s_dept">
                                    <a-select-option value="IS">IS</a-select-option>
                                    <a-select-option value="CS">CS</a-select-option>
                                    <a-select-option value="MA">MA</a-select-option>
                                </a-select>
                            </a-form-item>
                        </a-col>
                        <a-col :span="12">
                            <a-form-item label="奖学金" name="add_s_scholarship">
                                <a-radio-group v-model:value="form.add_s_scholarship">
                                    <a-radio-button value="是">是</a-radio-button>
                                    <a-radio-button value="否">否</a-radio-button>
                                </a-radio-group>
                            </a-form-item>
                        </a-col>
                    </a-row>
                </a-form>
                <template #extra>
                    <a-space>
                        <a-button @click="onClose">取消</a-button>
                        <a-button type="primary" @click="onClose">添加</a-button>
                    </a-space>
                </template>
            </a-drawer>
        </div>
    </div>
    <a-table :columns="columns" :data-source="dataSource" bordered>
        <template #bodyCell="{ column, text, record }">
            <template v-if="['name', 'age', 'key'].includes(column.dataIndex)">
                <div>
                    <a-input v-if="editableData[record.key]" v-model:value="editableData[record.key][column.dataIndex]"
                        style="margin: -5px 0" />
                    <template v-else>
                        {{ text }}
                    </template>
                </div>
            </template>
            <template v-else-if="column.dataIndex === 'sex'">
                <div>
                    <a-radio-group v-if="editableData[record.key]"
                        v-model:value="editableData[record.key][column.dataIndex]" style="margin: -5px 0">
                        <a-radio-button value="男">男</a-radio-button>
                        <a-radio-button value="女">女</a-radio-button>
                    </a-radio-group>
                    <template v-else>
                        {{ text }}
                    </template>
                </div>
            </template>
            <template v-else-if="column.dataIndex === 'dept'">
                <div>
                    <a-select v-if="editableData[record.key]" v-model:value="editableData[record.key][column.dataIndex]"
                        style="margin: -5px 0">
                        <a-select-option value="IS">IS</a-select-option>
                        <a-select-option value="CS">CS</a-select-option>
                        <a-select-option value="MA">MA</a-select-option>
                    </a-select>
                    <template v-else>
                        {{ text }}
                    </template>
                </div>
            </template>
            <template v-else-if="column.dataIndex === 'scholarship'">
                <div>
                    <a-radio-group v-if="editableData[record.key]"
                        v-model:value="editableData[record.key][column.dataIndex]" style="margin: -5px 0">
                        <a-radio-button value="是">是</a-radio-button>
                        <a-radio-button value="否">否</a-radio-button>
                    </a-radio-group>
                    <template v-else>
                        {{ text }}
                    </template>
                </div>
            </template>
            <template v-else-if="column.dataIndex === 'operation'">
                <div class="editable-row-operations">
                    <span v-if="editableData[record.key]">
                        <a-typography-link @click="save(record.key)">保存</a-typography-link>
                        <a-popconfirm title="是否放弃修改？" ok-text="放弃" cancel-text="暂不" @confirm="cancel(record.key)">
                            <a>放弃</a>
                        </a-popconfirm>
                    </span>
                    <span v-else>
                        <a @click="edit(record.key)">编辑</a>
                        <a-popconfirm v-if="dataSource.length" title="是否删除该行？" ok-text="删除" cancel-text="取消"
                            @confirm="onDelete(record.key)">
                            <a style="color: red;">删除</a>
                        </a-popconfirm>
                    </span>
                </div>
            </template>
        </template>
    </a-table>
</template>
<script setup>
import { cloneDeep } from 'lodash-es';
import { reactive, ref } from 'vue';
import {
    ReloadOutlined
} from '@ant-design/icons-vue';
const columns = [
    {
        title: '学号',
        dataIndex: 'key',
        width: '15%',
    },
    {
        title: '姓名',
        dataIndex: 'name',
        width: '20%',
    },
    {
        title: '性别',
        dataIndex: 'sex',
        width: '12%',
    },
    {
        title: '年龄',
        dataIndex: 'age',
        width: '10%',
    },
    {
        title: '专业',
        dataIndex: 'dept',
        width: '20%',
    },
    {
        title: '奖学金',
        dataIndex: 'scholarship',
        width: '12%',
    },
    {
        title: '操作',
        dataIndex: 'operation',
    },
];
const data = [];
for (let i = 0; i < 100; i++) {
    data.push({
        key: (202112000 + i).toString(),
        sex: i % 3 === 0 ? '男' : '女',
        name: `Edrward ${i}`,
        age: 32,
        dept: `CS`,
        scholarship: i % 2 === 0 ? '是' : '否',
    });
}
const dataSource = ref(data);
const editableData = reactive({});
const edit = key => {
    editableData[key] = cloneDeep(dataSource.value.filter(item => key === item.key)[0]);
};
const save = key => {
    Object.assign(dataSource.value.filter(item => key === item.key)[0], editableData[key]);
    delete editableData[key];
};
const cancel = key => {
    delete editableData[key];
};
const onDelete = key => {
    dataSource.value = dataSource.value.filter(item => key !== item.key);
};

const form = reactive({
    add_s_name: '',
    add_s_no: '',
    add_s_sex: '',
    add_s_age: '',
    add_s_dept: '',
    add_s_scholarship: '',
});
const rules = {
    add_s_name: [
        {
            required: true,
            message: 'Please enter user name',
        },
    ],
    add_s_no: [
        {
            required: true,
            message: 'Please enter user name',
        },
    ],
    add_s_sex: [
        {
            required: true,
            message: 'Please enter user name',
        },
    ],
    add_s_age: [
        {
            required: true,
            message: 'Please enter user name',
        },
    ],
    add_s_dept: [
        {
            required: true,
            message: 'Please enter user name',
        },
    ],
    add_s_scholarship: [
        {
            required: true,
            message: 'Please enter user name',
        },
    ],
};
const open = ref(false);
const show_drawer = () => {
    open.value = true;
};
const onClose = () => {
    open.value = false;
};
</script>
<style scoped>
.editable-row-operations a {
    margin-right: 8px;
}

.student-info-top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 16px;
}
</style>