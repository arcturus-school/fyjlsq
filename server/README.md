<div>
    <img src="https://img.shields.io/badge/python-3.11.1-orange" alt="python"/>
    <img src="https://img.shields.io/badge/flask-2.2.2-blue" alt="flask" />
</div>

## 本地开发

```bash
pip3 install virtualenv
```

```bash
virtualenv venv
```

windows

```bash
./venv/Scripts/activate
```

linux

```bash
source ./venv/bin/activate
```

install project dependencies

```bash
pip install -r requirements.txt
```

start this project

```bash
flask --debug run
```

获取依赖

```bash
pip freeze > requirements.txt
```

## docker

```bash
docker build -t fyjlsq-server-image .
```

```bash
docker run -p 5000:5000 --name fyjlsq-server fyjlsq-server-image
```

## 超级管理员账户

user: root

password: root123456

## 可配置环境变量(.env)

```
JWT_SECRET_KEY=FYJLSQ # jwt 秘钥
JWT_ACCESS_TOKEN_EXPIRES=365 # jwt 过期时间
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DB=fyjlsq
```

```bash
# MYSQL_HOST=172.17.0.1 # 单独 docker build 时使用

MYSQL_HOST=mysql # docker-compose 时使用
```