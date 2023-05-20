# Define a imagem base
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o contêiner
COPY . .

# Define o comando padrão a ser executado quando o contêiner for iniciado
CMD [ "python", "main.py" ]
