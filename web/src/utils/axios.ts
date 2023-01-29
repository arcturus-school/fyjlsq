import axios, { AxiosError, AxiosInstance, Method } from 'axios';
import { useLoginState, useToken, useUid } from '@utils/hooks';
import { message } from 'ant-design-vue';
import { log } from '@utils/log';

interface Configs {
  timeout?: number;
  headers?: Record<string, any>;
}

interface RequestOptions {
  url: string;
  method?: Method;
  data?: {
    params?: Record<string, any>;
    data?: Record<string, any>;
  };
}

export default class Http {
  ax: AxiosInstance;

  constructor(
    baseUrl: string,
    {
      timeout = 20000,
      headers = {
        'Content-Type': 'application/json',
      },
    }: Configs = {}
  ) {
    this.ax = axios.create({
      timeout: timeout,
      baseURL: baseUrl,
      headers,
    });

    this.ax.interceptors.request.use((config) => {
      if (useLoginState()[0].value) {
        const [token] = useToken();
        config.headers.Authorization = `Bearer ${token}`;
      }

      return config;
    });

    this.ax.interceptors.response.use(
      (resp) => {
        log(resp.data);

        if (resp.data.code == 200) {
          return resp.data;
        }

        if (resp.data.code === 801) {
          // account is not exist
          const [, setUid] = useUid();
          const [, setToken] = useToken();

          setUid(null);
          setToken(null);
        }

        message.error(resp.data.msg);

        return Promise.reject({
          code: resp.data.code,
          msg: resp.data.msg,
        });
      },
      (err: AxiosError) => {
        log(err);

        message.error(err.message);

        // 非 2xx 错误请求
        return Promise.reject({
          code: err.response?.status,
          msg: err.message,
        });
      }
    );
  }

  request({ url, method = 'GET', data = {} }: RequestOptions): Promise<any> {
    return this.ax({ url, method, ...data });
  }
}
