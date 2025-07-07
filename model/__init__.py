from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .task import Base

engine = create_engine('sqlite:///database/tasknote.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
