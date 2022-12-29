import { defineStore } from 'pinia';
import { message } from 'ant-design-vue';
import Http from '@utils/axios';
import {
  useLoginState,
  useUid,
  useToken,
} from '@utils/hooks';

import { SERVER_URL } from '@/config';

const _ = new Http(SERVER_URL);

const [, setUid] = useUid();
const [, setToken] = useToken();
const [, setLoginState] = useLoginState();

function setUserInfo(obj, info) {
  obj.roles = info.roles;
  obj.avatar = info.avatar;
  obj.email = info.email;
  obj.userName = info.user_name;
}

export const useAccountStore = defineStore('account', {
  state: () => ({
    roles: [],
    userName: '',
    avatar: '',
    email: '',
  }),
  getters: {
    isManager: (state) => state.roles.includes('manager'),
    isSuperUser: (state) => state.roles.includes('super'),
  },
  actions: {
    // 获取用户列表
    getUserList() {
      return _.request({
        url: '/auth/users',
        method: 'GET',
      }).catch(() => {});
    },

    // 退出登录
    logout() {
      setUid(null);
      setLoginState(false);

      this.$reset();
    },

    // 根据 uid 获取信息
    getUserInfoByUid(uid) {
      return _.request({
        url: '/auth/user_info',
        method: 'GET',
        data: {
          uid,
        },
      })
        .then((res) => {
          return res.userInfo;
        })
        .catch((err) => {
          message.error(err);
        });
    },

    // 获取个人信息
    userInfo() {
      const [uid] = useUid();
      const [isLogin] = useLoginState();

      if (isLogin && uid !== null) {
        return _.request({
          url: '/auth/user_info',
          method: 'GET',
          data: {
            uid,
          },
        })
          .then((res) => {
            setUserInfo(this, res.userInfo);
            setUid(res.userInfo.uid);
          })
          .catch((err) => {
            message.error(err);
          });
      }
    },

    // 登录请求
    login({ email, password }) {
      return _.request({
        url: '/auth/login',
        method: 'POST',
        data: {
          email,
          password,
        },
      })
        .then((res) => {
          setToken(res.token);
          setUid(res.userInfo.uid);
          setLoginState(true);
          setUserInfo(this, res.userInfo);

          message.success(res.msg);

          return true; // 登录成功
        })
        .catch((err) => {
          message.error(err);
        });
    },

    // 注册
    register({ email, password }) {
      return _.request({
        url: '/auth/register',
        method: 'POST',
        data: {
          email,
          password,
        },
      })
        .then((res) => {
          setToken(res.token);
          setUid(res.userInfo.uid);
          setLoginState(true);

          setUserInfo(this, res.userInfo);

          message.success(res.msg);

          return true; // 注册成功
        })
        .catch((err) => {
          message.error(err);
        });
    },

    setManager(uid, type) {
      return _.request({
        url: '/auth/manager',
        method: 'POST',
        data: {
          uid,
          type,
        },
      })
        .then((res) => {
          message.success(res.msg);

          return true;
        })
        .catch((err) => {
          message.error(err);
        });
    },
  },
});

export const useArticle = defineStore('article', {
  actions: {
    // 发帖
    post(data) {
      return _.request({
        url: '/article/post',
        method: 'POST',
        data,
      })
        .then((res) => {
          message.success(res.msg);

          return res.id;
        })
        .catch((err) => {
          message.error(err);
        });
    },

    // 编辑帖子
    edit(data) {
      return _.request({
        url: '/article/edit',
        method: 'POST',
        data,
      })
        .then((res) => {
          message.success(res.msg);
          return true;
        })
        .catch((err) => {
          message.error(err);
        });
    },

    // 获取首页文章
    getArticle() {
      return _.request({
        url: '/article/list',
        method: 'GET',
      })
        .then((res) => {
          message.success(res.msg);
          return res.articles;
        })
        .catch((err) => {
          message.error(err);
        });
    },

    // 获取文章详情
    getArticleDetail(id) {
      return _.request({
        url: `/article/${id}`,
        method: 'GET',
      })
        .then((res) => {
          return res.article;
        })
        .catch((err) => {
          message.error(err);
        });
    },

    // 删除文章
    removeArticle(id) {
      return _.request({
        url: '/article/delete',
        method: 'POST',
        data: {
          id,
        },
      })
        .then((res) => {
          message.success(res.msg);
          return true;
        })
        .catch((err) => {
          message.error(err);
        });
    },

    // 获取某个人的文章
    getOnesArticles(uid) {
      return _.request({
        url: 'article/user/list',
        method: 'GET',
        data: {
          uid,
        },
      })
        .then((res) => {
          return res;
        })
        .catch((err) => {
          message.error(err);
        });
    },
  },
});
