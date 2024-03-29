# Сервис для соцсети обмена рецептами
Проект состоит из фронтэнда на JS и бекэнда на Python. 
Написан по документации API и техническому задинию к готовому фронту.
Настроен CI/CD с тестами, деплоем и запуском в контейнерах на удаленном сервере.
Сервис выполнен в рамках курса ["Python-разрабочик плюс"](https://practicum.yandex.ru/profile/python-developer-plus/) Яндекс Практикума.

## Технологии в проекте
- React
- Node
- Python v.3.8
- Django v.2.2.16
- Django REST framework v.3.12.4
- postgres v.13.0
- Docker 
- gunicorn v.20.1.0
- nginx v.1.19.3
- Git Actions

## Функционал
Сервис позволяет:
- регистрировать, аутентифицировать и авторизовывать пользователей
- смотреть, размещать и редактировать рецепты, 
- добавлять их в избранное и/или корзину,
- формировать список покупок инредиентов рейептов в корзине
- администратору упралять контентом и пользователями

Полная [документация API](https://github.com/sldmxm/foodgram-project-react/tree/master/docs) проекта после запуска доступна по адресу: /api/docs/redoc/ в формате redoc

## Установка проекта    
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
Для запуска приложения локально в контейнерах перейдите в директорию "infra":
```
docker-compose up -d --build 
```
Осталось выполнить миграции, создать администратора, выгрузить статику:
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
