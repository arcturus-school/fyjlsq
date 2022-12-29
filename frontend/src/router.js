import { createRouter, createWebHistory } from 'vue-router';
import { useLoginState } from '@utils/hooks';

// 自定义组件(页面)
import Home from '@pages/home.vue';
import Login from '@pages/login.vue';
import Register from '@pages/register.vue';
import UserInfo from '@pages/userInfo.vue';
import Post from '@pages/post.vue';
import Admin from '@pages/admin.vue';
// 子页面
import Content from '@components/contents.vue';
import ArticleDetail from '@components/article.vue';

const routes = [
  {
    path: '/',
    component: Home,
    alias: ['/home'],
    children: [
      {
        path: '/contents',
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
  history: createWebHistory(), // history 模式
  routes,
});

// 路由守卫
router.beforeEach((to) => {
  const [isLogin] = useLoginState();

  if (to.meta.requiresAuth && !isLogin.value) {
    // 检查是否已登录, 如果没有, 则重定向到登录页面
    return {
      path: '/login',
      // 保存我们所在的位置, 以便成功后返回
      query: { redirect: to.fullPath },
    };
  }
});

export { router };
