# Sistema de Automação

Automação de tarefas nos sistemas iConsorcio e GovBR usando Python, Selenium e Streamlit.

Buscando poupar tempo durante a execução das minhas atividades no trabalho, criei esse pequeno sistema de automação que realiza o lançamento automático de consultas médicos no sistema iConsorcio, com base  em um arquivo .xls ou .xlsx emitido pelo sistema GovBR.

O meu sistema, a partir das informações inseridas nele, abre automaticamente o navegador Firefox e  realiza o lançamentos dessas consultas, desde a parte de logar no sistema até o último clique no botão "Salvar" para lançar as consultas realizadas pelos médicos.

![tela1](https://private-user-images.githubusercontent.com/203187817/456685376-412cff5e-001e-4f88-b633-9d0c27030360.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyNzYzMjUsIm5iZiI6MTc1MDI3NjAyNSwicGF0aCI6Ii8yMDMxODc4MTcvNDU2Njg1Mzc2LTQxMmNmZjVlLTAwMWUtNGY4OC1iNjMzLTlkMGMyNzAzMDM2MC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQxOTQ3MDVaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05YjNjMzA4NTQyMjY5ZTc2MDBhY2FkZjlmNjJjODg0NThmMzViNTEyMmU2NDAyOTllY2M1OGJiNWQxNWNhNGM0JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.-BphZvwnJ3OvJjHfHbs5dumajcxjKdPT_1W2Qd9blqc)
![tela2](https://private-user-images.githubusercontent.com/203187817/456685378-a2586bf7-8a24-4445-b680-8efc7dcd17c1.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyNzYzMjUsIm5iZiI6MTc1MDI3NjAyNSwicGF0aCI6Ii8yMDMxODc4MTcvNDU2Njg1Mzc4LWEyNTg2YmY3LThhMjQtNDQ0NS1iNjgwLThlZmM3ZGNkMTdjMS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQxOTQ3MDVaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT02MThkOTNhYTU5NDkxYTQxMTU2ZjVhY2FjMjFmMGU4NjAwZTRkMmIyMjQ3OGUwN2Y4YzUzOTg4ZTRiNTVkYWFhJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.jd8q9l48iogUbTJP9Jmc_aKBdywcOHI8YKbq_cXLCA0)
![tela3](https://private-user-images.githubusercontent.com/203187817/456685810-75c58848-f912-4c81-8a6d-38d0e9e7b1e2.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTAyNzYzMjUsIm5iZiI6MTc1MDI3NjAyNSwicGF0aCI6Ii8yMDMxODc4MTcvNDU2Njg1ODEwLTc1YzU4ODQ4LWY5MTItNGM4MS04YTZkLTM4ZDBlOWU3YjFlMi5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwNjE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDYxOFQxOTQ3MDVaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0yNDdhNjRhOGQ1MDhjZTdiYWFhZmY1ZjQxZDRkNjI2NzQyN2NjZDk0ZWUyOTlhNGZkYWE3NTdmYjI0ZTU2OWE2JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.5y1GfVVSCmesL3K0wyzSrmLKm92rijJpCqtLgJn0Ibg)

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
