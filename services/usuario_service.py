from model import Session
from model.usuario import Usuario
from model.task import Tarefa
from sqlalchemy.exc import IntegrityError

class UsuarioService:
    @staticmethod
    def criar_usuario(body):
        session = Session()
        try:
            usuario = Usuario(nome=body.nome, email=body.email)
            session.add(usuario)
            session.commit()
            session.refresh(usuario)  # Garante que os atributos estão carregados
            return usuario, None
        except IntegrityError:
            session.rollback()
            return None, 'E-mail já cadastrado.'
        except Exception:
            session.rollback()
            return None, 'Erro ao cadastrar usuário.'
        finally:
            session.close()

    @staticmethod
    def deletar_usuario(usuario_id):
        session = Session()
        try:
            usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
            if not usuario:
                return False
            session.query(Tarefa).filter(Tarefa.usuario_id == usuario_id).delete()
            session.delete(usuario)
            session.commit()
            return True
        finally:
            session.close()

    @staticmethod
    def listar_usuarios():
        session = Session()
        try:
            return session.query(Usuario).all()
        finally:
            session.close()
