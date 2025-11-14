FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# isso aqui vai copiar o projeto inteiro para uma pasta app dentro do docker
ADD . /app 

# define que todos os comandos vão ser executados aqui (raiz)
WORKDIR /app

RUN uv sync --locked

EXPOSE 5000


CMD ["uv", "run", "python", "main.py"]
