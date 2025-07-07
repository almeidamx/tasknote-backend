from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time

# Esquema base para criação de uma tarefa
class TarefaSchema(BaseModel):
    titulo: str  
    descricao: Optional[str] = None  
    prioridade: str  
    data_limite: date  
    horario_limite: time  
    alerta_ativado: Optional[bool] = False 
    minutos_antes_alerta: Optional[int] = 30  

# para busca de tarefa por ID
class TarefaBuscaSchema(BaseModel):
    id: int 

# para visualização de tarefa
class TarefaViewSchema(TarefaSchema):
    id: int 
    concluida: bool  

# para listagem de tarefas
class ListagemTarefasSchema(BaseModel):
    tarefas: List[TarefaViewSchema] 
