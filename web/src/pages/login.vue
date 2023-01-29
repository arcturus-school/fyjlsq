<template>
  <a-row justify="center" align="middle" class="style-full-screen">
    <a-button type="link" href="/" class="style-back-btn"> 返回首页 </a-button>

    <a-form :model="formState" class="style-login-form" @finish="onFinish">
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
            <font-awesome-icon icon="fa-solid fa-user" class="form-icon" />
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
        <a-input-password v-model:value="formState.password">
          <template #prefix>
            <font-awesome-icon icon="fa-solid fa-lock" class="form-icon" />
          </template>
        </a-input-password>
      </a-form-item>

      <a-form-item>
        <a class="style-login-form-forgot" href=""> 忘记密码? </a>
      </a-form-item>

      <a-form-item>
        <a-button
          type="primary"
          html-type="submit"
          class="style-login-form-btn"
        >
          登录
        </a-button>

        <router-link :to="addr" class="style-register-btn">
          没有账号? 立即注册
        </router-link>
      </a-form-item>
    </a-form>
  </a-row>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'login',
});
</script>

<script setup lang="ts">
import { computed, reactive } from 'vue';
import { useAccountStore } from '@store';
import { LocationQueryValue, useRouter } from 'vue-router';

const formState = reactive<Login>({
  email: '',
  password: '',
});

const user = useAccountStore();
const router = useRouter();

const addr = computed(() => {
  const redirect = router.currentRoute.value.query.redirect;

  if (typeof redirect !== 'undefined') {
    return {
      path: '/register',
      query: {
        redirect: redirect,
      },
    };
  }

  return { path: '/register' };
});

// 成功提交
function onFinish(values: Login) {
  user.login(values).then((res) => {
    if (res) {
      const redirect = router.currentRoute.value.query
        .redirect as LocationQueryValue;

      // 返回重定向地址
      router.push({ path: redirect ?? '/' });
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

.style-login-form {
  max-width: 300px;
}

.style-login-form-forgot {
  float: right;
}

.style-login-form-btn {
  width: 100%;
}

.style-register-btn {
  width: 100%;
  display: inline-block;
  text-align: center;
  margin-top: 12px;
}

.form-icon {
  color: rgba(0, 0, 0, 0.45);
}
</style>
