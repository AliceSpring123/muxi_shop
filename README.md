# Muxi Shop

前后端分离的电商项目

## 项目结构

muxi_shop/
├── muxi_shop_api/ # Django 后端 API
├── muxi_shop_web/ # Vue.js 前端
└── .gitignore

## 开发设置

### 后端 (Django)

```bash
cd muxi_shop_api
pipenv shell
pip install mysqlclient django-cors-headers djangorestframework
python manage.py runserver
```

### 前端 (Vue)

```bash
cd muxi_shop_web
npm install
npm run serve
```