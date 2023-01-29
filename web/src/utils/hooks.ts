import { Ref, ref } from 'vue';

type Token = [string | null, (t: string | null) => void];

export function useToken(): Token {
  const token = localStorage.getItem('token');

  function setToken(t: string | null) {
    if (t !== null) {
      localStorage.setItem('token', t);
    } else {
      localStorage.removeItem('token');
    }
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
  if (uid === null) {
    const u = localStorage.getItem('uid');

    if (u === null) {
      uid = null;
    } else {
      uid = Number(u);

      if (isNaN(uid)) {
        uid = null;
      }
    }
  }

  function setUid(id: number | null) {
    if (id !== null) {
      localStorage.setItem('uid', String(id));
      uid = id;
    } else {
      localStorage.removeItem('uid');
      uid = null;
    }
  }

  return [uid, setUid];
}
