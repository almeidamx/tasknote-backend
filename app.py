from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from flask_cors import CORS
from model import Session
from model.task import Tarefa
from model.usuario import Usuario
from schemas.task import TarefaSchema, TarefaViewSchema, ListagemTarefasSchema, TarefaIdSchema, TarefaUpdateSchema, UsuarioSchema, UsuarioViewSchema, ListagemUsuariosSchema
from schemas.error import ErrorSchema, MensagemSchema
from schemas.usuario import UsuarioIdSchema  # Importa o novo schema
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from pydantic import Field
from services.usuario_service import UsuarioService
from services.task_service import TaskService

# Informações da API para documentação OpenAPI
info = Info(title="TaskNote API", version="1.0.0")
# Instância principal do aplicativo Flask com OpenAPI
app = OpenAPI(__name__, info=info)
# Habilita CORS para permitir requisições de outros domínios
CORS(app)

# Tag utilizada para agrupar rotas relacionadas a tarefas
usuario_tag = Tag(name="Usuario", description="CRUD de usuários")
tarefa_tag = Tag(name="Tarefa", description="CRUD de tarefas")

# Endpoint para adicionar um novo usuário
@app.post('/usuario', tags=[usuario_tag], responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_usuario(body: UsuarioSchema):
    """Adiciona um novo usuário ao banco de dados."""
    usuario, erro = UsuarioService.criar_usuario(body)
    if usuario:
        return {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email
        }, 200
    elif erro == 'E-mail já cadastrado.':
        return {"message": erro}, 409
    else:
        return {"message": erro or "Erro ao cadastrar usuário."}, 400

# Endpoint para listar todos os usuários
@app.get('/usuarios', tags=[usuario_tag], responses={"200": ListagemUsuariosSchema})
def listar_usuarios():
    """Lista todos os usuários cadastrados no banco de dados."""
    usuarios = UsuarioService.listar_usuarios()
    usuarios_serializados = [
        {"id": u.id, "nome": u.nome, "email": u.email}
        for u in usuarios
    ]
    return {"usuarios": usuarios_serializados}

# Endpoint para adicionar uma nova tarefa
@app.post('/tarefa', tags=[tarefa_tag], responses={"200": TarefaViewSchema, "400": ErrorSchema})
def add_tarefa(body: TarefaSchema):
    """Adiciona uma nova tarefa ao banco de dados."""
    tarefa, erro = TaskService.criar_tarefa(body)
    if tarefa:
        return {
            "id": tarefa.id,
            "titulo": tarefa.titulo,
            "descricao": tarefa.descricao,
            "prioridade": tarefa.prioridade,
            "data_limite": tarefa.data_limite.isoformat() if tarefa.data_limite else None,
            "horario_limite": tarefa.horario_limite.isoformat() if tarefa.horario_limite else None,
            "minutos_antes_alerta": tarefa.minutos_antes_alerta,
            "usuario_id": tarefa.usuario_id
        }, 200
    else:
        return {"message": erro or "Erro ao cadastrar tarefa."}, 400

# Endpoint para listar todas as tarefas cadastradas
@app.get('/tarefas', tags=[tarefa_tag], responses={"200": ListagemTarefasSchema})
def listar_tarefas():
    """Lista todas as tarefas cadastradas no banco de dados."""
    tarefas = TaskService.listar_tarefas()
    tarefas_serializadas = [
        {
            "id": t.id,
            "titulo": t.titulo,
            "descricao": t.descricao,
            "prioridade": t.prioridade,
            "data_limite": t.data_limite.isoformat() if t.data_limite else None,
            "horario_limite": t.horario_limite.isoformat() if t.horario_limite else None,
            "minutos_antes_alerta": t.minutos_antes_alerta,
            "usuario_id": t.usuario_id,
            "usuario": {
                "nome": t.usuario.nome,
                "email": t.usuario.email
            } if t.usuario else None
        }
        for t in tarefas
    ]
    return {"tarefas": tarefas_serializadas}

# Função para envio de e-mail de alerta
def enviar_email_alerta(destinatario, assunto, mensagem):
    """Função exemplo para envio de e-mail de alerta usando MailHog (localhost:1025)."""
    import smtplib
    from email.mime.text import MIMEText
    # Configurações do servidor SMTP para o MailHog
    smtp_server = 'localhost'
    smtp_port = 1025
    smtp_user = 'tasknote@localhost'
    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = smtp_user
    msg['To'] = destinatario
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.sendmail(smtp_user, destinatario, msg.as_string())
        
# Função para enviar alertas de tarefas próximas do vencimento
# chame  enviar_email_alerta quando a tarefa estiver próxima do vencimento

@app.get('/enviar_alertas', tags=[tarefa_tag])
def enviar_alertas():
    """Retorna uma lista de tarefas próximas do vencimento para alerta."""
    alertas = TaskService.enviar_alertas()
    return {"alertas": alertas}

# Endpoint para remover um usuário pelo ID
@app.delete('/usuario/<int:usuario_id>', tags=[usuario_tag], responses={"200": MensagemSchema, "404": ErrorSchema})
def deletar_usuario(path: UsuarioIdSchema):
    """Remove um usuário do banco de dados pelo ID informado."""
    sucesso = UsuarioService.deletar_usuario(path.usuario_id)
    if sucesso:
        return {"message": "Usuário excluído com sucesso.", "id": path.usuario_id}, 200
    else:
        return {"message": "Usuário não encontrado."}, 404

@app.delete('/tarefa/<int:id>', tags=[tarefa_tag], responses={"200": MensagemSchema, "404": ErrorSchema})
def deletar_tarefa(path: TarefaIdSchema):
    """Remove uma tarefa do banco de dados pelo ID informado."""
    sucesso = TaskService.deletar_tarefa(path.id)
    if sucesso:
        return {"message": "Tarefa excluída com sucesso.", "id": path.id}, 200
    else:
        return {"message": "Tarefa não encontrada."}, 404

@app.put('/tarefa/<int:id>', tags=[tarefa_tag], responses={"200": TarefaViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def atualizar_tarefa(path: TarefaIdSchema, body: TarefaUpdateSchema):
    """Atualiza os dados de uma tarefa existente pelo ID informado."""
    tarefa_id = path.id
    tarefa, erro = TaskService.atualizar_tarefa(tarefa_id, body)
    if tarefa:
        return {
            "id": tarefa.id,
            "titulo": tarefa.titulo,
            "descricao": tarefa.descricao,
            "prioridade": tarefa.prioridade,
            "data_limite": tarefa.data_limite.isoformat() if tarefa.data_limite else None,
            "horario_limite": tarefa.horario_limite.isoformat() if tarefa.horario_limite else None,
            "minutos_antes_alerta": tarefa.minutos_antes_alerta,
            "usuario_id": tarefa.usuario_id
        }, 200
    elif erro == 'Tarefa não encontrada.':
        return {"message": erro}, 404
    else:
        return {"message": erro or "Erro ao atualizar tarefa."}, 400

@app.get('/')
def redirect_to_openapi():
    """Redireciona para a documentação OpenAPI."""
    return redirect('/openapi')

# Inicializa o servidor Flask em modo debug
if __name__ == '__main__':
    app.run(debug=True)
