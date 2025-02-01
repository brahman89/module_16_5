from fastapi.responses import HTMLResponse
from fastapi import FastAPI, status, Body, HTTPException, Request, Form, Path
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import Annotated

app = FastAPI(swagger_ui_parameters={"tryItOutEnable": True}, debug=True)

templates = Jinja2Templates(directory='app/m16_5')


users = []


class Users(BaseModel):
    id: int
    username: str
    age: int


@app.get("/")
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get(path="/users/{user_id}")
async def get_user(request: Request, user_id: Annotated[int, Path(ge=1)]) -> HTMLResponse:
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})

    raise HTTPException(status_code=404, detail=f"User not found {user_id}")


@app.post(path="/", status_code=status.HTTP_201_CREATED)
async def add_user(request: Request, username: str = Form(), age: int = Form()) -> HTMLResponse:
    if users:
        user_id = max(users, key=lambda m: m.id).id + 1
    else:
        user_id = 1
    users.append(Users(id=user_id, username=username, age=age))
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.put(path="/users/{user_id}/{username}/{age}")
async def update_user(user_id: int, username: str, age: int):
    for u in users:
        if u.id == user_id:
            u.username = str(username)
            u.age = int(age)
            return f"{u} is updated"
    raise HTTPException(status_code=404, detail="User not found")


@app.delete(path="/users/{user_id}", response_model=dict)
async def del_user(user_id: int):
    for i, t in enumerate(users):
        if t.id == user_id:
            del users[i]
            return {"detail": "User Delete"}
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/")
def kill_users_all() -> str:
    users.clear()
    return "All users deleted!"

# @app.post("/users/{username}/{age}")
# async def add_user(
#         username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
#         age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")]) -> list:
#
#     user_id = str(int(len(users) + 1)
#
#     user: List[User] = [User(id=user_id, username=username, age=age)]

# return f"User username - {username}, age - {age}  is registered!"

#
# @app.put("/users/{user_id}/{username}/{age}")
# async def update_user(user_id: int,
#                       username: Annotated[
#                           str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
#                       age: Annotated[int, Path(ge=18, le=120, description="Enter age", example="24")]) -> list:
#     users[user_id] = f"Имя: {username}, возраст: {age}"
#     return f"The user {user_id} is updated"
#
#
# @app.delete("/users/{user_id}")
# async def delete_user(user_id: int) -> dict:
#     users.pop(str(user_id))
#     return f"User with ID {user_id} was deleted."
