import streamlit as st
from gerador_sms import enviar_codigo_sms
from mongodb import inserir_aluno, inserir_aluno_menor

st.set_page_config(page_title="Sistema de Cadastro de Alunos", layout="centered")

menu = st.sidebar.selectbox(
    "Navegue",
    ["Início", "Verificação", "Cadastro"]
)

if menu == "Início":
    st.title("Sistema de Cadastro de Alunos")

elif menu == "Verificação":
    st.title("Verificação Via Código SMS")

    if "codigo_enviado" not in st.session_state:
        st.session_state.codigo_enviado = None
    if "verificado" not in st.session_state:
        st.session_state.verificado = False

    telefone = st.text_input("Digite o número de telefone (+55 DDD 99999 9999)")

    if st.button("Enviar código"):
        if telefone:
            enviar_codigo_sms(telefone)
        else:
            st.warning("Informe o número antes de enviar código.")

    if st.session_state.codigo_enviado:
        codigo_digitado = st.text_input("Digite o código")
        if st.button("Verificar código"):
            if codigo_digitado == str(st.session_state.codigo_enviado):
                st.session_state.verificado = True
                st.success("Verificado com sucesso!")
                st.balloons()
            else:
                st.error("Código incorreto.")

elif menu == "Cadastro":
    st.title("Cadastro de Alunos")

    if not st.session_state.get("verificado", False):
        st.warning("Você precisa realizar a verificação primeiro.")
        st.stop()

    st.subheader("Cadastrar Novo Aluno")

    idade_str = st.text_input("Qual a sua idade?")

    idade = None

    if idade_str:
        if idade_str.isdigit():
            idade_temp = int(idade_str)

            if 1 <= idade_temp <= 122:
                idade = idade_temp
            else:
                st.error("Idade inválida.")
        else:
            st.error("A idade deve conter apenas números.")

    if idade is None:
        st.info("Por favor, informe a idade para continuar com o cadastro.")
        st.stop()

    elif idade >= 18:
        st.info("Aluno maior de idade.")

        with st.form("aluno_maior"):
            nome = st.text_input("Nome Completo")
            telefone = st.text_input("Telefone")
            email = st.text_input("E-mail")
            cpf = st.text_input("CPF")
            salvar = st.form_submit_button("Cadastrar")

        if salvar:
            if nome and idade and telefone and email and cpf:
                inserir_aluno(nome, idade, telefone, email, cpf)
                st.success(f"Aluno {nome} cadastrado com sucesso!")
                st.balloons()
            else:
                st.warning("Preencha todos os campos!")

    else:
        st.info("Aluno menor de idade.")

        with st.form("aluno_menor"):
            nome = st.text_input("Nome do aluno")
            telefone = st.text_input("Telefone do aluno (opcional)")

            st.markdown("Dados do Responsável", unsafe_allow_html=False)
            responsavel = st.text_input("Nome do responsável")
            telefone_responsavel = st.text_input("Telefone do responsável")
            email_responsavel = st.text_input("E-mail do responsável")
            cpf_responsavel = st.text_input("CPF")
            salvar = st.form_submit_button("Cadastrar")

        if salvar:
            if nome and idade and responsavel and telefone_responsavel and email_responsavel and cpf_responsavel:
                inserir_aluno_menor(nome, idade, responsavel, telefone_responsavel, email_responsavel, cpf_responsavel)
                st.success(f"Aluno {nome} cadastrado com sucesso!")
                st.balloons()
            else:
                st.warning("Preencha todos os campos obrigatórios!")