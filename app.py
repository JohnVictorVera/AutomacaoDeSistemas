import streamlit as st
import pandas as pd
from utils import iniciar_navegador, finalizar
from automacao_iconsorcio import (
    executar_automacao_iconsorcio,
    salvar_pacientes_nao_encontrados,
)
from automacao_govbr import executar_automacao_govbr

st.title("Sistema de Automação")

menu = st.radio("Escolha o sistema para automatizar:", ["Automação iConsorcio - Consultas", "Automação GovBr - Relatório"])

if menu == "Automação iConsorcio - Consultas":
    st.header("Automação de Lançamento - iConsorcio")

    uploaded_file = st.file_uploader("Faça upload do relatório do GovBR Saúde (.xls ou .xlsx)", type=["xls", "xlsx"])

    usuario = st.text_input("Usuário do sistema iConsorcio")
    senha = st.text_input("Senha do sistema iConsorcio", type="password")

    st.subheader("Informações Fixas para Lançamento")
    medico = st.text_input("Nome do Médico (Nome completo)")
    fornecedor = st.text_input("Fornecedor (Nome completo)")
    procedimento = st.text_input("Procedimento (Descrição completa)")

    modo_continuo = st.checkbox("Executar todas as datas automaticamente")

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.success("Relatório carregado com sucesso!")
        st.dataframe(df[["Paciente", "Data Atendimento"]])

        if st.button("Iniciar Automação no iConsorcio"):
            if not all([usuario, senha, medico, fornecedor, procedimento]):
                st.error("Preencha todos os campos antes de iniciar a automação.")
            else:
                st.info("Iniciando automação...")
                executar_automacao_iconsorcio(
                    df, usuario.upper(), senha, medico.upper(), fornecedor.upper(), procedimento.upper(),
                    modo_continuo=modo_continuo,
                    iniciar_navegador_func=iniciar_navegador,
                    finalizar_func=finalizar
                )

    if 'pacientes_nao_encontrados_df' in st.session_state:
        st.subheader("⚠️ Pacientes não encontrados")
        df_nao_encontrados = st.session_state['pacientes_nao_encontrados_df']
        st.dataframe(df_nao_encontrados)

        if st.button("🔁 Tentar lançar novamente pacientes não encontrados"):
            if not df_nao_encontrados.empty:
                st.info("Tentando lançar novamente...")
                executar_automacao_iconsorcio(
                    df_nao_encontrados, usuario, senha, medico, fornecedor, procedimento,
                    modo_continuo=False,
                    iniciar_navegador_func=iniciar_navegador,
                    finalizar_func=finalizar
                )
            else:
                st.warning("Não há pacientes não encontrados para tentar lançar novamente.")

elif menu == "Automação GovBr - Relatório":
    st.header("Automação de Relatórios - GovBr")

    usuario_govbr = st.text_input("Usuário GovBr")
    senha_govbr = st.text_input("Senha GovBr", type="password")
    arquivo_medicos = st.file_uploader("📤 Arquivo com nomes dos médicos (.xlsx)", type=["xlsx"])

    data_inicio = st.date_input("Data Inicial do Relatório")
    data_fim = st.date_input("Data Final do Relatório")

    lista_medicos = []

    if arquivo_medicos:
        df_medicos = pd.read_excel(arquivo_medicos)
        if "Médico" in df_medicos.columns:
            lista_medicos = df_medicos["Médico"].dropna().unique().tolist()
            st.success(f"{len(lista_medicos)} médicos carregados.")
            st.dataframe(df_medicos[["Médico"]])
        else:
            st.error("A coluna 'Médico' não foi encontrada no arquivo.")

    if st.button("Iniciar Automação GovBr"):
        if not all([usuario_govbr, senha_govbr, lista_medicos, data_inicio, data_fim]):
            st.error("Preencha todos os campos e carregue o arquivo corretamente.")
        else:
            st.info("Iniciando automação GovBr...")
            executar_automacao_govbr(
                usuario_govbr, senha_govbr, lista_medicos, data_inicio, data_fim,
                iniciar_navegador_func=iniciar_navegador,
                finalizar_func=finalizar
            )