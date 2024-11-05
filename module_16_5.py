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