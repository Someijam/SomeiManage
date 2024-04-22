<template>
    <div class="course-body-top">
        <a-typography-title :level="3">课程基本信息</a-typography-title>
        <div>
            <a-button type="primary" style="margin-inline-end: .5em;" @click="getCourseTable">
                <template #icon>
                    <ReloadOutlined />
                </template>
            </a-button>
            <a-button type="primary" style="margin-bottom: 8px" @click="show_drawer">+ 新的课程</a-button>
            <a-drawer title="添加课程" :width="480" :open="course_newbutton_open" :body-style="{ paddingBottom: '80px' }"
                :footer-style="{ textAlign: 'right' }" @close="onClose">
                <a-form :model="course_newbutton_form" :rules="course_newbutton_rules" layout="vertical">
                    <a-row :gutter="16">
                        <a-col :span="12">
                            <a-form-item label="课程名称" name="add_c_name">
                                <a-input v-model:value="course_newbutton_form.add_c_name" placeholder="计算机组成原理" />
                            </a-form-item>
                        </a-col>
                        <a-col :span="12">
                            <a-form-item label="课程编号" name="add_c_no">
                                <a-input v-model:value="course_newbutton_form.add_c_no" placeholder="CS101" />
                            </a-form-item>
                        </a-col>
                    </a-row>
                    <a-row :gutter="16">
                        <a-col :span="12">
                            <a-form-item label="前置课程" name="add_c_pno">
                                <a-input v-model:value="course_newbutton_form.add_c_pno" placeholder="CS100" />
                            </a-form-item>
                        </a-col>
                        <a-col :span="12">
                            <a-form-item label="学分" name="add_credit">
                                <a-input v-model:value="course_newbutton_form.add_credit" placeholder="3" />
                            </a-form-item>
                        </a-col>
                    </a-row>
                </a-form>
                <template #extra>
                    <a-space>
                        <a-button @click="onClose">取消</a-button>
                        <a-button type="primary" @click="onSubmit">添加</a-button>
                    </a-space>
                </template>
            </a-drawer>
        </div>
    </div>
    <a-table :columns="course_table_columns" :data-source="course_dataSource" bordered>
        <template #bodyCell="{ column, text, record }">
            <template v-if="['c_no', 'c_name', 'c_pno','credit'].includes(column.dataIndex)">
                <div>
                    <a-input v-if="course_editableData[record.key]" v-model:value="course_editableData[record.key][column.dataIndex]"
                        style="margin: -5px 0" />
                    <template v-else>
                        {{ text }}
                    </template>
                </div>
            </template>
            <template v-else-if="column.dataIndex === 'operation'">
                <div class="course-editable-row-operations">
                    <span v-if="course_editableData[record.key]">
                        <a-typography-link @click="save(record.key)">保存</a-typography-link>
                        <a-popconfirm title="是否放弃修改？" ok-text="放弃" cancel-text="暂不" @confirm="cancel(record.key)">
                            <a>放弃</a>
                        </a-popconfirm>
                    </span>
                    <span v-else>
                        <a @click="edit(record.key)">编辑</a>
                        <a-popconfirm v-if="course_dataSource.length" title="是否删除该行？" ok-text="删除" cancel-text="取消"
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
import { ReloadOutlined } from '@ant-design/icons-vue';

const course_table_columns = [
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
        title: '前置课程',
        dataIndex: 'c_pno',
        width: '20%',
    },
    {
        title: '学分',
        dataIndex: 'credit',
        width: '10%',
    },
    {
        title: '选课人数',
        dataIndex: 'c_selectednum',
        width: '30%',
    },
    {
        title: '操作',
        dataIndex: 'operation',
    },
];
const course_table_data = [];
const course_dataSource = ref(course_table_data);
const course_editableData = reactive({});
const course_newbutton_form = reactive({
    add_c_name: '',
    add_c_no: '',
    add_c_pno: '',
    add_credit: '',
});
const course_newbutton_rules = {
    add_c_name: [
        { required: true, message: '请输入课程名称'},
    ],
    add_c_no: [
        { required: true, message: '请输入课程序号'},
    ],
    add_c_pno: [
        { required: true, message: '请输入前置课程'},
    ],
    add_credit: [
        { required: true, message: '请输入学分'},
    ], 
};
const course_newbutton_open = ref(false);

const edit = key => {
    course_editableData[key] = cloneDeep(course_dataSource.value.filter(item => key === item.key)[0]);
};
const save = key => {
    Object.assign(course_dataSource.value.filter(item => key === item.key)[0], course_editableData[key]);
    var data_to_update = {
        update_c_no: course_editableData[key].c_no,
        update_c_name: course_editableData[key].c_name,
        update_c_pno: course_editableData[key].c_pno,
        update_credit: course_editableData[key].credit,
    };
    fetch('http://localhost:5880/update/courseinfo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data_to_update)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            getCourseTable();
        });
    delete course_editableData[key];
};
const cancel = key => {
    delete course_editableData[key];
};
const onDelete = key => {
    // course_dataSource.value = course_dataSource.value.filter(item => key !== item.key);
    var data_to_delete = {
        delete_c_no: course_dataSource.value.filter(item => key === item.key)[0].c_no,
    };
    if ( 0 !== course_dataSource.value.filter(item => key === item.key)[0].c_selectednum ) {
        console.log('This course has been selected by students, cannot be deleted!');
        return;
    }
    fetch('http://localhost:5880/delete/courseinfo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data_to_delete)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            getCourseTable();
        });

};
const show_drawer = () => {
    course_newbutton_open.value = true;
};

const onSubmit = () => {
    fetch('http://localhost:5880/add/courseinfo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(course_newbutton_form)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            getCourseTable();
        });
    course_newbutton_open.value = false;
};

const onClose = () => {
    course_newbutton_open.value = false;
};

const getCourseTable = () => {
    fetch('http://localhost:5880/query/coursesinfo')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            course_table_data.value = data.dataarr.map((item, index) => ({
                key: index,
                c_no: item.key,
                c_name: item.name,
                c_pno: item.pno === null ? '(无)' : item.pno,
                credit: item.credit,
                c_selectednum: item.student_count,
            }));
            course_dataSource.value = cloneDeep(course_table_data.value);
        });
}

getCourseTable();

</script>

<style scoped>
.course-editable-row-operations a {
    margin-right: 8px;
}

.course-body-top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 16px;
}   
</style>