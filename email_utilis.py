import smtplib
from email.mime.text import MIMEText
import secrets
import string
import os  
from dotenv import load_dotenv  

load_dotenv()

# --- SUAS CONFIGURAÇÕES (PREENCHA AQUI) ---
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
SENHA_APP_GMAIL = os.getenv("SENHA_EMAIL")

def gerar_senha_aleatoria(tamanho=8):
    """Gera uma senha aleatória com letras e números."""
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for i in range(tamanho))

def enviar_credenciais(nome, email_destino, usuario, senha):
    """Envia o e-mail com login e senha para o novo usuário."""
    msg_content = f"""
    Olá, {nome}!
    
    Seu cadastro no Sistema Nutri Pro foi realizado com sucesso.
    Aqui estão seus dados de acesso:
    
    👤 Usuário: {usuario}
    🔑 Senha Provisória: {senha}
    
    Acesse o sistema e troque sua senha no primeiro login.
    """
    
    msg = MIMEText(msg_content)
    msg['Subject'] = "Bem-vindo ao Nutri Pro - Seu Acesso"
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = email_destino

    try:
        # Conexão segura com Gmail (Porta 465)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_REMETENTE, SENHA_APP_GMAIL)
        server.sendmail(EMAIL_REMETENTE, email_destino, msg.as_string())
        server.quit()
        return True, "E-mail enviado com sucesso!"
    except Exception as e:
        return False, f"Erro ao enviar e-mail: {e}"