<template>
  <contentList :articles="articles"></contentList>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'contents',
});
</script>

<script setup>
import { useArticle } from '@/store';
import { onMounted, ref } from 'vue';
import contentList from '@components/contents_list.vue';

const article = useArticle();

const articles = ref([]);

onMounted(() => {
  // 进入首页时自动加载文章页
  article.getArticle().then((res) => {
    articles.value = res;
  });
});
</script>
