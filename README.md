# TipTop от OaksDungeon
## Описание проекта

Даный проект является вариантом сервиса для бронирования билетов на музейные мероприятия.

## Ключевые функции

- 🔍 **Отображение музейных мероприятий**: Использую технологию парсинга сайта с применением RSS ленты, программа отображает на странице 25 наиболее актуальных музейных мероприятий.
  
- 🗒️ **Бронирование билетов**: Пользователь может забронировать билет на любое мероприятие, заполнив специальную форму и подтвердив участие с помощью письма на электронную почту.

- 🫳 **Анализ записей**: Администратор иммет возможность провести анализ всех созданных записей с помощью специальной страницы, на которой они отображены.

- 🚮 **Удаление**: Программа автоматически удаляет неподтвержденные записи каждые 3 минуты.

- ⬇️ **Авторизация и регистрация**: Авторизация и регистрация пользователя происходит с использованием собсвтенной базы данных, при этом пароли шифруются ключом, отвечающим всем стандартам безопасности.

## Как начать

1. Убедитесь, что ваша среда соответствует требованиям из `requirements.txt` и `npm.txt` (так же вам необходим установленный Python3, Uvicorn, PostgreSQL и npm).
2. Импортируйте файл `Museum_bd_backup.sql` с помощью pgAdmin 4.
3. Заполните dbname, user, password, host, port в обозначенном месте в файле `main.py` в соответсвии с вашими данными.
4. Скачайте архив по ссылке `https://disk.yandex.ru/d/xAwxzzCBn-4gdQ` и распакуйте содержимое в `/client/`.
5. Запустите сервер, перейдя по пути `Server/` и выполнив в терминале строку `uvicorn main:app --host 0.0.0.0 --port 8000`
6. Откройте файл `client/app/api.tsx`.
7. В строку `api = ***` вставьте строку `http://{ip_устройства_на_котором_запускается_uvicorn_сервер}:8000` (пример: `http://192.168.0.13:8000`). Сохраните изменение в файле.
8. Запустите веб-приложение, перейдя по пути `client/museum/app` и выполнив команду `npm start`.
9. Откройте браузер и перейдите по адресу `http://localhost:3000` (на устройстве, на котором запущено веб-приложение) или по адресу `http://{ip_адрес_устройства_с_запущенным_веб-приложением}:3000/` (на других устройствах).
10. Можете пользоваться веб-приложением!

P.s.: ВАЖНО! Доступ осуществляется внутри локальной сети. То есть устройство с запущенным на нем веб-приложением и устройство с которого осуществляется доступ должны находится в одной сети. Так же в связи устройство на котором запускается Uvicorn сервер (с FastAPI) и устройство с запущенным npm севрером должны быть разными. Не получится запустить оба сервера на одном устройстве. 

## Особенности

- **Масштабируемость**: Наш проект автоматически получает все новые обновления в базе данных сайта музея.
  
- **Современный дизайн**: Веб-интерфейс создан с учетом последних трендов в дизайне, обеспечивая вас приятным и продуктивным опытом, при этом сохраняя фирменный стиль сайта Tele2.

- **Открытый исходный код**: Мы приветствуем вклады и обратную связь от сообщества. Присоединяйтесь к нашему проекту и делитесь своим опытом!

## Демонстрация работы программы
### Демонстрация пк-версии
![alt-text](demo1.gif)

### Демонстрация мобильной версии
![alt-text](demo2.gif)


## О команде Oaks Dungeons
### Участники
- Сорокина Александра Валерьевна (капитан)
- Винтерголлер Тимофей Андреевич

### Описание
Команда, состоящая из студентов 2 курса группы 1520321 Института Передовых Информационных Технологий.

**Соединим виртуальное и реальное, создадим будущее вместе!** 🚀🌟

*С любовью, команда Oaks Dungeons*
