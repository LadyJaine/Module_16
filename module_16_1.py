from fastapi import FastAPI
app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})

@app.get('/')
async def main_page():
    return "Главная страница"

@app.get('/user/admin')
async def get_admin_page():
 return 'Вы вошли как администратор'
# http://127.0.0.1:8000/user/100

@app.get('/user/{user_id}')
async def get_user_number(user_id: int):
 return f'Вы вошли как пользователь № {user_id}'