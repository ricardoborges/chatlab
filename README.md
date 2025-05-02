# Guia de Instalação e Configuração

Este documento fornece instruções passo a passo para configurar o ambiente de desenvolvimento e executar a aplicação.

## Pré-requisitos

Antes de começar, certifique-se de que você tem todas as ferramentas necessárias instaladas no seu sistema.

## Passos para Instalação

### 1. Instalação e Execução do Ollama

O Ollama é necessário para fornecer capacidades de inferência de modelos.

1. Faça o download e instale o Ollama a partir de [https://ollama.com/](https://ollama.com/)
2. Inicie o serviço Ollama com o comando:
   ```bash
   ollama serve
   ```

### 2. Configuração do LLama-Stack

O LLama-Stack será utilizado para gerenciar nosso ambiente de inferência.

1. Instale o gerenciador de pacotes `uv`
2. Configure um ambiente virtual (venv)
3. Execute o seguinte comando dentro do ambiente virtual:
   ```bash
   INFERENCE_MODEL=gemma3:latest llama stack build --template ollama --image-type venv --run
   ```

### 3. Configuração do Projeto

Clone este repositório e instale as dependências necessárias:

1. Clone o repositório:
   ```bash
   git clone [https://github.com/ricardoborges/chatlab.git]
   cd [https://github.com/ricardoborges/chatlab.git]
   ```

2. Crie um ambiente virtual e instale as dependências:
   ```bash
   uv venv
   uv pip install -r myproject.toml
   ```

### 4. Execução da Aplicação

Inicie a aplicação Gradio com o seguinte comando:

```bash
gradio main.py
```

Após executar este comando, a interface da aplicação estará disponível no navegador.

## Resolução de Problemas

Se encontrar algum problema durante a instalação, verifique:
- Se o serviço Ollama está em execução
- Se o ambiente virtual foi ativado corretamente
- Se todas as dependências foram instaladas com sucesso

## Recursos Adicionais

Para mais informações sobre o LLama-Stack, consulte a [documentação oficial](https://llama-stack.readthedocs.io/en/latest/getting_started/index.html).