# Imagem base do Python
FROM python:latest

# Copiar os arquivos do aplicativo para o contêiner
COPY ./app/ /app/

# Instalar as dependências do Python
WORKDIR /app
RUN pip install -r requirements.txt

# Executar o script Python
CMD [ "python", "main.py" ]
