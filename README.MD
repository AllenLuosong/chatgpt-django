# chatgpt-django
使用django搭建的chatgpt后台服务


# ✨ 介绍

基于的 [chatgpt-web](https://github.com/Chanzhaoyu/chatgpt-web) 二次开发，适配[后台 chatgpt-django](https://github.com/AllenLuosong/chatgpt-django)，后续版本开发会在此项目上更新上线新功能


# 🔨构建运行

## 💾 环境准备

```shell
# 复制一份配置文件 并填充apikey apibaseurl
cp .env.example .env

```

```shell
# Nginx sever的配置
    listen       80;
    listen  [::]:80;
    server_name  localhost;

    location /api/ {
        proxy_pass   http://chatgpt-django:9004/;
    }



```

```shell
# 克隆项目
git clone https://github.com/AllenLuosong/chatgpt-django

# 进入项目
cd chatgpt-django

# 使用docker启动
docker-compose up -d 
```