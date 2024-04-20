import Vue from 'vue'
import VueRouter from 'vue-router'
import StudentInfo from '@/components/contentpages/StudentInfo.vue'
import CourseInfo from '@/components/contentpages/CourseInfo.vue'
import ScoreInfo from '@/components/contentpages/ScoreInfo.vue'
import AboutProject from '@/components/contentpages/AboutProject.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        redirect: '/student-info'
    },
    {
        path: '/student-info',
        name: 'StudentInfo',
        component: StudentInfo
    },
    {
        path: '/course-info',
        name: 'CourseInfo',
        component: CourseInfo
    },
    {
        path: '/score-info',
        name: 'ScoreInfo',
        component: ScoreInfo
    },
    {
        path: '/about-project',
        name: 'AboutProject',
        component: AboutProject
    },
    // 其他路由...
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router