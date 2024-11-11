from fastapi import FastAPI, Path, HTTPException, Request, Form, status, Body
from pydantic import BaseModel
from typing import Annotated, List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})
templates = Jinja2Templates(directory='./templates')
users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int



@app.get('/')
async def get_main(request:Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get(path='/user/{user_id}')
async def get_users(request:Request, user_id:int) -> HTMLResponse:
    try:
        return templates.TemplateResponse('users.html',{'request':request,'user_id': users[user_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')




@app.post('/user/{username}/{age}', status_code=HTTP_201_CREATED)
async def post_user(request: Request, user: str = Form()) -> HTMLResponse:
    # user.id = len(users)
    if users:
        user_id = max(users, key = lambda u: u.id).id + 1
    else:
        user_id = 1
    users.append(User(id=user_id, username= username, age= age)
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1, le=150, description='Enter user ID', example=1)],
                      username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=28)]) -> str:
    # Получаем объект "User" из списка "users"
    # Сначала сделаем из списка 'users' свой словарь. {'id':index}
    dict1 = {dict_i.id: users.index(dict_i) for dict_i in users}
    try:
        user_index = dict1[user_id]  # Поиск по ключу в словаре 'dict1'
        user_for_update = users[user_index]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"User №{user_id} was not found")
    else:
        # Изменяем объект "User"
        user_for_update.username = username
        user_for_update.age = age
        # Обновляем элемент списка "users"
        # users[user_index] = user_for_update
        return (f"User №{user_id} is updated: "
                f"username={users[user_index].username}, "
                f"age={users[user_index].age}")


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')],) -> str:
    # Сначала сделаем из списка 'users' свой словарь. {'id':index}
    dict1 = {dict_i.id: users.index(dict_i) for dict_i in users}
    try:
        user_index = dict1[user_id]  # Поиск по ключу в словаре 'dict1'
        # Для красоты запомним
        deleted_user_name = users[user_index].username
        deleted_user_age = users[user_index].age
        # Удаляем из списка
        users.pop(user_index)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"User №{user_id} was not found")
    else:
        return (f"User №{user_id} is deleted: "
                f"username={deleted_user_name}, "
                f"age={deleted_user_age}")

    # uvicorn module_16_4:app --reload
