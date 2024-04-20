<template>
    <div class="student-info-top">
        <a-typography-title :level="3" >学生信息</a-typography-title>
        <a-button type="primary" style="margin-bottom: 8px" >新同学……</a-button>
    </div>
    <a-table :columns="columns" :data-source="dataSource" bordered>
        <template #bodyCell="{ column, text, record }">
            <template v-if="['no', 'name', 'age'].includes(column.dataIndex)">
                <div>
                    <a-input v-if="editableData[record.key]" v-model:value="editableData[record.key][column.dataIndex]"
                        style="margin: -5px 0" />
                    <template v-else>
                        {{ text }}
                    </template>
                </div>
            </template>
            <template v-else-if="column.dataIndex === 'operation'">
                <div class="editable-row-operations">
                    <span v-if="editableData[record.key]">
                        <a-typography-link @click="save(record.key)">Save</a-typography-link>
                        <a-popconfirm title="Sure to cancel?" @confirm="cancel(record.key)">
                            <a>Cancel</a>
                        </a-popconfirm>
                    </span>
                    <span v-else>
                        <a @click="edit(record.key)">Edit</a>
                    </span>
                </div>
            </template>
        </template>
    </a-table>
</template>
<script setup>
import { cloneDeep } from 'lodash-es';
import { reactive, ref } from 'vue';
const columns = [
    {
        title: '学号',
        dataIndex: 'no',
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
        width: '10%',
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
        width: '10%',
    },
    {
        title: '操作',
        dataIndex: 'operation',
    },
];
const data = [];
for (let i = 0; i < 100; i++) {
    data.push({
        no: (i+202112000).toString(),
        name: `Edward ${i}`,
        sex: i % 2 === 0 ? '男' : '女',
        age: 114,
        dept: `CS`,
        scholarship: i % 2 === 0 ? '是' : '否',
        // address: `London Park no. ${i}`,
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