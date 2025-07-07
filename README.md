# TaskNote Backend

Organizador de tarefas diárias com alerta de prazo.

## Como clonar o repositório

Clone este projeto usando o comando:
```bash
git clone https://github.com/almeidamx/tasknote-backend.git
```

## Como rodar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Para executar a API, execute:
   ```bash
   python app.py
   ```

Acesse a documentação Swagger em [http://localhost:5000/swagger](http://localhost:5000/swagger) ou simplesmente acesse a raiz do backend em [http://localhost:5000/](http://localhost:5000/) para ser redirecionado automaticamente para a documentação da API.

## (Opcional) Testar envio de e-mails com MailHog

Para testar o envio de e-mails de alerta sem enviar e-mails reais, podemos pode usar o MailHog, uma ferramenta de testes para capturar e visualizar e-mails localmente.

1. Execute o comando abaixo via Terminal para executar o MailHog no Docker e iniciar seu serviço:
   ```bash
   docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog
   ```
   - O serviço SMTP ficará disponível em `localhost:1025` (usado automaticamente pela aplicação).
   - A interface web para visualizar os e-mails estará em [http://localhost:8025](http://localhost:8025).

2. Após criar uma tarefa e esperar seu devido tempo, confira os e-mails recebidos acessando a interface web do MailHog.

3. Este passo é **opcional** e serve apenas para testes locais de envio de e-mails, e mostra que a aplicação pode ser facilmente adaptada para envio de e-mails reais.


