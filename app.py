import streamlit as st
from gerador_sms import enviar_codigo_sms
from mongodb import inserir_aluno, inserir_aluno_menor
from check_data import check_data, Checks, in_check

st.set_page_config(page_title="Sistema de Cadastro de Alunos", layout="centered")

menu = st.sidebar.selectbox("Navegue", ["Início", "Verificação", "Cadastro"])

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
        checks = st.session_state.get("checks", [])

        st.info("Aluno maior de idade.")

        with st.form("aluno_maior"):
            nome = st.text_input("Nome Completo")

            if in_check(Checks.NOME, checks):
                st.warning("Nome inválido.")

            telefone = st.text_input("Telefone")

            if in_check(Checks.TELEFONE, checks):
                st.warning("Telefone inválido.")

            email = st.text_input("E-mail")

            if in_check(Checks.EMAIL, checks):
                st.warning("E-mail inválido.")

            cpf = st.text_input("CPF")

            if in_check(Checks.CPF, checks):
                st.warning("CPF inválido.")

            faixa_salarial = st.text_input("Faixa Salarial")

            if in_check(Checks.FAIXA_SALARIAL, checks):
                st.warning("Faixa Salarial deve ser um número positivo.")

            pessoas_familia = st.text_input("Pessoas na Familia")

            if in_check(Checks.PESSOAS_FAMILIA, checks):
                st.warning("Pessoas Familia deve ser uma quantidade.")

            etnia = st.selectbox(
                "Etnia",
                ("Selecione", "Amarelo", "Branco", "Indígena", "Pardo", "Preto"),
            )

            if in_check(Checks.ETNIA, checks):
                st.warning("Selecione uma etnia.")

            religião = st.text_input("Religião")

            if in_check(Checks.RELIGIÃO, checks):
                st.warning("Religião inválida.")

            salvar = st.form_submit_button("Cadastrar")

        if salvar:
            if (
                nome
                and idade
                and telefone
                and email
                and cpf
                and etnia
                and faixa_salarial
                and pessoas_familia
                and religião
            ):
                checks_aluno = check_data(
                    idade_str,
                    nome,
                    telefone,
                    email,
                    cpf,
                    etnia,
                    faixa_salarial,
                    pessoas_familia,
                    religião,
                )

                if checks_aluno == [Checks.OK]:
                    inserir_aluno(
                        nome,
                        idade,
                        telefone,
                        email,
                        cpf,
                        etnia,
                        faixa_salarial,
                        pessoas_familia,
                        religião
                    )
                    st.success(f"Aluno {nome} cadastrado com sucesso!")
                    st.balloons()
                else:
                    st.session_state.checks = checks_aluno
                    st.warning("Um ou mais campos foram preenchidos incorretamente!")
            else:
                st.warning("Preencha todos os campos!")

    else:
        checks_aluno = st.session_state.get("checks_aluno", [])
        checks_responsavel = st.session_state.get("checks_responsavel", [])

        print(checks_aluno)
        print(checks_responsavel)

        st.info("Aluno menor de idade.")

        with st.form("aluno_menor"):
            nome = st.text_input("Nome completo do aluno")

            if in_check(Checks.NOME, checks_aluno):
                st.warning("Nome inválido.")

            etnia = st.selectbox(
                "Etnia",
                ("Selecione", "Amarelo", "Branco", "Indígena", "Pardo", "Preto"),
            )

            if in_check(Checks.ETNIA, checks_aluno):
                st.warning("Selecione uma etnia.")

            st.markdown("Dados do Responsável", unsafe_allow_html=False)
            responsavel = st.text_input("Nome do responsável")

            if in_check(Checks.NOME, checks_responsavel):
                st.warning("Nome inválido.")

            telefone_responsavel = st.text_input("Telefone do responsável")

            if in_check(Checks.TELEFONE, checks_responsavel):
                st.warning("Telefone inválido.")

            email_responsavel = st.text_input("E-mail do responsável")

            if in_check(Checks.EMAIL, checks_responsavel):
                st.warning("E-mail inválido.")

            cpf_responsavel = st.text_input("CPF")

            if in_check(Checks.NOME, checks_responsavel):
                st.warning("CPF inválido.")

            faixa_salarial = st.text_input("Faixa Salarial")

            if in_check(Checks.FAIXA_SALARIAL, checks_responsavel):
                st.warning("Faixa Salarial deve ser um número positivo.")

            pessoas_familia = st.text_input("Pessoas na Familia")

            if in_check(Checks.PESSOAS_FAMILIA, checks_responsavel):
                st.warning("Pessoas Familia deve ser uma quantidade.")

            religião = st.text_input("Religião")

            if in_check(Checks.RELIGIÃO, checks_responsavel):
                st.warning("Religião inválida.")

            salvar = st.form_submit_button("Cadastrar")

        if salvar:
            if (
                nome
                and etnia
                and idade
                and responsavel
                and telefone_responsavel
                and email_responsavel
                and cpf_responsavel
            ):
                checks_aluno = check_data(idade=idade_str, nome=nome, etnia=etnia)

                checks_responsavel = check_data(
                    nome=responsavel,
                    telefone=telefone_responsavel,
                    email=email_responsavel,
                    cpf=cpf_responsavel,
                    faixa_salarial=faixa_salarial,
                    pessoas_familia=pessoas_familia,
                    religião=religião,
                )

                if checks_aluno == [Checks.OK] and checks_responsavel == [Checks.OK]:
                    inserir_aluno_menor(
                        nome,
                        etnia,
                        idade,
                        responsavel,
                        telefone_responsavel,
                        email_responsavel,
                        cpf_responsavel,
                        faixa_salarial,
                        pessoas_familia,
                        religião
                    )
                    st.success(f"Aluno {nome} cadastrado com sucesso!")
                    st.balloons()
                else:
                    st.session_state["checks_aluno"] = checks_aluno
                    st.session_state["checks_responsavel"] = checks_responsavel
                    st.warning("Um ou mais campos foram preenchidos incorretamente!")
            else:
                st.warning("Preencha todos os campos obrigatórios!")