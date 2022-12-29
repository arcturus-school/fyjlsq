<template>
  <a-row
    justify="center"
    align="middle"
    class="style-full-screen"
  >
    <a-button
      type="link"
      href="/home"
      class="style-back-btn"
    >
      返回首页
    </a-button>

    <a-form
      class="style-register-form"
      :model="formState"
      @finish="onFinish"
    >
      <a-form-item
        label="邮箱"
        name="email"
        :rules="[
          {
            required: true,
            message: '请输入邮箱',
          },
        ]"
      >
        <a-input v-model:value="formState.email">
          <template #prefix>
            <user-outlined class="site-form-item-icon" />
          </template>
        </a-input>
      </a-form-item>

      <a-form-item
        label="密码"
        name="password"
        :rules="[
          {
            required: true,
            message: '请输入密码',
          },
        ]"
      >
        <a-input-password
          v-model:value="formState.password"
        >
          <template #prefix>
            <lock-outlined class="site-form-item-icon" />
          </template>
        </a-input-password>
      </a-form-item>

      <a-form-item>
        <a-button
          type="primary"
          html-type="submit"
          class="style-register-form-btn"
        >
          注册
        </a-button>

        <router-link :to="addr" class="style-register-btn">
          已有账号? 立即登录
        </router-link>
      </a-form-item>
    </a-form>
  </a-row>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'register',
});
</script>

<script setup>
import { reactive, computed } from 'vue';
import { useAccountStore } from '@/store';
import { useRouter } from 'vue-router';

const formState = reactive({
  email: '',
  password: '',
  remember: true,
});

const user = useAccountStore();
const router = useRouter();

const addr = computed(() => {
  const redirect = router.currentRoute.value.query.redirect;

  if (typeof redirect !== 'undefined') {
    return {
      path: '/login',
      query: {
        redirect: redirect,
      },
    };
  }

  return { path: '/login' };
});

// 成功提交
function onFinish(values) {
  user.register(values).then((res) => {
    if (res) {
      const redirect =
        router.currentRoute.value.query.redirect;

      // 返回重定向地址
      router.push({ path: redirect ?? '/home' });
    }
  });
}
</script>

<style scoped>
.style-back-btn {
  position: absolute;
  top: 10px;
  left: 10px;
}

.style-register-form {
  max-width: 300px;
}

.style-register-form-btn {
  margin-top: 12px;
  width: 100%;
}

.style-register-btn {
  width: 100%;
  display: inline-block;
  text-align: center;
  margin-top: 12px;
}
</style>
