from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from .usuario import Usuario, Base

class Tarefa(Base):
    __tablename__ = 'tarefas'
    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String)
    prioridade = Column(String)
    data_limite = Column(Date)
    horario_limite = Column(Time)
    minutos_antes_alerta = Column(Integer, default=30)

    # Chave estrangeira para o usuário
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    # Relacionamento com o usuário
    usuario = relationship("Usuario", back_populates="tarefas")
