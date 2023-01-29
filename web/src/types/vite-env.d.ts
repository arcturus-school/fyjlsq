/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue';
  const component: DefineComponent<{}, {}, any>;
  export default component;
}

interface ImportMetaEnv {
  readonly VITE_SERVER_URL: string;
  readonly VITE_IMAGE_UPLOAD_URL: string;
  readonly VITE_IMAGE_UPLOAD_TOKEN: string;
}
