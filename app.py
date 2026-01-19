import streamlit as st
import pandas as pd
import os
import email_utilis
from datetime import datetime
from PIL import Image
from streamlit_option_menu import option_menu
import auth  # Seu arquivo de autenticação atualizado

# Nome do arquivo CSV onde os dados dos pacientes são salvos
ARQUIVO_DADOS = 'dados.csv'

def main():
    # --- 1. CONFIGURAÇÃO DA PÁGINA E LOGO ---
    try:
        # Tenta carregar a logo se ela existir
        logo_img = Image.open("logo.jpeg")
        page_icon_img = logo_img
    except:
        logo_img = None
        page_icon_img = "🍎"

    st.set_page_config(page_title="Sistema Nutri Pro", layout="wide", page_icon=page_icon_img)
    
    # Garante que a tabela de usuários existe
    auth.create_usertable()

    # --- 2. INICIALIZAÇÃO DE VARIÁVEIS DE SESSÃO ---
    if 'logado' not in st.session_state:
        st.session_state['logado'] = False
        st.session_state['usuario'] = ''
        st.session_state['role'] = ''           # Define se é 'admin' ou 'user'
        st.session_state['force_change'] = 0    # Define se precisa trocar a senha (0 ou 1)

    # --- 3. BLOQUEIO DE SEGURANÇA (Troca de Senha Obrigatória) ---
    # Se o usuário está logado E a "bandeira" de trocar senha for 1, ele fica preso aqui.
    if st.session_state['logado'] and st.session_state['force_change'] == 1:
        st.warning("🔒 SEGURANÇA: Este é seu primeiro acesso ou sua senha foi resetada. Você precisa definir uma nova senha pessoal.")
        
        with st.form("form_troca_senha"):
            nova_senha = st.text_input("Nova Senha", type="password")
            confirma_senha = st.text_input("Confirme a Nova Senha", type="password")
            btn_trocar = st.form_submit_button("Atualizar Minha Senha")
            
            if btn_trocar:
                if nova_senha == confirma_senha and len(nova_senha) >= 4:
                    # Atualiza no banco de dados e remove a obrigatoriedade
                    auth.update_password(st.session_state['usuario'], nova_senha)
                    
                    # Atualiza a sessão atual para liberar o acesso
                    st.session_state['force_change'] = 0 
                    
                    st.success("✅ Senha atualizada com sucesso! O sistema será liberado.")
                    st.rerun() # Recarrega a página para entrar no menu principal
                elif len(nova_senha) < 4:
                    st.error("A senha deve ter pelo menos 4 caracteres.")
                else:
                    st.error("As senhas não coincidem.")
        
        st.stop() # 🛑 IMPORTANTE: Isso impede que o resto do código abaixo seja executado.

    # --- 4. MENU LATERAL (Dinâmico) ---
    with st.sidebar:
        if logo_img:
            st.image(logo_img, use_container_width=True)
        
        # CASO 1: Usuário NÃO logado
        if not st.session_state['logado']:
            selected = option_menu(
                menu_title="Acesso",
                options=["Home", "Login"], # Note que "Cadastro" sumiu daqui!
                icons=["house", "key"],
                default_index=0,
            )
        
        # CASO 2: Usuário LOGADO
        else:
            st.markdown(f"Olá, **{st.session_state['usuario']}**!")
            
            # Opções básicas que todo mundo vê
            opcoes_menu = ["Inserir Dados", "Visualizar Base"]
            icones_menu = ["pencil-square", "table"]
            
            # Opção EXTRA apenas para Admin
            if st.session_state['role'] == 'admin':
                opcoes_menu.append("Gerenciar Usuários")
                icones_menu.append("person-plus-fill")
            
            # Botão de sair sempre aparece por último
            opcoes_menu.append("Sair")
            icones_menu.append("box-arrow-right")

            selected = option_menu(
                menu_title="Painel",
                options=opcoes_menu,
                icons=icones_menu,
                default_index=0,
            )

    # --- 5. LÓGICA DAS PÁGINAS ---

    # === PÁGINA: HOME ===
    if selected == "Home":
        st.title("Bem-vindo ao Sistema Nutri Pro")
        st.markdown("""
        Este é um sistema seguro e exclusivo para gestão de pacientes.
        
        Por favor, vá até o menu **Login** para acessar suas ferramentas.
        """)

    # === PÁGINA: LOGIN ===
    elif selected == "Login":
        st.title("🔐 Acesso Restrito")
        
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type='password')
        
        if st.button("Entrar"):
            # Verifica no banco de dados
            result = auth.login_user(username, password)
            
            if result:
                st.session_state['logado'] = True
                st.session_state['usuario'] = username
                # O banco retorna uma lista de tuplas. Pegamos a primeira [0].
                # Estrutura esperada: (username, password, role, force_change)
                st.session_state['role'] = result[0][2] 
                st.session_state['force_change'] = result[0][3]
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    # === PÁGINA: SAIR ===
    elif selected == "Sair":
        st.session_state.clear() # Limpa todas as variáveis da sessão
        st.rerun()

    # === PÁGINA: GERENCIAR USUÁRIOS (Só Admin vê) ===
   # === PÁGINA: GERENCIAR USUÁRIOS (Automação Completa) ===
    elif selected == "Gerenciar Usuários":
        st.title("⚙️ Gestão de Equipe")
        
        # Cria duas abas para organizar: uma de Cadastro e uma de Exclusão
        tab1, tab2 = st.tabs(["📝 Cadastrar Novo", "🗑️ Remover Usuário"])
        
        # --- ABA 1: CADASTRAR (O que já fizemos) ---
        with tab1:
            st.info("Cadastre um novo membro. A senha será enviada por e-mail.")
            with st.form("novo_usuario_form"):
                st.markdown("### Dados do Novo Usuário")
                col1, col2 = st.columns(2)
                with col1:
                    nome_real = st.text_input("Nome Completo")
                    new_user = st.text_input("Login de Acesso")
                with col2:
                    email_user = st.text_input("E-mail")
                    tipo_acesso = st.selectbox("Nível", ["user", "admin"])
                
                if st.form_submit_button("Gerar Acesso e Enviar E-mail 📧"):
                    if new_user and email_user:
                        senha_aleatoria = email_utils.gerar_senha_aleatoria()
                        try:
                            auth.add_userdata(new_user, auth.make_hashes(senha_aleatoria), role=tipo_acesso, force_change=1)
                            with st.spinner('Enviando e-mail...'):
                                sucesso, msg = email_utils.enviar_credenciais(nome_real, email_user, new_user, senha_aleatoria)
                            if sucesso:
                                st.success(f"✅ Usuário '{new_user}' criado e notificado!")
                            else:
                                st.warning(f"⚠️ Criado, mas erro no e-mail: {msg}. Senha: {senha_aleatoria}")
                        except Exception as e:
                            st.error(f"Erro: {e}")
                    else:
                        st.warning("Preencha Login e E-mail.")

        # --- ABA 2: EXCLUIR USUÁRIOS (Novidade!) ---
        with tab2:
            st.warning("⚠️ Cuidado: A exclusão é permanente e retira o acesso imediatamente.")
            
            # 1. Buscar todos os usuários no banco
            resultado_banco = auth.view_all_users()
            # resultado_banco vem assim: [('admin', 'admin'), ('joao', 'user')...]
            
            # 2. Criar um DataFrame para mostrar bonitinho na tela
            df_usuarios = pd.DataFrame(resultado_banco, columns=['Usuário', 'Função'])
            st.dataframe(df_usuarios, use_container_width=True)
            
            # 3. Criar uma lista só com os nomes para o menu de seleção
            lista_nomes = [i[0] for i in resultado_banco]
            
            st.markdown("---")
            col_del_1, col_del_2 = st.columns([3, 1])
            
            with col_del_1:
                usuario_para_deletar = st.selectbox("Selecione quem você quer remover:", lista_nomes)
            
            with col_del_2:
                st.write("") # Espaço vazio para alinhar o botão
                st.write("") 
                if st.button("🗑️ Excluir Acesso", type="primary"):
                    # TRAVA DE SEGURANÇA: Não deixar a Admin deletar a si mesma
                    if usuario_para_deletar == st.session_state['usuario']:
                        st.error("⛔ Você não pode excluir a si mesmo enquanto está logado!")
                    else:
                        auth.delete_user(usuario_para_deletar)
                        st.success(f"Usuário '{usuario_para_deletar}' removido com sucesso!")
                        st.rerun() # Atualiza a tela para sumir o nome da lista
    # === PÁGINA: INSERIR DADOS (Funcionalidade Original) ===
    elif selected == "Inserir Dados":
        st.title("📋 Cadastro de Paciente")
        
        with st.form("form_paciente"):
            nome = st.text_input("Nome do Paciente")
            idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
            peso = st.number_input("Peso (kg)", min_value=0.0, format="%.2f")
            altura = st.number_input("Altura (m)", min_value=0.0, format="%.2f")
            
            submit_paciente = st.form_submit_button("Salvar Registro")
            
            if submit_paciente:
                if nome and peso > 0 and altura > 0:
                    # 1. Calcular IMC
                    imc = peso / (altura ** 2)
                    
                    # 2. Preparar Dados
                    novo_dado = {
                        'Nome': [nome],
                        'Idade': [idade],
                        'Peso_kg': [peso],
                        'Altura_m': [altura],
                        'IMC': [round(imc, 2)],
                        'Data_Registro': [datetime.now()]
                    }
                    df_novo = pd.DataFrame(novo_dado)
                    
                    # 3. Salvar no CSV
                    if os.path.isfile(ARQUIVO_DADOS):
                        df_novo.to_csv(ARQUIVO_DADOS, mode='a', header=False, index=False)
                    else:
                        df_novo.to_csv(ARQUIVO_DADOS, mode='w', header=True, index=False)
                    
                    st.success(f"Paciente {nome} cadastrado com sucesso! IMC: {imc:.2f}")
                else:
                    st.warning("Por favor, preencha o nome, peso e altura corretamente.")

    # === PÁGINA: VISUALIZAR BASE (Funcionalidade Original) ===
    elif selected == "Visualizar Base":
        st.title("📂 Base de Dados (Power BI)")
        
        if os.path.exists(ARQUIVO_DADOS):
            df = pd.read_csv(ARQUIVO_DADOS)
            st.dataframe(df)
            
            st.download_button(
                label="Baixar CSV Atualizado",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name='dados_pacientes.csv',
                mime='text/csv',
            )
        else:
            st.warning("Nenhum dado encontrado. Cadastre o primeiro paciente na aba 'Inserir Dados'.")

if __name__ == '__main__':
    main()