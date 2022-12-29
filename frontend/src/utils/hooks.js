import { ref } from 'vue';

export function useToken() {
  const token = localStorage.getItem('token');

  function setToken(t) {
    localStorage.setItem('token', t);
  }

  return [token, setToken];
}

let isLogin = null;

export function useLoginState() {
  let [token] = useToken();

  isLogin =
    isLogin === null
      ? token
        ? ref(true)
        : ref(false)
      : isLogin;

  function setLoginState(state) {
    isLogin.value = state;

    if (!state) {
      localStorage.removeItem('token');
    }
  }

  return [isLogin, setLoginState];
}

let uid = null;

export function useUid() {
  uid = uid === null ? localStorage.getItem('uid') : uid;

  function setUid(id) {
    uid = id;

    if (id !== null) {
      localStorage.setItem('uid', id);
    } else {
      localStorage.removeItem('uid');
    }
  }

  return [uid, setUid];
}
