<template>
  <a-layout class="style-full-screen">
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

    <a-layout-content class="style-contents">
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

      <a-result
        status="403"
        title="403"
        sub-title="没有权限哦~"
        v-else-if="!hasPermission"
      >
      </a-result>

      <a-table v-else :dataSource="dataSources" :columns="columns">
        <template v-slot:bodyCell="{ column, record, index }">
          <!-- 用户名 -->
          <template v-if="column.dataIndex === 'name'">
            {{ record.name }}
          </template>
          <!-- 账号 -->
          <template v-if="column.dataIndex === 'account'">
            {{ record.account }}
          </template>
          <!-- uid -->
          <template v-if="column.dataIndex === 'uid'">
            {{ record.uid }}
          </template>
          <!-- 操作 -->
          <template v-if="column.dataIndex === 'operation'">
            <a-popconfirm
              v-if="dataSources.length"
              title="确定嘛?"
              ok-text="确定"
              cancel-text="取消"
              @confirm="onSetManager(record, index)"
            >
              <a>
                {{ record.isManager ? '取消管理员' : '设为管理员' }}
              </a>
            </a-popconfirm>
          </template>
        </template>
      </a-table>
    </a-layout-content>
  </a-layout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'admin',
});
</script>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useAccountStore } from '@store';
import { useRouter } from 'vue-router';

const user = useAccountStore();

const router = useRouter();

interface TableItem {
  key: number;
  name: string;
  uid: number;
  account: string;
  roles: string[];
  isManager: boolean;
}

const dataSources = ref<TableItem[]>([]);

const loading = ref(true);
const failed = ref(false);
const hasPermission = ref(false);

const columns = ref([
  {
    title: '用户名',
    dataIndex: 'name',
  },
  {
    title: '账号',
    dataIndex: 'account',
  },
  {
    title: 'uid',
    dataIndex: 'uid',
  },
  {
    title: '操作',
    dataIndex: 'operation',
  },
]);

const obtainPageData = function () {
  user
    .getUserList()
    .then((res) => {
      loading.value = false;
      hasPermission.value = true;

      dataSources.value = res.users.map((e, i) => ({
        key: i,
        name: `用户 ${i}`,
        uid: e.uid,
        account: e.email,
        roles: e.roles!,
        isManager: e.roles!.includes('manager'),
      }));
    })
    .catch((err) => {
      loading.value = false;

      if (err.code === 403) {
        hasPermission.value = false;
      } else {
        failed.value = true;
      }
    });
};

onMounted(() => {
  // 获取用户列表
  obtainPageData();
});

function onSetManager(u: TableItem, idx: number) {
  let type;

  if (u.isManager) {
    // 当前用户是管理员, 则取消管理员
    type = 'remove';
  } else {
    type = 'appoint';
  }

  user.setManager(u.uid, type).then((res) => {
    if (res) {
      dataSources.value[idx].isManager = !dataSources.value[idx].isManager;
    }
  });
}
</script>

<style scoped>
.style-contents {
  padding: 20px 50px;
  margin-top: 60px;
}
</style>
