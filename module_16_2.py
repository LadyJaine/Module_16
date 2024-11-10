from fastapi import FastAPI, Path
from typing import Annotated
app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})


@app.get('/')
async def main_page():
    return "Главная страница"


@app.get('/user/{user_id}')
async def get_user_id(user_id: Annotated[int, Path(min_length=1, max_length=100,
                                      description='Enter User ID', example='1')]):
    return f'Вы вошли как пользователь №:{user_id}'


@app.get('/user/{username}/{age}')
async def get_user_info(
        username: Annotated[str, Path(min_length=5, max_length=20,
                                      description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(le=120, ge=18, description='Enter age',
                                 example='24')]):
    return f'Информация о пользователе. Имя:{username}, Возраст:{age}'
