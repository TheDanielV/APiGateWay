from pydantic import BaseModel


class UserBase(BaseModel):
    ci: str
    name: str
    last_name: str
    cellphone: str
    direction: str
    auth_token: str


class VehicleBase(BaseModel):
    marca: str
    modelo: str
    placa: str
    usuario_id: str
    anio: str
    color: str


class AuthBase(BaseModel):
    username: str
    password: str
    email: str


class AuthenticateUser(BaseModel):
    username: str
    password: str
