import { defineStore } from 'pinia';
import { message } from 'ant-design-vue';
import { useLoginState, useUid, useToken } from '@utils/hooks';
import Http from '@utils/axios';

const req = new Http(import.meta.env.VITE_SERVER_URL);

const [, setUid] = useUid();
const [, setToken] = useToken();
const [, setLoginState] = useLoginState();

interface AccountState {
  roles: string[];
  username: string;
  avatar: string;
  email: string;
}

export const useAccountStore = defineStore('account', {
  state: (): AccountState => ({
    roles: [],
    username: '',
    avatar: '',
    email: '',
  }),
  getters: {
    isManager: (state) => state.roles.includes('manager'),
    isSuperUser: (state) => true /*state.roles.includes('super')*/,
  },
  actions: {
    // 获取用户列表
    async getUserList(): Promise<UserListRes> {
      return await req.request({
        url: '/auth/users',
        method: 'GET',
      });
    },

    // 退出登录
    logout() {
      setUid(null);
      setLoginState(false);
      this.$reset();
    },

    // 根据 uid 获取信息
    getUserInfoByUid(uid: string) {
      return req
        .request({
          url: '/auth/user_info',
          method: 'GET',
          data: { params: { uid } },
        })
        .then((res: UserInfoRes) => {
          return res.userInfo;
        });
    },

    // 获取个人信息
    userInfo() {
      const [uid] = useUid();
      const [isLogin] = useLoginState();

      if (isLogin && uid !== null) {
        req
          .request({
            url: '/auth/user_info',
            method: 'GET',
            data: { params: { uid } },
          })
          .then((res: UserInfoRes) => {
            this.updateUserInfo(res.userInfo);
            setUid(res.userInfo.uid);
          })
          .catch(() => {});
      }
    },

    updateUserInfo(info: UserInfo) {
      this.roles = info.roles;
      this.avatar = info.avatar;
      this.email = info.email;
      this.username = info.user_name;
    },

    // 登录
    login({ email, password }: Login) {
      return req
        .request({
          url: '/auth/login',
          method: 'POST',
          data: { data: { email, password } },
        })
        .then((res: LoginRes) => {
          setToken(res.token);
          setUid(res.userInfo.uid);
          setLoginState(true);

          this.updateUserInfo(res.userInfo);

          message.success(res.msg);

          return true;
        });
    },

    // 注册
    register({ email, password }: Register) {
      return req
        .request({
          url: '/auth/register',
          method: 'POST',
          data: { data: { email, password } },
        })
        .then((res: RegisterRes) => {
          setToken(res.token);
          setUid(res.userInfo.uid);
          setLoginState(true);

          this.updateUserInfo(res.userInfo);

          message.success(res.msg);

          return true;
        });
    },

    setManager(uid: number, type: string) {
      return req
        .request({
          url: '/auth/manager',
          method: 'POST',
          data: { data: { uid, type } },
        })
        .then((res: Res) => {
          message.success(res.msg);
          return true;
        });
    },
  },
});

export const useArticle = defineStore('article', {
  actions: {
    // 发帖
    post(data: PostData) {
      return req
        .request({
          url: '/article/post',
          method: 'POST',
          data: { data },
        })
        .then((res: PostRes) => {
          message.success(res.msg);
          return res.id;
        })
        .catch(() => {
          return false;
        });
    },

    // 编辑帖子
    edit(data: PostData) {
      return req
        .request({
          url: '/article/edit',
          method: 'POST',
          data: { data },
        })
        .then((res: Res) => {
          message.success(res.msg);
          return true;
        })
        .catch(() => {
          return false;
        });
    },

    // 获取首页文章
    getArticle() {
      return req
        .request({
          url: '/article/list',
          method: 'GET',
        })
        .then((res: ArticlesRes) => {
          message.success(res.msg);
          return res.articles;
        });
    },

    // 获取文章详情
    getArticleDetail(id: string) {
      return req
        .request({
          url: `/article/${id}`,
          method: 'GET',
        })
        .then((res: ArticleDetailRes) => {
          return res.article;
        });
    },

    // 删除文章
    removeArticle(id: string) {
      return req
        .request({
          url: '/article/delete',
          method: 'POST',
          data: { data: { id } },
        })
        .then((res: Res) => {
          message.success(res.msg);
          return true;
        });
    },

    // 获取某个人的文章
    getOnesArticles(uid: number, page: number = 1) {
      return req
        .request({
          url: 'article/user/list',
          method: 'GET',
          data: { data: { uid, page } },
        })
        .then((res: PersonArticles) => {
          return res;
        });
    },
  },
});
