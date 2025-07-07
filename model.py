from sqlalchemy import Column, Integer, String, Boolean, Date, Time, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Tarefa(Base):
    __tablename__ = 'tarefas'
    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String)
    prioridade = Column(String)
    data_limite = Column(Date)
    horario_limite = Column(Time)
    alerta_ativado = Column(Boolean, default=False)
    minutos_antes_alerta = Column(Integer, default=30)
    concluida = Column(Boolean, default=False)

engine = create_engine('sqlite:///database/tasknote.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
