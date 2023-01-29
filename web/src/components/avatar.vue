<template>
  <a-row>
    <a-dropdown placement="bottomRight" @click="clickAvatar">
      <!-- 头像 -->
      <a-avatar :src="user.avatar" :size="32" style="cursor: pointer">
        <template #icon>
          <font-awesome-icon icon="fa-solid fa-user" />
        </template>
      </a-avatar>

      <template #overlay>
        <a-menu @click="clickMenu" v-if="isLogin">
          <a-menu-item key="person"> 个人中心 </a-menu-item>
          <a-menu-item key="admin" v-if="user.isSuperUser">
            后台管理
          </a-menu-item>
          <a-menu-item key="logout"> 退出 </a-menu-item>
        </a-menu>
      </template>
    </a-dropdown>
  </a-row>
</template>

<script lang="ts">
import { VNodeChild, computed, defineComponent } from 'vue';

export default defineComponent({
  name: 'avatar',
});
</script>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useAccountStore } from '@store';
import { useLoginState, useUid } from '@utils/hooks';

interface MenuInfo {
  key: string;
  keyPath: string[];
  item: VNodeChild;
  domEvent: MouseEvent;
}

const router = useRouter();
const user = useAccountStore();

const isLogin = computed(() => useLoginState()[0].value);

function clickMenu({ key }: MenuInfo) {
  if (key === 'person') {
    router.push(`/userInfo/${useUid()[0]}`);
  } else if (key === 'admin') {
    router.push('/admin');
  } else if (key === 'logout') {
    user.logout();
  }
}

function clickAvatar() {
  if (!isLogin.value) {
    router.push('/login');
  }
}
</script>
