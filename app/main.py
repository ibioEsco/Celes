from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from .connection import Connection
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
SECRET_KEY = "dbab42abae14dacc4687afd7f1192d87039e31bebb668068ddf3d37b7c6283ad"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 2


fake_users_db = {
    "ibio": {
        "username": "ibio",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()





def log_and_handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            logger.info(f"Success: {func.__name__} with args: {args} kwargs: {kwargs}")
            return result
        except Exception as ex:
            logger.error(f"Error in {func.__name__}: {str(ex)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error: {str(ex)}"
            )
    return wrapper

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt



async def get_current_active_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    return username


@app.get("/")
def read_root():
    return {"message": "Bienvenido al microservicio de consultas"}

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.post("/sales/by_employee/{employee}")
@log_and_handle_exceptions
async def read_employee(employee: str, _: Annotated[User, Depends(get_current_active_user)]):
    cone = Connection()
    return cone.select_fire_store('employee_sales', 'Employees', 'Employee', employee)


@app.post("/sales/by_product/{product}")
@log_and_handle_exceptions
async def read_produc(product: str, _: Annotated[User, Depends(get_current_active_user)]):
    cone = Connection()
    employee_retturn = cone.select_fire_store('product_sales','Products','Product',product)
    return employee_retturn

    

@app.post("/sales/by_store/{store}")
@log_and_handle_exceptions
def get_sales_by_product(store: str, _: Annotated[User, Depends(get_current_active_user)]):
    cone = Connection()
    employee_retturn = cone.select_fire_store('store_sales','Stores','Store',store)
    return employee_retturn


@app.post("/sales/total_avg_by_employee/{avg_employee}")
@log_and_handle_exceptions
def get_sales_by_product(avg_employee: str, _: Annotated[User, Depends(get_current_active_user)]):
    cone = Connection()
    employee_retturn = cone.select_fire_store_average_sales('promedio_employee_sales','Employees','Employee',avg_employee)
    return employee_retturn



@app.post("/sales/total_avg_by_product/{avg_produc}")
@log_and_handle_exceptions
def get_sales_by_product(avg_produc: str, _: Annotated[User, Depends(get_current_active_user)]):
    cone = Connection()
    employee_retturn = cone.select_fire_store_average_sales('promedio_products_sales','Products','Product',avg_produc)
    return employee_retturn


@app.post("/sales/total_avg_by_store/{avg_store}")
@log_and_handle_exceptions
def get_sales_by_product(avg_produc :str, _: Annotated[User, Depends(get_current_active_user)]):
    cone = Connection()
    employee_retturn = cone.select_fire_store_average_sales('promedio_store_sales','Stores','Store',avg_produc)
    return employee_retturn


