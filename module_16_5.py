'''Задача "Список пользователей в шаблоне":
Подготовка:
Используйте код из предыдущей задачи.
Скачайте заготовленные шаблоны для их дополнения.
Шаблоны оставьте в папке templates у себя в проекте.
Создайте объект Jinja2Templates, указав в качестве папки шаблонов - templates.
Измените и дополните ранее описанные CRUD запросы:
Напишите новый запрос по маршруту '/':
Функция по этому запросу должна принимать аргумент request и возвращать TemplateResponse.
TemplateResponse должен подключать ранее заготовленный шаблон 'users.html', а также передавать в него request и список users. Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.
Измените get запрос по маршруту '/user' на '/user/{user_id}':
Функция по этому запросу теперь принимает аргумент request и user_id.
Вместо возврата объекта модели User, теперь возвращается объект TemplateResponse.
TemplateResponse должен подключать ранее заготовленный шаблон 'users.html', а также передавать в него request и одного из пользователей - user. Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.
Создайте несколько пользователей при помощи post запроса со следующими данными:
username - UrbanUser, age - 24
username - UrbanTest, age - 22
username - Capybara, age - 60
В шаблоне 'users.html' заготовлены все необходимые теги и обработка условий, вам остаётся только дополнить закомментированные строки вашим Jinja 2 кодом (использование полей id, username и age объектов модели User):
1. По маршруту '/' должен отображаться шаблон 'users.html' со списком все ранее созданных объектов:
2. Здесь каждая из записей является ссылкой на описание объекта, информация о котором отображается по маршруту '/user/{user_id}':'''

from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from typing import List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")
users = []


class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/")
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/user/{user_id}")
async def get_users(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id - 1]})

@app.post("/user/{username}/{age}")
async def create_user(username: str, age: int) -> User:
    if users:
        last_user_id = users[-1].id
        user_id = last_user_id + 1
    else:
        user_id = 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put('/user/{id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int):
    try:
        edit_user = users[user_id-1]
        edit_user.username = username
        edit_user.age = age
        return edit_user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.delete('/user/{id}')
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(i)  # Удаляем и сохраняем удаленного пользователя
            return deleted_user
    raise HTTPException(status_code=404, detail="User was not found")


# Python -m uvicorn module_16_5:app
