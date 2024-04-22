<template>
    <div class="score-body-top">
        <a-typography-title :level="3">学生成绩管理</a-typography-title>
        <div>
            <a-select style="margin-inline-end: .5em; min-width:120px;" placeholder="选择专业系(CS)" @change="onChangeDept">
                <a-select-option value="IS">IS</a-select-option>
                <a-select-option value="CS">CS</a-select-option>
                <a-select-option value="MA">MA</a-select-option>
            </a-select>
            <a-select style="margin-inline-end: .5em; min-width:90px;" placeholder="选择课程(1)" @change="onChangeCourse">
                <!-- <a-select-option v-for="item in course_list_dataSource" :value="item.value">{{ item.label }}</a-select-option> -->
                <a-select-option v-for="item in course_list_dataSource" :value="item.value" :key="item.value">{{ item.label }}</a-select-option>
                <!-- <a-select-option value="1">1</a-select-option>
                <a-select-option value="2">2</a-select-option>
                <a-select-option value="3">3</a-select-option>
                <a-select-option value="4">4</a-select-option> -->
            </a-select>
            <a-button type="primary" style="margin-inline-end: 1.5em;" @click="onRefresh">
                <template #icon>
                    <ReloadOutlined />
                </template>
            </a-button>
            <a-button type="primary" style="margin-bottom: 8px" @click="show_drawer">+ 录入成绩</a-button>
            <a-drawer title="录入成绩" :open="score_newbutton_open" :body-style="{ paddingBottom: '80px' }"
                :footer-style="{ textAlign: 'right' }" @close="onClose">
                <a-form :model="score_newbutton_form" :rules="score_newbutton_rules" layout="vertical">
                    <a-row :gutter="16">
                        <a-col :span="12">
                            <a-form-item label="学号" name="addscore_s_no">
                                <a-input v-model:value="score_newbutton_form.addscore_s_no" placeholder="CS101" />
                            </a-form-item>
                        </a-col>
                    </a-row>
                    <a-row :gutter="16">
                        <a-col :span="12">
                            <a-form-item label="课程编号" name="addscore_c_no">
                                <a-input v-model:value="score_newbutton_form.addscore_c_no" placeholder="CS101" />
                            </a-form-item>
                        </a-col>
                    </a-row>
                    <a-row :gutter="16">
                        <a-col :span="12">
                            <a-form-item label="成绩" name="addscore_sc">
                                <a-input v-model:value="score_newbutton_form.addscore_sc" placeholder="CS101" />
                            </a-form-item>
                        </a-col>
                    </a-row>
                </a-form>
                <template #extra>
                    <a-space>
                        <a-button @click="onClose">取消</a-button>
                        <a-button type="primary" @click="onSubmit">确定</a-button>
                    </a-space>
                </template>
            </a-drawer>
        </div>
    </div>
    <div class="score-body-mid">
        <div>
            <a-descriptions title="统计">
                <a-descriptions-item label="平均成绩">{{ average_score.valueOf() }}</a-descriptions-item>
                <a-descriptions-item label="最好成绩">{{ max_score.valueOf() }}</a-descriptions-item>
                <a-descriptions-item label="最差成绩">{{ min_score.valueOf() }}</a-descriptions-item>
                <a-descriptions-item label="优秀率">{{ excellent_rate.valueOf() }}%</a-descriptions-item>
                <a-descriptions-item label="不及格人数">{{ fail_num.valueOf() }}</a-descriptions-item>
            </a-descriptions>
        </div>
    </div>
    <div class="score-body-table">
        <a-table :columns="score_table_columns" :data-source="score_table_dataSource" bordered size="small">
            <template #bodyCell="{ column, text, record }">
                <template v-if="['score'].includes(column.dataIndex)">
                    <div>
                        <a-input v-if="score_editableData[record.key]"
                            v-model:value="score_editableData[record.key][column.dataIndex]" style="margin: -5px 0" />
                        <template v-else>
                            {{ text }}
                        </template>
                    </div>
                </template>
                <template v-else-if="column.dataIndex === 'operation'">
                    <div class="score-editable-row-operations">
                        <span v-if="score_editableData[record.key]">
                            <a-typography-link @click="save(record.key)">保存</a-typography-link>
                            <a-popconfirm title="是否放弃修改？" ok-text="放弃" cancel-text="暂不" @confirm="cancel(record.key)">
                                <a>放弃</a>
                            </a-popconfirm>
                        </span>
                        <span v-else>
                            <a @click="edit(record.key)">编辑</a>
                            <a-popconfirm v-if="score_table_dataSource.length" title="是否删除该行？" ok-text="删除" cancel-text="取消"
                                @confirm="onDelete(record.key)">
                                <a style="color: red;">删除</a>
                            </a-popconfirm>
                        </span>
                    </div>
                </template>
            </template>
        </a-table>
    </div>

</template>

<script setup>
import { cloneDeep } from 'lodash-es';
import { reactive, ref } from 'vue';
import { ReloadOutlined } from '@ant-design/icons-vue';

const score_table_columns = [
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
        title: '排名',
        dataIndex: 'rank',
        width: '13%',
    },
    {
        title: '操作',
        dataIndex: 'operation',
    },
];
const score_table_data = [];
const score_table_dataSource = ref(score_table_data);
const score_editableData = reactive({});
const score_newbutton_form = reactive({
    addscore_s_no: '',
    addscore_c_no: '',
    addscore_sc: '',
});

// 课程列表
const course_list_data = []; // {value: '1', label: '数据库'} ...
const course_list_dataSource = ref(course_list_data);

// 选择框项目
const selected_dept = ref('CS');
const selected_cno = ref('1');

// 指标文本
const average_score = ref('0.0');
const excellent_rate = ref('0.0');
const max_score = ref('0');
const min_score = ref('0');
const fail_num = ref('0');

const score_newbutton_rules = {
    addscore_s_no: [
        { required: true, message: '请输入学号' },
    ],
    addscore_c_no: [
        { required: true, message: '请输入课程编号' },
    ],
    addscore_sc: [
        { required: true, message: '请输入成绩' },
    ],
};
const score_newbutton_open = ref(false);

const edit = key => {
    score_editableData[key] = cloneDeep(score_table_dataSource.value.filter(item => key === item.key)[0]);
};
const save = key => {
    Object.assign(score_table_dataSource.value.filter(item => key === item.key)[0], score_editableData[key]);
    var data_to_update={
        update_s_no: score_editableData[key].s_no,
        update_c_no: score_editableData[key].c_no,
        update_sc: score_editableData[key].score,
    }
    fetch('http://localhost:5880/update/scorerecord', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data_to_update),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            getScores(selected_dept.value,selected_cno.value);
        });
    delete score_editableData[key];
};
const cancel = key => {
    delete score_editableData[key];
};
const onDelete = key => {
    // score_table_dataSource.value = score_table_dataSource.value.filter(item => key !== item.key);
    var data_to_delete={
        delete_s_no: score_table_dataSource.value.filter(item => key === item.key)[0].s_no,
        delete_c_no: score_table_dataSource.value.filter(item => key === item.key)[0].c_no,
    }
    fetch('http://localhost:5880/delete/scorerecord', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data_to_delete),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            getScores(selected_dept.value,selected_cno.value);
        });
};
const show_drawer = () => {
    score_newbutton_open.value = true;
};
const onClose = () => {
    score_newbutton_open.value = false;
};

const onSubmit = () => {
    console.log(score_newbutton_form);
    fetch('http://localhost:5880/add/scorerecord', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(score_newbutton_form),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            getScores(selected_dept.value,selected_cno.value);
        });
    score_newbutton_open.value = false;
};

const onChangeDept = (value) => {
    selected_dept.value = value;
};

const onChangeCourse = (value) => {
    selected_cno.value = value;
};

const getScores = (dept,cno) => {
    fetch(`http://localhost:5880/query/scoreinfo/${dept}/${cno}`)
        .then(response => response.json())
        .then(data => {
            // console.log(data);
            score_table_data.value = data.dataarr.map((item, index) => ({
                key: index.toString(),
                s_no: item.sno,
                s_name: item.sname,
                c_no: item.cno,
                c_name: item.cname,
                score: item.grade,
                rank: (index + 1).toString(),
            }));
            score_table_dataSource.value = cloneDeep(score_table_data.value);
            average_score.value = data.average_grade;
            excellent_rate.value = data.excellent_rate;
            max_score.value = (data.max_grade).toString();
            min_score.value = (data.min_grade).toString();
            fail_num.value = (data.fail_count).toString();
        });
};

const getCourseList = () => {
    fetch('http://localhost:5880/query/coursesinfo')
        .then(response => response.json())
        .then(data => {
            // console.log(data);
            course_list_data.value = data.dataarr.map(item => ({
                value: item.key,
                label: item.name,
            }));
            course_list_dataSource.value = cloneDeep(course_list_data.value);
            // console.log(course_list_dataSource.value);
        });
};

const onRefresh = () => {
    getScores(selected_dept.value,selected_cno.value);
    getCourseList();
};

onRefresh();

</script>

<style scoped>
.score-editable-row-operations a {
    margin-right: 8px;
}

.score-body-top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 16px;
}

.score-body-mid {
    align-items: center;
    display: flex;
    justify-content: space-between;
    margin-bottom: 24px;
}
</style>