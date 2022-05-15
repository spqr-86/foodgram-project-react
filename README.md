<h1 align="center">foodgram_project</h1>

![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

# Описание сервиса
Сайт Foodgram, «Продуктовый помощник». Cервис для публикации рецептов.<br> 
Пользователи могут подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в список «Избранное», 
а перед походом в магазин скачивать сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд.

# Сайт
http://178.154.208.254/

user: user  
password: passworduser

# Установка
1. Клонируйте репрозиторий ```https://github.com/spqr-86/foodgram-project-react```
2. Установите Docker (https://docs.docker.com/engine/install/)
3. Выполните ```docker-compose up -d --build```
4. Выполните:<br>
  ```docker-compose exec web python manage.py migrate --noinput```<br>
  ```docker-compose exec web python manage.py createsuperuser```<br>
  ```docker-compose exec web python manage.py collectstatic --no-input ```
5. Теперь проект доступен по адресу http://178.154.208.254

# Технологии
* Python
* Django
* Django REST
* Docker

# Проект разработал:
* [Петр Балдаев](https://github.com/spqr-86)
