import { createRouter, createWebHistory } from 'vue-router';
import StudentInfo from '@/components/contentpages/StudentInfo.vue';
import CourseInfo from '@/components/contentpages/CourseInfo.vue';
import ScoreInfo from '@/components/contentpages/ScoreInfo.vue';
import AboutProject from '@/components/contentpages/AboutProject.vue';

const routes = [
  { path: '/', redirect: '/about' },
  { path: '/student-info', component: StudentInfo },
  { path: '/course-info', component: CourseInfo },
  { path: '/score-info', component: ScoreInfo },
  { path: '/about', component: AboutProject },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;