# Sistema de Automação

Automação de tarefas nos sistemas iConsorcio e GovBR usando Python, Selenium e Streamlit.

Buscando poupar tempo durante a execução das minhas atividades no trabalho, criei esse pequeno sistema de automação que realiza o lançamento automático de consultas médicos no sistema iConsorcio, com base  em um arquivo .xls ou .xlsx emitido pelo sistema GovBR.

O meu sistema, a partir das informações inseridas nele, abre automaticamente o navegador Firefox e  realiza o lançamentos dessas consultas, desde a parte de logar no sistema até o último clique no botão "Salvar" para lançar as consultas realizadas pelos médicos, facilitando e acelerando a digitação do nome dos pacientes.

<div align="center">
   <img src="https://github.com/user-attachments/assets/f1b9bb7e-d7a9-4979-ba08-a4af288a1a2d" width = "700px"/>
   <img src="https://github.com/user-attachments/assets/60a2a20a-ee9b-4821-bef0-813ba524657a" width = "700px"/>
   <img src="https://github.com/user-attachments/assets/c937e900-b1c1-42a3-8816-f8a6929dc7b7" width = "700px"/>
</div>
Obs: Os nomes dos pacientes foram censurados.

## Estrutura

- `app.py`: Interface principal em Streamlit.
- `utils.py`: Funções utilitárias (iniciar/finalizar navegador).
- `automacao_iconsorcio.py`: Funções de automação para o iConsorcio.
- `automacao_govbr.py`: Funções de automação para o GovBr.

## Pré-requisitos

- Python 3.8 ou superior instalado ([download aqui](https://www.python.org/downloads/))
- Navegador Firefox instalado ([download aqui](https://www.mozilla.org/firefox/))

O driver do Firefox (geckodriver) será baixado automaticamente pelo sistema na primeira execução.

Se o navegador for bloqueado por firewall ou antivírus, permita a execução para que a automação funcione corretamente.

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

2. Execute a interface web:
   ```
   streamlit run app.py
   ```

Siga as instruções na tela para enviar os dados e iniciar a automação.

---

## ATENÇÃO

Módulo para automatizar a emissão de relatórios do GovBR ainda não terminado.
