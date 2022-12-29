# 非物质文化遗产交流社区

🤗 作为课设的一个备份

## 本地开发

### 服务器端-flask

用到了 `mysql` 数据库, 需要在 `config.py` 下填写相关配置

```bash
virtualenv venv
```

```bash
./venv/Scripts/activate
```

安装项目依赖

```bash
pip install -r requirements.txt
```

运行项目

```bash
flask --debug run
```

### 前端-vue

```bash
pnpm install
```

修改 `/src/config.js` 中的相关配置

```bash
pnpm run dev
```
