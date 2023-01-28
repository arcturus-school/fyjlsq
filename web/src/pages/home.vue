<template>
  <a-layout class="style-full-screen">
    <a-layout-header class="style-layout-header">
      <a-row justify="space-between">
        <a-col>
          <!-- 导航栏 -->
          <a-menu
            v-model:selectedKeys="selectedKeys"
            mode="horizontal"
            @click="({ key }) => router.push(key)"
            :style="{
              lineHeight: '64px',
              borderBottom: 'None',
            }"
          >
            <a-menu-item
              v-for="item of navbars"
              :key="item.key"
            >
              {{ item.name }}
            </a-menu-item>
          </a-menu>
        </a-col>

        <a-space>
          <!-- 发帖按钮 -->
          <a-button
            type="primary"
            shape="circle"
            size="32px"
            v-if="isLogin"
            href="/post"
          >
            <template #icon>
              <plus-outlined />
            </template>
          </a-button>
          <Avatar></Avatar>
        </a-space>
      </a-row>
    </a-layout-header>

    <a-layout-content class="style-layout-contents">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </a-layout-content>
  </a-layout>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'home',
});
</script>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAccountStore } from '@/store';
import { useLoginState } from '@utils/hooks';
import Avatar from '@components/avatar.vue';

const router = useRouter();
const route = useRoute();
const user = useAccountStore();

const navbars = ref([
  {
    key: '/contents',
    name: '首页',
  },
]);

const isLogin = computed(() => useLoginState()[0].value);

const selectedKeys = ref([navbars.value[0].key]);

onMounted(() => {
  if (route.params.id !== undefined) {
    router.push(`/article-detail/${route.params.id}`);
  } else {
    router.push(navbars.value[0].key);
  }

  user.userInfo();
});
</script>

<style scoped></style>
