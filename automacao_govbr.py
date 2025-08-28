import streamlit as st
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def preencher_datas_govbr(driver, data_inicio, data_fim):
    """Preenche datas no sistema GovBr."""
    try:
        data_inicio_str = data_inicio.strftime("%d/%m/%Y")
        data_fim_str = data_fim.strftime("%d/%m/%Y")

        icone_data_inicial = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "idde"))
        )
        icone_data_inicial.click()
        time.sleep(1)

        campo_data_inicial = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "iddd"))
        )
        campo_data_inicial.clear()
        campo_data_inicial.send_keys(data_inicio_str)
        campo_data_inicial.send_keys(Keys.ENTER)

        icone_data_final = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "ide0"))
        )
        icone_data_final.click()
        time.sleep(1)

        campo_data_final = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "iddf"))
        )
        campo_data_final.clear()
        campo_data_final.send_keys(data_fim_str)
        campo_data_final.send_keys(Keys.ENTER)

        st.success(f"Datas preenchidas: {data_inicio_str} a {data_fim_str}")

    except Exception as e:
        st.error(f"Erro ao preencher datas: {e}")

def executar_automacao_govbr(usuario, senha, lista_medicos, data_inicio, data_fim, iniciar_navegador_func=None, finalizar_func=None):
    """Executa a automação completa do GovBr."""
    url_relatorio = "https://leme.celk.com.br/unidadesaude/relatorio/relatorioRelacaoAtendimentos?5&cdPrg=193"
    if iniciar_navegador_func is None or finalizar_func is None:
        raise Exception("Funções de navegador não fornecidas.")
    driver = iniciar_navegador_func()
    if not driver:
        return

    try:
        driver.get("https://leme.celk.com.br")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login"))).send_keys(usuario)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "senha"))).send_keys(senha + Keys.ENTER)

        st.success("Login realizado com sucesso.")
        time.sleep(1)

        driver.get(url_relatorio)
        preencher_datas_govbr(driver, data_inicio, data_fim)

        for medico in lista_medicos:
            st.info(f"Gerando relatório para: {medico}")

            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "token-input-id3e")))
            input_medico = driver.find_element(By.ID, "token-input-id3e")

            input_medico.clear()
            input_medico.send_keys(medico)
            time.sleep(2)
            input_medico.send_keys(Keys.ENTER)
            time.sleep(2)

            if "token" not in driver.page_source:
                st.warning(f"Médico '{medico}' não foi reconhecido pelo sistema. Pulando...")
                continue

            botao_gerar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "id3d"))
            )
            botao_gerar.click()

            WebDriverWait(driver, 10).until(
                lambda d: "internalerror" not in d.page_source.lower()
            )
            time.sleep(3)

            st.success(f"Relatório para {medico} gerado.")

    except Exception as e:
        st.error(f"Erro durante automação GovBr: {e}")
    finally:
        finalizar_func(driver)