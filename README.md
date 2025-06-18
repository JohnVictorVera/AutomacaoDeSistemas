# Sistema de Automação

Automação de tarefas nos sistemas iConsorcio e GovBr (futuramente) usando Python, Selenium e Streamlit.

## Estrutura

- `app.py`: Interface principal em Streamlit.
- `utils.py`: Funções utilitárias (iniciar/finalizar navegador).
- `automacao_iconsorcio.py`: Funções de automação para o iConsorcio.
- `automacao_govbr.py`: Funções de automação para o GovBr.

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/JohnVictorVera/Automacaoiconsorcio.git
   cd Automacaoiconsorcio
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Uso

Execute a interface web:
```
streamlit run app.py
```

Siga as instruções na tela para enviar os dados e iniciar a automação.

---

## ATENÇÃO

Módulo para automatizar a emissão de relatórios do GovBR ainda não terminado.