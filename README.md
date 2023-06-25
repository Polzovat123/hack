# hack 
Это серверная мл-ная часть проекта. 
Развертка нашего приложения доступна в нескольких возможных вариантах:
1. запусутить run.py в директории 
2. запустить Dockerfile для развертки в контейнере
docker build -t server_hack 
docker run -it --gpus all -p 6432:6432 server_hack /bin/bash
