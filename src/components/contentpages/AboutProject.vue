<template>
    <a-typography>
        <a-typography-title :level="2">介绍</a-typography-title>
        <a-typography-paragraph>
            基于Vue的学生管理系统前端页面。
        </a-typography-paragraph>
        <a-typography-paragraph>
            项目已在
            <GithubOutlined />
            <a href="https://github.com/Someijam/SomeiManage" target="_blank">Github</a>
            上开源。保留为Someijam所有的权利。
        </a-typography-paragraph>

    </a-typography>
</template>
<script setup>
import {
    GithubOutlined
} from '@ant-design/icons-vue';
</script>