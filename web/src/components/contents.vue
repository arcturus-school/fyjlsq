<template>
  <div class="style-loading" v-if="loading">
    <a-spin size="large" />
  </div>

  <div class="style-failed" v-else-if="failed">
    <a-result status="error" title="获取失败" sub-title="请重新尝试">
      <template #extra>
        <a-button key="refresh" @click="obtainPageData"> 刷新 </a-button>
      </template>
    </a-result>
  </div>

  <contentList v-else :articles="articles"></contentList>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'contents',
});
</script>

<script setup lang="ts">
import { useArticle } from '@store';
import { onMounted, ref } from 'vue';
import contentList from '@components/contents_list.vue';

const article = useArticle();

const loading = ref(true);
const failed = ref(false);

const articles = ref<Article[]>([]);

const obtainPageData = function () {
  loading.value = true;
  failed.value = false;

  article
    .getArticle()
    .then((res) => {
      loading.value = false;
      articles.value = res;
    })
    .catch(() => {
      loading.value = false;
      failed.value = true;
    });
};

onMounted(() => {
  // 进入首页时自动加载文章页
  obtainPageData();
});
</script>
