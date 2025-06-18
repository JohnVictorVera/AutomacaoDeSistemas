from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import streamlit as st

def iniciar_navegador():
    """Inicia o navegador Firefox com as opções padrão."""
    options = webdriver.FirefoxOptions()
    options.add_argument("--start-maximized")
    try:
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        return driver
    except Exception as e:
        st.error(f"Erro ao iniciar o navegador: {e}")
        return None

def finalizar(driver):
    """Finaliza o navegador."""
    if driver:
        try:
            driver.quit()
        except Exception as e:
            st.error(f"Erro ao fechar o navegador: {e}")