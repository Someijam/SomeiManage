<template>
    <a-layout class="dash-main-index">
        <a-affix :offset-top="top">
            <a-layout-header class="dash-head-navbar">
                <div class="dash-head-navbar-left">
                    <router-link to="/about" @click="click_logo">
                        <img src="../assets/avatar_logo.svg" alt="logo" />
                        <span class="logo-text">Student Manage System</span>
                    </router-link>
                </div>
                <div class="dash-head-navbar-right">
                    <a-input-search class="dash-head-navbar-search" v-model:value="dash_search_input" placeholder="输入学号以查找" @search="onSearch" />
                    <a-drawer v-model:open="dash_search_drawerOpen" class="dash-head-navbar-search-drawer" title="查询结果" placement="right"
                        @after-open-change="afterOpenChange">
                        <a-descriptions title="个人信息" :column="2">
                            <a-descriptions-item label="姓名">
                                {{ dash_search_person_data.s_name }}
                            </a-descriptions-item>
                            <a-descriptions-item label="学号">
                                {{ dash_search_person_data.s_no }}
                            </a-descriptions-item>
                            <a-descriptions-item label="性别">
                                {{ dash_search_person_data.s_sex }}
                            </a-descriptions-item>
                            <a-descriptions-item label="年龄">
                                {{ dash_search_person_data.s_age }}
                            </a-descriptions-item>
                            <a-descriptions-item label="专业">
                                {{ dash_search_person_data.s_dept }}
                            </a-descriptions-item>
                            <a-descriptions-item label="奖学金">
                                {{ dash_search_person_data.s_scholarship }}
                            </a-descriptions-item>
                        </a-descriptions>
                        <a-divider />
                        <a-typography-title :level="5">选课信息</a-typography-title>
                        <a-table :columns="dash_search_columns" :data-source="dash_search_course_dataSource" size="small">
                        </a-table>
                    </a-drawer>
                </div>
            </a-layout-header>
        </a-affix>
        <a-layout>
            <a-affix :offset-top="64">
                <a-layout-sider class="dash-body-sidebar" breakpoint="lg" collapsed-width="0" @collapse="onCollapse"
                    @breakpoint="onBreakpoint">
                    <a-menu class="dash-body-sidebar-items" v-model:selectedKeys="dash_sidebar_selectedKeys" theme="light" mode="inline">
                        <a-menu-item key="1">
                            <user-outlined />
                            <router-link to="/student-info"><span class="nav-text">学生信息</span></router-link>
                        </a-menu-item>
                        <a-menu-item key="2">
                            <video-camera-outlined />
                            <router-link to="/course-info"><span class="nav-text">课程信息</span></router-link>
                        </a-menu-item>
                        <a-menu-item key="3">
                            <upload-outlined />
                            <router-link to="/score-info"><span class="nav-text">成绩信息</span></router-link>
                        </a-menu-item>
                        <a-menu-item key="4">
                            <user-outlined />
                            <router-link to="/about"><span class="nav-text">关于项目</span></router-link>
                        </a-menu-item>
                    </a-menu>
                </a-layout-sider>
            </a-affix>
            <a-layout class="dash-body-content">
                <a-layout-content :style="{ margin: '24px 16px 0' }">
                    <router-view></router-view>
                </a-layout-content>
                <a-layout-footer style="text-align: center">
                    Created by Someijam 2024 (Using Ant Design ©2018 )
                </a-layout-footer>
            </a-layout>
        </a-layout>
    </a-layout>
</template>

<script setup>
import { cloneDeep } from 'lodash-es';
import { ref } from 'vue';

const dash_sidebar_selectedKeys = ref(['4']);
const dash_search_drawerOpen = ref(false);
const dash_search_columns = [
  {
    title: '编号',
    dataIndex: 'c_no',
  },
  {
    title: '课程名称',
    dataIndex: 'c_name',
  },
  {
    title: '成绩',
    dataIndex: 'c_score',
  },
  {
    title: '学分',
    dataIndex: 'c_credit',
  },
];
const dash_search_course_data = [];
const dash_search_person_data = ref({
    key: '1',
    s_name: '刘伟',
    s_no: '202100000',
    s_sex: '男',
    s_age: 38,
    s_dept: 'CS',
    s_scholarship: '是'
});
const dash_search_course_dataSource = ref(dash_search_course_data);
const dash_search_input = ref('');

const onCollapse = (collapsed, type) => {
    console.log(collapsed, type);
};
const onBreakpoint = broken => {
    console.log(broken);
};
const click_logo = () => {
    dash_sidebar_selectedKeys.value = ['4'];
};

const getPersonInfo = (sno) => {
    console.log('getPersonInfo:', sno);
    fetch(`http://localhost:5880/query/singlestuinfo/${sno}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            dash_search_person_data.value = {
                key: '1',
                s_name: data.sname,
                s_no: data.sno,
                s_sex: data.ssex,
                s_age: data.sage,
                s_dept: data.sdept,
                s_scholarship: data.scholarship
            }
        })
        .catch(err => console.log(err));
};

const getStuScoreInfo = (sno) => {
    console.log('getStuScoreInfo:', sno);
    fetch(`http://localhost:5880/query/singlestuscore/${sno}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            dash_search_course_data.value = data.dataarr.map((item, index) => {
                return {
                    key: index,
                    c_no: item.cno,
                    c_name: item.cname,
                    c_score: item.grade,
                    c_credit: item.credit
                }
            });
            dash_search_course_dataSource.value = cloneDeep(dash_search_course_data.value);
        })
        .catch(err => console.log(err));
};

const onSearch = () => {
    getPersonInfo(dash_search_input.value);
    getStuScoreInfo(dash_search_input.value);
    dash_search_drawerOpen.value = true;
};
</script>

<style scoped>
#components-layout-demo-responsive .logo {
    height: 32px;
    background: rgba(255, 255, 255, 0.2);
    margin: 16px;
}

.dash-main-index {
    min-height: 100vh;
}

.site-layout-sub-header-background {
    background: #fff;
}

.site-layout-background {
    background: #fff;
}

[data-theme='dark'] .site-layout-sub-header-background {
    background: #141414;
}

.dash-head-navbar {
    background: #36558f;
    padding: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.dash-head-navbar-left {
    padding-left: 2%;
    justify-content: start;
    display: flex;
    align-items: center;
}

.dash-head-navbar-left img {
    width: 40px;
    height: auto;
    margin-inline-end: .8rem;
}

.logo-text {
    color: #fff;
    font-size: 1.25rem;
    font-weight: 400;
}

.dash-head-navbar-right {
    width: 20%;
    padding-right: 2%;
    justify-content: end;
    display: flex;
    align-items: center;
}

.dash-body-sidebar-items {
    min-height: 100vh;
    background: #eeeeee;
}
</style>