<template>
    <div class="score-info-top">
        <a-typography-title :level="3">学生成绩管理</a-typography-title>
        <div>
            <a-button type="primary" style="margin-inline-end: .5em;">
                <template #icon>
                    <ReloadOutlined />
                </template>
            </a-button>
            <a-button type="primary" style="margin-bottom: 8px">+ 录入成绩</a-button>
        </div>
    </div>
    <a-table :columns="columns" :data-source="dataSource" bordered>
        <template #bodyCell="{ column, text, record }">
            <template v-if="['s_no', 's_name','c_no', 'c_name','score'].includes(column.dataIndex)">
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
        dataIndex: 's_no',
        width: '15%',
    },
    {
        title: '姓名',
        dataIndex: 's_name',
        width: '20%',
    },
    {
        title: '课程序号',
        dataIndex: 'c_no',
        width: '10%',
    },  
    {
        title: '课程名称',
        dataIndex: 'c_name',
        width: '20%',
    },
    {
        title: '成绩',
        dataIndex: 'score',
        width: '10%',
    },
    {
        title: ' ',
        dataIndex: 'reserve',
        width: '13%',
    },
    {
        title: '操作',
        dataIndex: 'operation',
    },
];
const data = [];
for (let i = 0; i < 10; i++) {
    data.push({
        key: i.toString(),
        s_no: (202112000+i).toString(),
        s_name: `Edward No.${i}`,
        c_no: (i+1).toString(),
        c_name: `Course ${i}`,
        score: Math.floor(Math.random() * 100),
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
</script>
<style scoped>
.editable-row-operations a {
    margin-right: 8px;
}

.score-info-top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 16px;
}   
</style>