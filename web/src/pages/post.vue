<template>
  <a-layout class="style-full-screen">
    <a-layout-header class="style-layout-header">
      <a-row justify="space-between" align="middle">
        <a-space>
          <a-button
            @click="router.back()"
            shape="circle"
            class="icon-btn-center"
          >
            <template #icon>
              <font-awesome-icon icon="fa-solid fa-arrow-left" size="lg" />
            </template>
          </a-button>
          <div style="font-size: 16px">发表文章</div>
        </a-space>
      </a-row>
    </a-layout-header>

    <a-layout-content class="style-layout-contents">
      <!-- 富文本编辑器 -->
      <div v-if="loading" class="style-loading">
        <a-spin size="large"></a-spin>
      </div>
      <Editor :articleInfo="articleInfo" v-else />
    </a-layout-content>
  </a-layout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

// 发帖页面
export default defineComponent({
  name: 'post',
});
</script>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import Editor from '@components/editor/editor.vue';
import { useRoute, useRouter } from 'vue-router';
import { useArticle } from '@store';

const articleInfo = ref<ArticleDetail>();
const article = useArticle();

const loading = ref(true);

const route = useRoute();
const router = useRouter();

onMounted(() => {
  const id = route.params.id;

  if (id && route.path.indexOf('edit') !== -1) {
    article.getArticleDetail(route.params.id as string).then((res) => {
      articleInfo.value = res;
      loading.value = false;
    });
  } else {
    loading.value = false;
  }
});
</script>
