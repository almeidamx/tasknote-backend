from pydantic import BaseModel, ConfigDict
from typing import List

class UsuarioSchema(BaseModel):
    nome: str 
    email: str 

class UsuarioViewSchema(UsuarioSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ListagemUsuariosSchema(BaseModel):
    usuarios: List[UsuarioViewSchema]

class UsuarioIdSchema(BaseModel):
    usuario_id: int
