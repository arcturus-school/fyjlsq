<template>
  <a-row :gutter="[16, 16]" style="padding: 12px 20px">
    <a-col
      v-for="item of articles"
      :key="item.id"
      :span="6"
    >
      <a-card
        hoverable
        @click="enter(item)"
        :bordered="false"
      >
        <!-- 封面图 -->
        <template #cover>
          <img
            class="style-cover"
            :alt="item.title"
            :src="item.cover"
          />
        </template>

        <a-card-meta
          :title="item.title"
          :description="item.abstract"
        >
          <!-- 用户头像 -->
          <template #avatar>
            <a-avatar :size="32" :src="item.user.avatar">
              <template #icon>
                <user-outlined />
              </template>
            </a-avatar>
          </template>
        </a-card-meta>
      </a-card>
    </a-col>
  </a-row>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'contents_list',
});
</script>

<script setup>
import { useRouter } from 'vue-router';
import { defineProps } from 'vue';

const router = useRouter();

const props = defineProps({
  articles: Array,
});

function enter(article) {
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
