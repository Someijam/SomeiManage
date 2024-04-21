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
                    <a-input-search class="dash-head-navbar-search" v-model:value="value" placeholder="输入学号以查找" @search="onSearch" />
                    <a-drawer v-model:open="dash_search_drawerOpen" class="dash-head-navbar-search-drawer" title="查询结果" placement="right"
                        @after-open-change="afterOpenChange">
                        <a-descriptions title="个人信息" :column="2">
                            <a-descriptions-item label="姓名">刘伟</a-descriptions-item>
                            <a-descriptions-item label="学号">202100000</a-descriptions-item>
                            <a-descriptions-item label="性别">男</a-descriptions-item>
                            <a-descriptions-item label="年龄">38</a-descriptions-item>
                            <a-descriptions-item label="专业">CS</a-descriptions-item>
                            <a-descriptions-item label="奖学金">是</a-descriptions-item>
                        </a-descriptions>
                        <a-divider />
                        <a-typography-title :level="5">选课信息</a-typography-title>
                        <a-table :columns="dash_search_columns" :data-source="dash_search_data" size="small">
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
const dash_search_data = [
    {
        key: '1',
        c_no: 'C001',
        c_name: '计算机网络',
        c_score: 90,
        c_credit: 3,
    },
    {
        key: '2',
        c_no: 'C002',
        c_name: '数据库系统',
        c_score: 85,
        c_credit: 3,
    },
    {
        key: '3',
        c_no: 'C003',
        c_name: '数据结构',
        c_score: 88,
        c_credit: 3,
    },
    {
        key: '4',
        c_no: 'C004',
        c_name: '操作系统',
        c_score: 92,
        c_credit: 3,
    },
    {
        key: '5',
        c_no: 'C005',
        c_name: '软件工程',
        c_score: 87,
        c_credit: 3,
    },
    {
        key: '6',
        c_no: 'C006',
        c_name: '编译原理',
        c_score: 89,
        c_credit: 3,
    },
    {
        key: '7',
        c_no: 'C007',
        c_name: '计算机组成原理',
        c_score: 91,
        c_credit: 3,
    },
    {
        key: '8',
        c_no: 'C008',
        c_name: '计算机图形学',
        c_score: 86,
        c_credit: 3,
    },
    {
        key: '9',
        c_no: 'C009',
        c_name: '计算机视觉',
        c_score: 93,
        c_credit: 3,
    },
    {
        key: '10',
        c_no: 'C010',
        c_name: '机器学习',
        c_score: 94,
        c_credit: 3,
    },
    {
        key: '11',
        c_no: 'C011',
        c_name: '机器学习2',
        c_score: 94,
        c_credit: 3,
    },
];

const onCollapse = (collapsed, type) => {
    console.log(collapsed, type);
};
const onBreakpoint = broken => {
    console.log(broken);
};
const click_logo = () => {
    dash_sidebar_selectedKeys.value = ['4'];
};
const onSearch = () => {
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