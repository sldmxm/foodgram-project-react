## Сервис Foodgram

### Описание проекта
Сервис позволяет:
- смотреть, размещать и редактировать рецепты, 
- добавлять их в избранное и/или корзину,
- формировать список покупок инредиентов рейептов в корзине

Состоит из фронтэнда на JS и бекэнда на Python

Полная документация API проекта доступна по адресу: /api/docs/redoc/ в формате redoc

Сервис выполнен в рамках курса ["Python-разрабочик плюс"](https://practicum.yandex.ru/profile/python-developer-plus/) Яндекс Практикума.

### Установка проекта    
Клонируйте репозиторий:
```
git clone git@github.com:sldmxm/foodgram-project-react.git
```
В директории infra создайте файл .env:
```
# Укажите, что используете postgresql
DB_ENGINE=django.db.backends.postgresql
# Укажите имя созданной базы данных
DB_NAME=foodgram
# Укажите имя пользователя
POSTGRES_USER=foodgram
# Укажите пароль для пользователя
POSTGRES_PASSWORD=xxxxxxxxxxxxxxxx
# Укажите localhost
DB_HOST=db
# Укажите порт для подключения к базе
DB_PORT=5432 
# Перенесите SECRET_KEY из settings.py бекенда 
SECRET_KEY=xxxxxxxxxxxxxxxx 
```
Для запуска приложения локально в контейнерах перейдите в директорию "infra" и выполните:
```
docker-compose up -d --build 
```
Осталось выполнить миграции, создать администратора и выгрузить статику
```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input 
```
Теперь проект готов к работе, фронтенд на http://localhost/
Доступ к API http://localhost/api/, к админке: http://localhost/admin
Полная документация по работе с API http://localhost/api/docs/redoc/

### Наполнение базы
Можно загрузить ингредиенты из csv файла:
```
docker cp <путь до директории с csv-файлами> <id>:backend/

docker-compose exec backend python manage.py import_ingredients 
```

### Технологии в проекте
- React
- Node
- Python v.3.8
- Django v.2.2.16
- Django REST framework v.3.12.4
- postgres v.13.0
- Docker 
- gunicorn v.20.1.0
- nginx v.1.19.3

### Размещение
http://solmax.hopto.org/
u: admin
p: ghbvfghbvf