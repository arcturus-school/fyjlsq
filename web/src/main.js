import { createApp } from 'vue';
import Antd from 'ant-design-vue';
import { createPinia } from 'pinia';

import { router } from '@/router';
import AntDesignIcons from '@/utils/icons';
import App from '@/App.vue';

import 'ant-design-vue/dist/antd.css'; // ant-design 样式
import '@/style.css'; // 全局样式

const app = createApp(App);

// 注册插件
app
  .use(Antd)
  .use(router)
  .use(createPinia())
  .use(AntDesignIcons);

// 挂载元素
app.mount('#app');
