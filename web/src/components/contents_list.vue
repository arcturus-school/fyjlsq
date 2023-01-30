<template>
  <a-row :gutter="[16, 16]" style="padding: 12px 20px">
    <a-col v-for="item of articles" :key="item.id" :xs="24" :sm="12" :md="6">
      <a-card hoverable @click="enter(item)" :bordered="false">
        <!-- 封面图 -->
        <template #cover>
          <img class="style-cover" :alt="item.title" :src="item.cover" />
        </template>

        <a-card-meta :title="item.title" :description="item.abstract">
          <!-- 用户头像 -->
          <template #avatar>
            <a-avatar :size="32" :src="item.user.avatar">
              <template #icon>
                <font-awesome-icon icon="fa-solid fa-user" />
              </template>
            </a-avatar>
          </template>
        </a-card-meta>
      </a-card>
    </a-col>
  </a-row>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'contents_list',
});
</script>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

defineProps<{ articles: Article[] }>();

function enter(article: Article) {
  router.push(`/article-detail/${article.id}`);
}
</script>

<style scoped>
.style-cover {
  height: 200px;
  object-fit: cover;
}

:deep(.ant-card-meta-description) {
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}
</style>
