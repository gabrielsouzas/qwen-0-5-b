import PyPDF2
import requests
import json

port = 11434
path = "livro_dos_espiritos_intro.pdf"


# Passo 2: Extrair Texto do PDF
# Agora, vamos criar uma função para extrair texto de um PDF usando a biblioteca PyPDF2:
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text


# Passo 3: Configurar a Comunicação com o Modelo Qwen-0.5B
# Para comunicar-se com o modelo Qwen-0.5B, vamos usar a biblioteca requests:
def send_message_to_qwen(context, message):
    url = "http://localhost:11434/api/generate"  # Substitua pelo URL correto do servidor do Qwen-0.5B
    payload = {
        "model": "qwen:0.5b",  # Substitua pelo modelo correto se necessário
        "prompt": f"{context}\n\n{message}",
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)

    # Imprimir a resposta bruta do servidor
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


# Passo 4: Criar a Interface do Chat
# Agora, vamos criar uma interface simples de linha de comando para o chat:


def chat_with_qwen(pdf_path):
    context = extract_text_from_pdf(pdf_path)
    print(
        "Contexto extraído do PDF:\n", context[:500], "..."
    )  # Mostra apenas os primeiros 500 caracteres do contexto

    while True:
        user_message = input("Você: ")
        if user_message.lower() in ["sair", "exit", "quit"]:
            break
        response = send_message_to_qwen(context, user_message)
        print("Qwen: ", response["response"])


if __name__ == "__main__":
    pdf_path = path
    chat_with_qwen(pdf_path)
