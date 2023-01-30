## 本地开发

```bash
pnpm install
```

```bash
pnpm run dev
```

新建 `.env` 文件, 填上服务端地址和图床 token

```
VITE_IMAGE_UPLOAD_TOKEN=xxx # https://imgloc.com/

VITE_SERVER_URL=http://127.0.0.1/api
```

自定义的图床需要修改 `src/image.ts` 文件, 以及 `vite.config.ts` 里的代理路径

## docker

```bash
docker build -t fyjlsq-web-image .
```

```bash
docker run -p 5000:5000 --name fyjlsq-web fyjlsq-web-image
```