from model import Session
from model.task import Tarefa
from model.usuario import Usuario
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from .email_service import EmailService

class TaskService:
    @staticmethod
    def criar_tarefa(body):
        session = Session()
        try:
            usuario = session.query(Usuario).filter(Usuario.id == body.usuario_id).first()
            if not usuario:
                return None, 'Usuário não encontrado.'
            tarefa = Tarefa(**body.dict())
            session.add(tarefa)
            session.commit()
            session.refresh(tarefa)  # <-- Garante que os atributos estão carregados
            return tarefa, None
        finally:
            session.close()

    @staticmethod
    def deletar_tarefa(tarefa_id):
        session = Session()
        try:
            tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
            if not tarefa:
                return False
            session.delete(tarefa)
            session.commit()
            return True
        finally:
            session.close()

    @staticmethod
    def listar_tarefas():
        session = Session()
        try:
            return session.query(Tarefa).all()
        finally:
            session.close()

    @staticmethod
    def enviar_alertas():
        session = Session()
        try:
            agora = datetime.now()
            tarefas = session.query(Tarefa).filter(Tarefa.minutos_antes_alerta > 0).all()
            alertas = []
            for t in tarefas:
                dt_venc = datetime.combine(t.data_limite, t.horario_limite)
                minutos_restantes = int((dt_venc - agora).total_seconds() // 60)
                if 0 < minutos_restantes <= t.minutos_antes_alerta:
                    if t.usuario and t.usuario.email:
                        assunto = f"[TaskNote] Alerta: Tarefa '{t.titulo}' próxima do vencimento"
                        mensagem = (
                            f"Olá, {t.usuario.nome}!\n\n"
                            f"A tarefa '{t.titulo}' está próxima do vencimento.\n"
                            f"Prioridade: {t.prioridade}\n"
                            f"Entrega: {t.data_limite.strftime('%d-%m-%Y')} {t.horario_limite.strftime('%H:%M')}\n"
                            f"Restam {minutos_restantes} minutos para o prazo.\n\n"
                            f"Acesse o TaskNote para mais detalhes."
                        )
                        try:
                            EmailService.enviar_email(t.usuario.email, assunto, mensagem)
                        except Exception as e:
                            print(f"Erro ao enviar e-mail: {e}")
                    alertas.append({
                        "id": t.id,
                        "titulo": t.titulo,
                        "prioridade": t.prioridade,
                        "minutos_restantes": minutos_restantes,
                        "usuario": {
                            "nome": t.usuario.nome,
                            "email": t.usuario.email
                        } if t.usuario else None
                    })
            return alertas
        finally:
            session.close()

    @staticmethod
    def atualizar_tarefa(tarefa_id, body):
        session = Session()
        try:
            tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
            if not tarefa:
                return None, 'Tarefa não encontrada.'
            for field, value in body.dict(exclude_unset=True).items():
                setattr(tarefa, field, value)
            session.commit()
            session.refresh(tarefa)
            return tarefa, None
        except Exception as e:
            session.rollback()
            return None, str(e)
        finally:
            session.close()
