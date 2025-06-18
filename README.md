# Sistema de Automação

Automação de tarefas nos sistemas iConsorcio e GovBR usando Python, Selenium e Streamlit.

Buscando poupar tempo durante a execução das minhas atividades no trabalho, criei esse pequeno sistema de automação que realiza o lançamento automático de consultas médicos no sistema iConsorcio, com base  em um arquivo .xls ou .xlsx emitido pelo sistema GovBR.

O meu sistema, a partir das informações inseridas nele, abre automaticamente o navegador Firefox e  realiza o lançamentos dessas consultas, desde a parte de logar no sistema até o último clique no botão "Salvar" para lançar as consultas realizadas pelos médicos.

(./img/telainicial.png)

(./img/aposadicionararquivo.png)

(./img/botaoiniciar.png)

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