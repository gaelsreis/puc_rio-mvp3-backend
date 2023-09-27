# Define a imagem base
FROM python:3.9

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos para o diretório de trabalho
COPY requisitos.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requisitos.txt

# Copia o código-fonte para o diretório de trabalho
COPY . .

# Define as variáveis de ambiente
ENV HOST 0.0.0.0
ENV PORT 5000

# Expõe a porta em que a API estará disponível
EXPOSE ${PORT}

# Define o comando de execução da API
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
#CMD ["uvicorn", "app:app", "--host", "${HOST}", "--port", "${PORT}"]