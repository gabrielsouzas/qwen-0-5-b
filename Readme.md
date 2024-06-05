# 📘 Projeto de Chat com Modelo Qwen-0.5B

Este projeto demonstra como extrair texto de um PDF e usar um modelo de linguagem Qwen-0.5B para criar uma interface de chat simples.

## 📜 Sumário

- [Instalação](#instalação)
- [Uso](#uso)
- [Passo a Passo](#passo-a-passo)
  - [1. Extração de Texto do PDF](#1-extração-de-texto-do-pdf)
  - [2. Configuração da Comunicação com o Modelo Qwen-05B](#2-configuração-da-comunicação-com-o-modelo-qwen-05b)
  - [3. Interface de Chat](#3-interface-de-chat)
- [Contribuição](#contribuição)
- [Licença](#licença)

## 🛠️ Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/gabrielsouzas/qwen-0-5-b.git
   ```
2. Navegue até o diretório do projeto:
   ```sh
   cd qwen-0-5-b
   ```
3. Crie um ambiente virtual e instale as dependências:
   ```sh
   python -m venv env
   source env/bin/activate  # No Windows use `env\Scripts\activate`
   pip install -r requirements.txt
   ```

## 📝 Uso

1. Coloque o arquivo PDF (`livro_dos_espiritos_intro.pdf`) no diretório do projeto.
2. Inicie o script:
   ```sh
   python chat_with_qwen.py
   ```
3. Digite suas perguntas no prompt de linha de comando. Digite `sair`, `exit` ou `quit` para encerrar o chat.

## 🧩 Passo a Passo

### 1. Extração de Texto do PDF

O script utiliza a biblioteca `PyPDF2` para extrair texto de um PDF. O texto extraído será usado como contexto para o chat.

```python
import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text
```

### 2. Configuração da Comunicação com o Modelo Qwen-0.5B

Para comunicar-se com o modelo Qwen-0.5B, o script utiliza a biblioteca `requests` para enviar uma solicitação HTTP POST para o servidor do modelo.

```python
import requests
import json

def send_message_to_qwen(context, message):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "qwen:0.5b",
        "prompt": f"{context}\n\n{message}",
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)

    print("Resposta bruta do servidor:", response.text)

    try:
        response_text = response.text.strip().split("\n")
        full_response = "".join(
            [json.loads(line)["response"] for line in response_text if line]
        )
        return {"response": full_response}
    except (requests.exceptions.JSONDecodeError, KeyError) as e:
        print("Erro ao processar a resposta:", e)
        return {"response": "Ocorreu um erro ao processar a resposta do servidor."}
```

### 3. Interface de Chat

A interface de chat permite que o usuário interaja com o modelo Qwen-0.5B, enviando mensagens e recebendo respostas.

```python
def chat_with_qwen(pdf_path):
    context = extract_text_from_pdf(pdf_path)
    print(
        "Contexto extraído do PDF:\n", context[:500], "..."
    )

    while True:
        user_message = input("Você: ")
        if user_message.lower() in ["sair", "exit", "quit"]:
            break
        response = send_message_to_qwen(context, user_message)
        print("Qwen: ", response["response"])


if __name__ == "__main__":
    pdf_path = "livro_dos_espiritos_intro.pdf"
    chat_with_qwen(pdf_path)

```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (git checkout -b feature/fooBar)
3. Commit suas mudanças (git commit -am 'Add some fooBar')
4. Push para a branch (git push origin feature/fooBar)
5. Crie um novo Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
