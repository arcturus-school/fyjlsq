<template>
  <a-layout class="style-full-screen">
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

    <a-layout-content class="style-contents">
      <a-result
        status="403"
        title="403"
        sub-title="没有权限哦~"
        v-if="!hasPermission"
      >
      </a-result>
      <a-table
        v-else
        :dataSource="dataSource"
        :columns="columns"
      >
        <template
          v-slot:bodyCell="{ column, record, index }"
        >
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
              v-if="dataSource.length"
              title="确定嘛?"
              ok-text="确定"
              cancel-text="取消"
              @confirm="onSetManager(record, index)"
            >
              <a>
                {{
                  record.isManager
                    ? '取消管理员'
                    : '设为管理员'
                }}
              </a>
            </a-popconfirm>
          </template>
        </template>
      </a-table>
    </a-layout-content>
  </a-layout>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'admin',
});
</script>

<script setup>
import { onMounted, ref } from 'vue';
import { useAccountStore } from '@/store';
import { useRouter } from 'vue-router';

const user = useAccountStore();
const hasPermission = ref(false);
const router = useRouter();

const dataSource = ref([]);

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

onMounted(() => {
  // 获取用户列表
  user.getUserList().then((res) => {
    hasPermission.value = true;

    dataSource.value = res.users.map((e, i) => ({
      key: i,
      name: `用户 ${i}`,
      uid: e.uid,
      account: e.account,
      roles: e.roles,
      isManager: e.roles.includes('manager'),
    }));
  });
});

function onSetManager(user, idx) {
  let type;

  if (user.isManager) {
    // 当前用户是管理员, 则取消管理员
    type = 'remove';
  } else {
    type = 'appoint';
  }

  user.setManager(user.uid, type).then((res) => {
    if (res) {
      dataSource.value[idx].isManager =
        !dataSource.value[idx].isManager;
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
