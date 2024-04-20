<template>
    <a-layout class="main-index">
        <a-affix :offset-top="top">
            <a-layout-header class="head-navbar">
                <div class="navbar-left">
                    <img src="../assets/avatar_logo.svg" alt="logo" />
                    <span class="logo-text">Student Manage System</span>
                </div>
                <div class="navbar-right">
                    <a-input-search class="nav-search" v-model:value="value" placeholder="输入学号以查找" @search="onSearch" />
                </div>
            </a-layout-header>
        </a-affix>
        <a-layout>
            <a-layout-sider class="body-sidebar" breakpoint="lg" collapsed-width="0" @collapse="onCollapse"
                @breakpoint="onBreakpoint">
                <a-menu class="body-sidebar" v-model:selectedKeys="selectedKeys" theme="light" mode="inline">
                    <a-menu-item key="1">
                        <user-outlined />
                        <span class="nav-text">学生信息</span>
                    </a-menu-item>
                    <a-menu-item key="2">
                        <video-camera-outlined />
                        <span class="nav-text">课程信息</span>
                    </a-menu-item>
                    <a-menu-item key="3">
                        <upload-outlined />
                        <span class="nav-text">成绩管理</span>
                    </a-menu-item>
                    <a-menu-item key="4">
                        <user-outlined />
                        <span class="nav-text">关于项目</span>
                    </a-menu-item>
                </a-menu>
            </a-layout-sider>
            <a-layout>
                <a-layout-content :style="{ margin: '24px 16px 0' }">
                    <!-- <AboutProject /> -->
                    <StudentInfo />
                </a-layout-content>
                <a-layout-footer style="text-align: center">
                    Created by Someijam (Using Ant Design ©2018 )
                </a-layout-footer>
            </a-layout>
        </a-layout>
    </a-layout>
</template>

<script setup>
import { ref } from 'vue';
// import AboutProject from './contentpages/AboutProject.vue';
import StudentInfo  from './contentpages/StudentInfo.vue';

const onCollapse = (collapsed, type) => {
    console.log(collapsed, type);
};
const onBreakpoint = broken => {
    console.log(broken);
};
const selectedKeys = ref(['4']);


</script>

<style scoped>
#components-layout-demo-responsive .logo {
    height: 32px;
    background: rgba(255, 255, 255, 0.2);
    margin: 16px;
}

.main-index {
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

.navbar-left {
    padding-left: 2%;
    justify-content: start;
    display: flex;
    align-items: center;
}
.navbar-left img {
    /* vertical-align: middle; */
    width: 40px;
    height: auto;
    margin-inline-end: .8rem;
}
.logo-text {
    color: #fff;
    font-size: 1.25rem;
    font-weight: 400;
}

.navbar-right {
    width: 20%;
    padding-right: 2%;
    justify-content: end;
    display: flex;
    align-items: center;
    /* margin-left: 20px; */
}

.head-navbar {
    background: #36558f;
    padding: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    /* box-shadow:
    inset 0 -3em 3em rgba(0, 0, 0, 0.1),
    0 0 0 2px rgb(255, 255, 255),
    0.3em 0.3em 1em rgba(0, 0, 0, 0.3); */
}

.body-sidebar {
    background: #eeeeee;
}
</style>