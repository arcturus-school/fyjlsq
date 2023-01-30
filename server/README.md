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
