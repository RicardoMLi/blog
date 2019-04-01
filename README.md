## 环境配置
### venv虚拟环境安装配置
```
pip3 install virtualenv
virtualenv venv
```

### 激活虚拟环境
```
Linux
  workon venv
Windows
  1. cd venv/Scripts
  2. active
```

### 安装第三方依赖
```
pip install -r requirement.txt
```

### 系统参数配置
修改数据库配置
```
settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DATABASENAME,
        'USER': USERNAME,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': 3306
    }
}
```

### 数据库初始化
1. 进入项目文件夹
2. 初始化数据库
```
python manage.py makemigrations
python manage.py migrate
```

### 启动应用
```
python manage.py runserver
```
