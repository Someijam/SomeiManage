<template>
    <div class="student-info-top">
        <a-typography-title :level="3">学生基本信息</a-typography-title>
        <div>
            <a-button type="primary" style="margin-inline-end: .5em;">
                <template #icon>
                    <ReloadOutlined />
                </template>
            </a-button>
            <a-button type="primary" style="margin-bottom: 8px">新同学……</a-button>
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