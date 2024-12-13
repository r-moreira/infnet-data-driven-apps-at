# INFNET 
## AT - Data Driven APPs
### Aluno: Rodrigo Moreira Avila

GIT: TODO

---
### Sobre o projeto:
Aplicação que implementa ReAct Agents com LangChain e Streamlit, além de um sistema WEB com LLM usando fastAPI para analisar dados de esporte.


### Estrutura do projeto:
```./README.md``` - Este arquivo.

```./src/*``` - Contém o código fonte da aplicação com a resolução de todos os exercícios.

```./requirements.txt``` - Contém as dependências do projeto.

```./images```- Contém os prints das aplicações em funcionamento.


### Como rodar o projeto:
1. Configurando versão do python:
```bash
pyenv local 3.11.9
```

2. Crie um ambiente virtual:
```bash
python -m venv .venv
```

3. Ative o ambiente virtual:
```bash
source .venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Execute a aplicação (Fast API):
```bash
# No diretório raiz do projeto
PYTHONPATH=./src ./.venv/bin/uvicorn src.api_app:app --reload 
```

6. Execute a aplicação (Streamlit):
```bash
# No diretório raiz do projeto
PYTHONPATH=./src ./.venv/bin/uvicorn src.api_app:app --reload
```