import auth
import email_utilis

# ==============================================================================
# DADOS DA DONA DO SISTEMA (EDITAR AQUI)
# ==============================================================================
NOME_REAL_ADMIN = "Isabella Melo"             # Nome da dona
EMAIL_ADMIN = "isamelonutricao@gmail.com"     # E-mail que vai RECEBER a senha
USUARIO_LOGIN = "IsaMeloNutri"                       # O login que ela vai usar
# ==============================================================================

def criar_primeiro_admin():
    print("--- INICIANDO CONFIGURAÇÃO DO ADMIN ---")
    
    # 1. Garante que o banco existe
    auth.create_usertable()
    
    # 2. Gera uma senha aleatória usando a função que já criamos
    senha_forte = email_utilis.gerar_senha_aleatoria(10)
    
    # 3. Salva no banco de dados
    # role='admin' -> Dá poderes totais
    # force_change=1 -> Obriga ela a trocar a senha ao entrar
    try:
        auth.add_userdata(USUARIO_LOGIN, auth.make_hashes(senha_forte), role='admin', force_change=1)
        print(f"✅ Usuário '{USUARIO_LOGIN}' criado no banco de dados.")
    except Exception as e:
        print(f"❌ Erro ao salvar no banco (o usuário já existe?): {e}")
        return

    # 4. Envia o e-mail para a dona
    print(f"📧 Enviando e-mail para {EMAIL_ADMIN}...")
    sucesso, msg = email_utilis.enviar_credenciais(NOME_REAL_ADMIN, EMAIL_ADMIN, USUARIO_LOGIN, senha_forte)
    
    if sucesso:
        print("✅ SUCESSO! O e-mail foi enviado. Peça para ela verificar a caixa de entrada.")
    else:
        print(f"⚠️ O usuário foi criado, mas o e-mail falhou: {msg}")
        print(f"A senha gerada foi: {senha_forte} (Anote, pois não foi enviada)")

if __name__ == "__main__":
    criar_primeiro_admin()