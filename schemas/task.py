from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date, time
from .usuario import UsuarioSchema, UsuarioViewSchema, ListagemUsuariosSchema


class TarefaSchema(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    prioridade: str
    data_limite: date
    horario_limite: time
    minutos_antes_alerta: Optional[int] = 30
    usuario_id: int 

class TarefaBuscaSchema(BaseModel):
    id: int

class TarefaViewSchema(BaseModel):
    id: int
    titulo: str
    descricao: str | None = None
    prioridade: str
    data_limite: date  
    horario_limite: time  
    minutos_antes_alerta: int | None = 30
    usuario_id: int
    usuario: Optional[UsuarioViewSchema] = None 
    model_config = ConfigDict(from_attributes=True)

class ListagemTarefasSchema(BaseModel):
    tarefas: List[TarefaViewSchema]

class TarefaIdSchema(BaseModel):
    id: int

class TarefaUpdateSchema(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    prioridade: Optional[str] = None
    data_limite: Optional[date] = None
    horario_limite: Optional[time] = None
    minutos_antes_alerta: Optional[int] = None
    usuario_id: Optional[int] = None
