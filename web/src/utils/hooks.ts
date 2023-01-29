import { Ref, ref } from 'vue';

type Token = [string | null, (t: string) => void];

export function useToken(): Token {
  const token = localStorage.getItem('token');

  function setToken(t: string) {
    localStorage.setItem('token', t);
  }

  return [token, setToken];
}

let isLogin: Ref<boolean> | null = null;

type LoginState = [Ref<boolean>, (s: boolean) => void];

export function useLoginState(): LoginState {
  let [token] = useToken();

  isLogin = isLogin === null ? (token ? ref(true) : ref(false)) : isLogin;

  function setLoginState(state: boolean) {
    isLogin!.value = state;

    if (!state) {
      localStorage.removeItem('token');
    }
  }

  return [isLogin, setLoginState];
}

let uid: number | null = null;

type Uid = [number | null, (id: number | null) => void];

export function useUid(): Uid {
  uid = uid === null ? Number(localStorage.getItem('uid')) : uid;

  function setUid(id: number | null) {
    uid = id;

    if (id !== null) {
      localStorage.setItem('uid', String(id));
    } else {
      localStorage.removeItem('uid');
    }
  }

  return [uid, setUid];
}
