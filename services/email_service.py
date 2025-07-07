from config import SMTP_SERVER, SMTP_PORT, SMTP_USER
import smtplib
from email.mime.text import MIMEText

class EmailService:
    @staticmethod
    def enviar_email(destinatario, assunto, mensagem):
        msg = MIMEText(mensagem)
        msg['Subject'] = assunto
        msg['From'] = SMTP_USER
        msg['To'] = destinatario
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.sendmail(SMTP_USER, destinatario, msg.as_string())
