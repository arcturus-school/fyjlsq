<template>
  <a-layout class="style-full-screen">
    <a-layout-header class="style-layout-header">
      <a-row justify="space-between" align="middle">
        <a-space>
          <a-button @click="router.back()" shape="circle">
            <template #icon>
              <arrow-left-outlined />
            </template>
          </a-button>
          <div style="font-size: 16px">发表文章</div>
        </a-space>

        <a-avatar
          class="style-clickable"
          @click="router.push('/userInfo')"
          :size="32"
          :src="user.avatar"
        >
          <template #icon>
            <user-outlined />
          </template>
        </a-avatar>
      </a-row>
    </a-layout-header>

    <a-layout-content class="style-layout-contents">
      <!-- 富文本编辑器 -->
      <Editor :articleInfo="articleInfo" v-if="loading" />
    </a-layout-content>
  </a-layout>
</template>

<script>
import { defineComponent } from 'vue';

// 发帖页面
export default defineComponent({
  name: 'post',
});
</script>

<script setup>
import { onMounted, ref } from 'vue';
import Editor from '@components/editor/editor.vue';
import { useRoute, useRouter } from 'vue-router';
import { useArticle, useAccountStore } from '@/store';

const articleInfo = ref(null);
const article = useArticle();
const user = useAccountStore();

const loading = ref(false);

const route = useRoute();
const router = useRouter();

onMounted(() => {
  const id = route.params.id;

  if (id && route.path.indexOf('edit') !== -1) {
    article
      .getArticleDetail(route.params.id)
      .then((res) => {
        articleInfo.value = res;
        loading.value = true;
      });
  } else {
    loading.value = true;
  }

  user.userInfo();
});
</script>
