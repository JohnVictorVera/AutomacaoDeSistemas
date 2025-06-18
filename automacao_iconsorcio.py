import pandas as pd
import streamlit as st
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import io

def login_iconsorcio(driver, usuario, senha):
    """Realiza login no sistema iConsorcio."""
    driver.get("https://limeira.nuvemsitcon.com.br/cismetro/frm_login.php")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "usuario"))).send_keys(usuario)
    senha_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "senha")))
    senha_input.send_keys(senha)
    senha_input.send_keys(Keys.ENTER)
    WebDriverWait(driver, 10).until(EC.url_contains("index.php"))

def preencher_informacoes_fixas_iconsorcio(driver, medico, fornecedor, procedimento, data_atendimento):
    """Preenche informações fixas no sistema iConsorcio."""
    driver.get("https://limeira.nuvemsitcon.com.br/cismetro/index.php?i=508")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profissionalID")))
    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "swal2-container")))

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "select2-fornecedor_id-container"))).click()
    fornecedor_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "select2-search__field")))
    fornecedor_input.send_keys(fornecedor)
    fornecedor_input.send_keys(Keys.ENTER)
    time.sleep(1)

    select = Select(driver.find_element(By.ID, "profissionalID"))
    select.select_by_visible_text(medico)
    time.sleep(1)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "procedimentoID"))).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//select[@id='procedimentoID']/option[contains(text(), '{procedimento}')]"))
    ).click()
    time.sleep(1)

    data_str = data_atendimento.strftime("%Y-%m-%d")
    data_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "date")))
    driver.execute_script(f"arguments[0].value = '{data_str}';", data_input)
    time.sleep(1)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Gerar Lista de Produção')]"))
    ).click()
    time.sleep(3)

def inserir_bloco_pacientes(driver, bloco_df, pacientes_nao_encontrados, medico, fornecedor, procedimento, data_atendimento):
    """Insere um bloco de pacientes no sistema iConsorcio."""
    paciente_inserido = False
    idx_df = 0
    campo_index = 0

    while campo_index < 20 and idx_df < len(bloco_df):
        row = bloco_df.iloc[idx_df]
        paciente = row["Paciente"]
        horario = row["Data Atendimento"].strftime("%H:%M")

        try:
            selects = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//select[@name='paciente_id[]']/following-sibling::span[contains(@class, 'select2')]"))
            )

            if campo_index >= len(selects):
                raise Exception("Campo de paciente não disponível.")

            paciente_container = selects[campo_index]
            driver.execute_script("arguments[0].scrollIntoView(true);", paciente_container)
            time.sleep(0.5)
            paciente_container.click()

            search_input = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@class='select2-search__field']"))
            )
            search_input.clear()
            search_input.send_keys(paciente)
            time.sleep(1)
            search_input.send_keys(Keys.ENTER)
            time.sleep(1)

            selects = driver.find_elements(By.XPATH, "//select[@name='paciente_id[]']/following-sibling::span[contains(@class, 'select2')]")
            nome_selecionado = selects[campo_index].text.strip()

            if not nome_selecionado or nome_selecionado == "Selecione o paciente" or paciente.lower() not in nome_selecionado.lower():
                st.warning(f"Paciente não encontrado: {paciente} - {horario} - {row['Data Atendimento'].strftime('%d/%m/%Y')}")
                pacientes_nao_encontrados.append({
                    "Paciente": paciente,
                    "Data Atendimento": row["Data Atendimento"],
                    "Horário": horario
                })

                try:
                    remover_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Remover Lançamento')]"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", remover_btn)
                    time.sleep(0.5)
                    remover_btn.click()
                    time.sleep(1)
                except Exception as e:
                    st.error(f"Erro ao tentar remover lançamento: {e}")

                if campo_index == 0:
                    st.info("Primeiro paciente não encontrado. Recarregando página e preenchendo dados fixos novamente.")
                    driver.refresh()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profissionalID")))
                    time.sleep(2)
                    preencher_informacoes_fixas_iconsorcio(driver, medico, fornecedor, procedimento, data_atendimento)
                    idx_df += 1
                    continue
                else:
                    if idx_df + 1 < len(bloco_df):
                        driver.find_element(By.CLASS_NAME, "add_item_btn").click()
                        time.sleep(1)
                    idx_df += 1
                    continue

            hora_inputs = driver.find_elements(By.NAME, "time[]")
            if campo_index >= len(hora_inputs):
                raise Exception("Campo de horário não disponível.")

            hora_input = hora_inputs[campo_index]
            hora_input.clear()
            hora_input.send_keys(horario)

            paciente_inserido = True
            campo_index += 1
            idx_df += 1

            if campo_index < 20 and idx_df < len(bloco_df):
                driver.find_element(By.CLASS_NAME, "add_item_btn").click()
                time.sleep(1)

        except Exception as e:
            st.error(f"Erro ao inserir paciente '{paciente}': {e}")
            pacientes_nao_encontrados.append({
                "Paciente": paciente,
                "Data Atendimento": row["Data Atendimento"],
                "Horário": horario
            })
            idx_df += 1

    return paciente_inserido

def salvar_pacientes_nao_encontrados(pacientes_nao_encontrados):
    """Salva pacientes não encontrados em arquivo para download."""
    if pacientes_nao_encontrados:
        df_nao_encontrados = pd.DataFrame(pacientes_nao_encontrados)
        st.session_state['pacientes_nao_encontrados_df'] = df_nao_encontrados

        st.warning(f"{len(df_nao_encontrados)} pacientes não encontrados.")
        buffer = io.BytesIO()
        df_nao_encontrados.to_csv(buffer, index=False)
        st.download_button(
            label="📄 Baixar lista de pacientes não encontrados",
            data=buffer.getvalue(),
            file_name="pacientes_nao_encontrados.csv",
            mime="text/csv"
        )

def executar_automacao_iconsorcio(df, usuario, senha, medico, fornecedor, procedimento, modo_continuo=False, iniciar_navegador_func=None, finalizar_func=None):
    """Executa a automação completa do iConsorcio."""
    pacientes_nao_encontrados = []
    if iniciar_navegador_func is None or finalizar_func is None:
        raise Exception("Funções de navegador não fornecidas.")
    driver = iniciar_navegador_func()
    if not driver:
        return

    try:
        login_iconsorcio(driver, usuario, senha)
        df["Data Atendimento"] = pd.to_datetime(df["Data Atendimento"])
        datas_unicas = df["Data Atendimento"].dt.date.unique()

        for data in datas_unicas:
            df_data = df[df["Data Atendimento"].dt.date == data]
            pacientes_restantes = df_data.copy()
            bloco_index = 0

            while not pacientes_restantes.empty:
                preencher_informacoes_fixas_iconsorcio(driver, medico, fornecedor, procedimento, data)

                bloco_df = pacientes_restantes.iloc[:20]
                paciente_inserido = inserir_bloco_pacientes(driver, bloco_df, pacientes_nao_encontrados, medico, fornecedor, procedimento, data)

                if paciente_inserido:
                    salvar_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'salvar') and contains(text(), 'Salvar')]"))
                    )
                    salvar_btn.click()

                    try:
                        ok_btn = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled"))
                        )
                        ok_btn.click()
                        st.info("Botão 'Ok' clicado. Recarregando a página para garantir continuidade...")
                        driver.refresh()
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "profissionalID")))
                        time.sleep(2)

                        st.info(f"Bloco de pacientes {bloco_index + 1} salvo para {data}.")
                        bloco_index += 1

                        pacientes_restantes = pacientes_restantes.iloc[20:]

                    except Exception as e:
                        st.warning("Botão 'Ok' não apareceu. Recarregando página.")
                        driver.refresh()
                        time.sleep(2)

                else:
                    st.warning(f"Nenhum paciente foi inserido no bloco {bloco_index + 1} ({data}).")
                    bloco_index += 1
                    pacientes_restantes = pacientes_restantes.iloc[20:]

            if not modo_continuo:
                break

        salvar_pacientes_nao_encontrados(pacientes_nao_encontrados)
        st.success("Automação concluída!")

    except Exception as e:
        st.error(f"Erro durante automação: {e}")
    finally:
        finalizar_func(driver)