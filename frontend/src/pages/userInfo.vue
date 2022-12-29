<template>
  <a-layout class="style-full-screen">
    <a-layout-content
      class="style-layout-user-info-contents"
    >
      <a-button
        shape="circle"
        size="large"
        @click="router.back()"
        class="style-back-btn"
      >
        <template #icon>
          <font-awesome-icon
            icon="fa-solid fa-arrow-left"
            size="lg"
          />
        </template>
      </a-button>
      <a-row
        align="middle"
        justify="center"
        class="style-user-info-container"
      >
        <a-space
          direction="vertical"
          size="large"
          align="center"
        >
          <a-avatar
            :src="userInfo.avatar"
            class="style-user-avatar"
          ></a-avatar>

          <h1 class="style-user-name">
            {{ userInfo.user_name }}
          </h1>
        </a-space>
      </a-row>

      <div class="style-contents-container">
        <a-tabs v-model:activeKey="activeKey">
          <a-tab-pane key="1" tab="文章">
            <contentList :articles="articles"></contentList>
          </a-tab-pane>
        </a-tabs>
      </div>
    </a-layout-content>
  </a-layout>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'userInfo',
});
</script>

<script setup>
import { onMounted, ref } from 'vue';
import { useAccountStore, useArticle } from '@/store';
import { useRoute, useRouter } from 'vue-router';
import contentList from '@components/contents_list.vue';

const user = useAccountStore();
const article = useArticle();
const route = useRoute();
const router = useRouter();

const userInfo = ref({});
const articles = ref([]);

const activeKey = ref('1');

onMounted(() => {
  user.getUserInfoByUid(route.params.id).then((user) => {
    userInfo.value = user;

    article.getOnesArticles(user.uid).then((res) => {
      articles.value = res.articles.map((e) => {
        e.user = user;

        return e;
      });
    });
  });
});

// TODO: 触底刷新
</script>

<style scoped>
.style-user-info-container {
  margin: 80px 0 20px;
}

.style-user-avatar {
  width: 100px;
  height: 100px;
  box-shadow: 0 0 10px #e6e6e6;
}

.style-user-name {
  font-size: 40px;
  margin: 0;
}

.style-contents-container {
  padding: 0 30px;
}

.style-layout-user-info-contents {
  background-color: #fff;
  overflow-x: hidden;
  overflow-y: scroll;
}

:deep(.style-contents-container .ant-tabs-nav) {
  justify-content: center;
}

:deep(.style-contents-container
    .ant-tabs-nav
    .ant-tabs-nav-wrap) {
  flex: none;
}
</style>
