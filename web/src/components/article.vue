<template>
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

  <div class="style-contents-container" v-if="!loading">
    <a-row>
      <a-col span="12">
        <a-image :src="articleInfo.cover" height="300px" />
      </a-col>

      <a-col span="12" class="style-article-info">
        <a-space>
          <a-button
            shape="circle"
            size="large"
            @click="share"
          >
            <template #icon>
              <font-awesome-icon
                icon="fa-solid fa-share-nodes"
                size="lg"
              />
            </template>
          </a-button>

          <a-button
            shape="circle"
            size="large"
            @click="removeArticle(articleInfo.id)"
            v-if="displayRemoveButton"
          >
            <template #icon>
              <font-awesome-icon
                icon="fa-solid fa-trash"
                size="lg"
              />
            </template>
          </a-button>

          <a-button
            shape="circle"
            size="large"
            @click="editArticle(articleInfo.id)"
            v-if="displayEditButton"
          >
            <template #icon>
              <font-awesome-icon
                icon="fa-solid fa-pen-to-square"
                size="lg"
              />
            </template>
          </a-button>
        </a-space>

        <a-space direction="vertical" style="display: flex">
          <h1 class="style-title">
            # {{ articleInfo.title }}
          </h1>

          <div>
            全文共 {{ articleInfo.character_count }} 字
          </div>
        </a-space>

        <a-row align="middle" style="margin-bottom: 10px">
          <a-space size="middle">
            <a-avatar
              style="cursor: pointer"
              :size="80"
              :src="articleInfo.user.avatar"
              @click="
                router.push(
                  `/userInfo/${articleInfo.user.uid}`
                )
              "
            >
              <template #icon>
                <user-outlined />
              </template>
            </a-avatar>
            <a-space direction="vertical">
              <div class="style-user-name">
                {{ articleInfo.user.user_name }}
              </div>
              <div>
                更新于
                {{ formatTime(articleInfo.update_at) }}
              </div>
            </a-space>
          </a-space>
        </a-row>
      </a-col>
    </a-row>

    <div
      class="style-content-body"
      v-html="articleInfo.content"
    ></div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'article-detail',
});
</script>

<script setup>
import {
  ref,
  onMounted,
  createVNode,
  computed,
  watchEffect,
} from 'vue';
import { useArticle, useAccountStore } from '@/store';
import { useRoute, useRouter } from 'vue-router';
import { useUid } from '@utils/hooks';
import { formatTime } from '@utils/handle';
import { message } from 'ant-design-vue';
import { useClipboard } from '@vueuse/core';
import { ExclamationCircleOutlined } from '@ant-design/icons-vue';
import { Modal } from 'ant-design-vue';

const article = useArticle();
const user = useAccountStore();
const route = useRoute();
const router = useRouter();

const articleInfo = ref({});
const loading = ref(true);

const displayRemoveButton = computed(() => {
  return (
    useUid()[0] === articleInfo.value.user.uid ||
    user.isManager ||
    user.isSuperUser
  );
});

// TODO: 支持管理员/超级管理员编辑用户帖子
const displayEditButton = computed(() => {
  return useUid()[0] == articleInfo.value.user.uid;
});

onMounted(() => {
  const id = route.params.id;

  article.getArticleDetail(id).then((res) => {
    if (res) {
      articleInfo.value = res;
      loading.value = false;
    }
  });
});

watchEffect(
  () => {
    const id = route.params.id;

    if (typeof id !== 'undefined') {
      loading.value = true;

      article.getArticleDetail(id).then((res) => {
        if (res) {
          articleInfo.value = res;
          loading.value = false;
        }
      });
    }
  },
  () => route.params.id
);

// 删除文章
function removeArticle(id) {
  return Modal.confirm({
    title: () => '确定删除吗?',
    icon: () => createVNode(ExclamationCircleOutlined),
    okText: () => '确定',
    okType: 'danger',
    cancelText: () => '按错了',
    onOk() {
      article.removeArticle(id).then((res) => {
        if (res) {
          router.push('contents');
        }
      });
    },
  });
}

// 编辑文章
function editArticle(id) {
  router.push(`/edit/${id}`);
}

const { copy } = useClipboard();

// 分享
function share() {
  copy(window.location.href);
  message.success('复制链接成功');
}
</script>

<style scoped>
.style-contents-container {
  margin: 20px 100px;
  padding: 24px;
  border-radius: 20px;
  background-color: white;
}

.style-title {
  font-size: 60px;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}

.style-user-name {
  font-size: 32px;
}

.style-article-info {
  padding-left: 30px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.style-content-body {
  margin: 30px 0;
}

:deep(.style-content-body img) {
  width: 100%;
}

:deep(.ant-image) {
  border-radius: 24px;
  width: 100%;
  overflow: hidden;
}

:deep(.ant-image img) {
  background-size: cover;
  object-fit: cover;
}

h1 {
  margin: 0;
}
</style>
