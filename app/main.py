from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from app.database import(
    create_user,get_user_by_username,init_db
)

app = FastAPI(title="API Test Lab")

init_db()


class UserRegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=6, max_length=50)


class UserLoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=6, max_length=50)


class UserResponse(BaseModel):
    username: str


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post(
    "/users/register",
    status_code=status.HTTP_201_CREATED,
)
def register_user(user: UserRegisterRequest):
    stored_user = get_user_by_username(user.username) 
    if stored_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    create_user(user.username,user.password)

    return {
        "message": "User registered successfully",
        "username": user.username,
    }


@app.post("/users/login")
def login_user(user: UserLoginRequest):
    stored_user = get_user_by_username(user.username)

    if stored_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if stored_user["password"] != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return {
        "message": "Login successful",
        "username": user.username,
    }


#查询用户是否存在
@app.get(
    "/user/{username}",
    response_model= UserResponse,
)
def get_user(username:str):
    stored_user = get_user_by_username(username)
    if stored_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return stored_user