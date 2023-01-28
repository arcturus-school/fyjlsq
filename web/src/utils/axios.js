import axios from 'axios';
import { useLoginState } from '@utils/hooks';

export default class Http {
  constructor(baseUrl, { timeout, headers } = {}) {
    // 默认 post 请求体为 json 格式
    if (typeof headers === 'undefined') {
      headers = { 'Content-Type': 'application/json' };
    }

    this.ax = axios.create({
      timeout: timeout ?? 20000,
      baseURL: baseUrl,
      headers,
    });

    // 请求拦截器
    this.ax.interceptors.request.use((config) => {
      if (useLoginState()[0].value) {
        // 只要登录过, 请求就带上 token
        const token = localStorage.getItem('token');
        config.headers.Authorization = `Bearer ${token}`;
      }

      return config;
    });

    // 响应拦截器
    this.ax.interceptors.response.use(
      (resp) => {
        // 请求正确, 返回结果
        if (resp.data.code == 200) return resp.data;

        // 请求错误, 抛出错误
        // 例如 resp.data = {
        //   "msg": "密码错误",
        //   "code": "800",
        // }
        return Promise.reject(resp.data.msg);
      },
      (err) => {
        // 非 2xx 错误请求
        return Promise.reject(err.message);
      }
    );
  }

  request({ url, method = 'GET', data }) {
    const p = {};

    if (data) {
      if (method === 'GET') {
        p.params = data;
      } else if (method === 'POST') {
        p.data = data;
      }
    }

    return this.ax({
      url,
      method,
      ...p,
    });
  }
}
