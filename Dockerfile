# Estágio de build (para instalação de dependências)
FROM python:3.9-slim as builder

WORKDIR /app

# Instalar dependências de build se necessário
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiar apenas o necessário para instalar dependências
COPY requirements.txt .

# Criar ambiente virtual e instalar dependências
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Estágio final (imagem leve)
FROM python:3.9-slim

WORKDIR /app

# Copiar ambiente virtual do estágio builder
COPY --from=builder /opt/venv /opt/venv

# Garantir que scripts usem o ambiente virtual
ENV PATH="/opt/venv/bin:$PATH"

# Copiar aplicação
COPY . .

# Variáveis de ambiente (ajuste conforme necessário)
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=8000

# Expor porta
EXPOSE ${PORT}

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# Comando de execução (usando Gunicorn para produção)
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "--workers", "4", "app:app"]
