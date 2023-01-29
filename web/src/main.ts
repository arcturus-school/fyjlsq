import { createApp } from 'vue';
import { createPinia } from 'pinia';
import Icons from '@utils/icons';
import { router } from '@router';
import App from '@src/App.vue';

import 'ant-design-vue/dist/antd.css';
import '@src/style.css';

const app = createApp(App);

app.use(router);
app.use(Icons);
app.use(createPinia());

app.mount('#app');
