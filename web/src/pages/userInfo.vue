<template>
  <a-layout class="style-full-screen">
    <a-layout-content class="style-layout-user-info-contents">
      <a-button
        shape="circle"
        size="large"
        @click="router.back()"
        class="style-back-btn"
      >
        <template #icon>
          <font-awesome-icon icon="fa-solid fa-arrow-left" size="lg" />
        </template>
      </a-button>

      <div class="style-loading" v-if="loading">
        <a-spin size="large" />
      </div>

      <div v-else-if="failed" class="style-failed">
        <a-result status="error" title="获取失败" sub-title="请重新尝试">
          <template #extra>
            <a-button key="back" type="primary" href="/"> 返回首页 </a-button>
            <a-button key="refresh" @click="obtainPageData">
              重新尝试
            </a-button>
          </template>
        </a-result>
      </div>

      <div v-else>
        <a-row
          align="middle"
          justify="center"
          class="style-user-info-container"
        >
          <a-space direction="vertical" size="large" align="center">
            <a-avatar
              :src="userInfo!.avatar"
              class="style-user-avatar"
            ></a-avatar>

            <h1 class="style-user-name">
              {{ userInfo!.user_name }}
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
      </div>
    </a-layout-content>
  </a-layout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'userInfo',
});
</script>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useAccountStore, useArticle } from '@store';
import { useRoute, useRouter } from 'vue-router';
import contentList from '@components/contents_list.vue';

const user = useAccountStore();
const article = useArticle();
const route = useRoute();
const router = useRouter();

const userInfo = ref<UserInfo>();
const loading = ref(true);
const failed = ref(false);

const articles = ref<Article[]>([]);

const activeKey = ref('1');

const obtainPageData = function () {
  loading.value = true;
  failed.value = false;

  user
    .getUserInfoByUid(route.params.id as string)
    .then((user) => {
      userInfo.value = user;

      article.getOnesArticles(user.uid).then((res) => {
        loading.value = false;

        articles.value = res.articles.map((e) => {
          const res: Article = e as Article;

          res.user = user;

          return res;
        });
      });
    })
    .catch(() => {
      loading.value = false;
      failed.value = true;
    });
};

onMounted(() => {
  obtainPageData();
});
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

:deep(.style-contents-container .ant-tabs-nav .ant-tabs-nav-wrap) {
  flex: none;
}
</style>
