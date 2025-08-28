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

    medico_default = ""
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        if "Data Atendimento" in df.columns:
            df["Data Atendimento"] = pd.to_datetime(df["Data Atendimento"], errors='coerce')
            df = df.sort_values("Data Atendimento")
        if "Profissional" in df.columns and not df["Profissional"].dropna().empty:
            medico_default = str(df["Profissional"].dropna().iloc[0])

    usuario = st.text_input("Usuário do sistema iConsorcio")
    senha = st.text_input("Senha do sistema iConsorcio", type="password")

    st.subheader("Informações Fixas para Lançamento")
    medico = st.text_input("Nome do Médico (Nome completo)", value=medico_default)
    fornecedor = st.text_input("Fornecedor (Nome completo)")
    procedimento = st.selectbox("Procedimento (Descrição completa)", [
        "CONSULTA MEDICA EM ATENÇÃO ESPECIALIZADA - ESTRUTURA DO MUNICIPIO",
        "CONSULTA MEDICA EM ATENÇÃO ESPECIALIZADA - ESTRUTURA DO PRESTADOR",
        "CONSULTA MEDICA EM ATENÇÃO ESPECIALIZADA  NEUROLOGISTA/ NEUROCIRURGIA - ESTRUTURA DO MUNICIPIO",
        "EXCISAO DE LESAO E/OU SUTURA DE FERIMENTO DA PELE ANEXOS E MUCOSA",
        "EXERESE DE TUMOR DE PELE E ANEXOS / CISTO SEBACEO / LIPOMA",
        "BIOMETRIA ULTRASSÔNICA (MONOCULAR)",
        "PROVA DE FUNCÃO PULMONAR COMPLETA C/ BRONCODILATADOR (ESPIROMETRIA)"
    ])

    modo_continuo = st.checkbox("Executar todas as datas automaticamente")

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        if "Data Atendimento" in df.columns:
            df["Data Atendimento"] = pd.to_datetime(df["Data Atendimento"], errors='coerce')
            df = df.sort_values("Data Atendimento")
        if "Profissional" in df.columns and not df["Profissional"].dropna().empty:
            medico_default = str(df["Profissional"].dropna().iloc[0])

        st.success("Relatório carregado com sucesso!")
        st.dataframe(df[["Paciente", "Data Atendimento"]])

        # Mostrar tabela de atendimentos por dia
        if "Data Atendimento" in df.columns:
            atendimentos_por_dia = df.groupby(df["Data Atendimento"].dt.date)["Paciente"].count().reset_index()
            atendimentos_por_dia.columns = ["Data", "Total de Pacientes"]
            st.subheader("Total de pacientes atendidos por dia")
            st.dataframe(atendimentos_por_dia)

        if st.button("Iniciar Automação no iConsorcio"):
            if not all([usuario, senha, medico, fornecedor, procedimento]):
                st.error("Preencha todos os campos antes de iniciar a automação.")
            else:
                st.info("Iniciando automação...")
                executar_automacao_iconsorcio(
                    df, usuario.upper(), senha, medico, fornecedor.upper(), procedimento.upper(),
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
                    modo_continuo=True,
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