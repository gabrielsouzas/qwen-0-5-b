import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, Trainer, TrainingArguments

# Carregar modelo e tokenizador
model_name = "qwen-0.5b"  # Supondo que exista um modelo com esse nome na Hugging Face
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

# Preparar o dataset (exemplo simplificado)
# Suponha que você tenha um conjunto de pares de perguntas e respostas sobre o texto
train_data = [
    {"context": "Texto do documento...", "question": "Qual é o tema principal?", "answer": "Tema principal..."},
    # Mais pares de perguntas e respostas
]

# Tokenização do dataset
def preprocess_data(data):
    return tokenizer(data['question'], data['context'], truncation=True, padding=True)

train_encodings = [preprocess_data(example) for example in train_data]

# Ajuste fino do modelo
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=2,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_encodings,
)

trainer.train()

# Inferência
def answer_question(question, context):
    inputs = tokenizer(question, context, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**inputs)
    answer_start = torch.argmax(outputs.start_logits)
    answer_end = torch.argmax(outputs.end_logits) + 1
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][answer_start:answer_end]))
    return answer

context = "Texto do documento..."
question = "Qual é o tema principal?"
print(answer_question(question, context))
