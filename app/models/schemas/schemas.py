from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    last_name: str
    ci: str
    cellphone: str
    direction: str



class VehicleBase(BaseModel):
    marca: str
    modelo: str
    placa: str
    usuario_id: str
    anio: str
    color: str
