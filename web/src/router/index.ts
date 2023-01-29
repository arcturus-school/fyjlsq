import { RouteRecordRaw, createRouter, createWebHistory } from 'vue-router';
import { useLoginState } from '@utils/hooks';

import Home from '@pages/home.vue';
import Login from '@pages/login.vue';
import Register from '@pages/register.vue';
import UserInfo from '@pages/userInfo.vue';
import Post from '@pages/post.vue';
import Admin from '@pages/admin.vue';
import Content from '@components/contents.vue';
import ArticleDetail from '@components/article.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: Home,
    children: [
      {
        path: '/',
        component: Content,
      },
      {
        path: '/article-detail/:id',
        component: ArticleDetail,
      },
    ],
  },
  {
    path: '/login',
    component: Login,
  },
  {
    path: '/register',
    component: Register,
  },
  {
    path: '/userInfo/:id',
    component: UserInfo,
    meta: { requiresAuth: true },
  },
  {
    path: '/edit/:id',
    component: Post,
    meta: { requiresAuth: true },
  },
  {
    path: '/post',
    component: Post,
    meta: { requiresAuth: true },
  },
  {
    path: '/admin',
    component: Admin,
  },
];

const router = createRouter({
  history: createWebHistory(), // history mode
  routes,
});

router.beforeEach((to) => {
  const [isLogin] = useLoginState();

  if (to.meta.requiresAuth && !isLogin.value) {
    return {
      path: '/login',
      query: { redirect: to.fullPath },
    };
  }
});

export { router };
