# foodgram-project
[![Foodgram-app workflow](https://github.com/dimasick11/foodgram-project/workflows/Foodgram-app_workflow/badge.svg)](https://github.com/dimasick11/foodgram-project/actions)

# Описание проекта
«Продуктовый помощник» (Проект Яндекс.Практикум)

Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, 
добавлять понравившиеся рецепты в «Избранное» и скачивать список необходимых продуктов для приготовления блюд.

##### **Стек технологий:**
* Python3
* Django
* Docker
* Docker-compose

## Build
`docker-compose build`.

## Migrate databases
`docker-compose run --rm web code/manage.py migrate`.

## Run
`docker-compose up`.
