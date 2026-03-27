FROM python:3.11-slim AS builder
WORKDIR /app
COPY starter/requirements.txt .
RUN pip install --prefix=/install -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY starter/main.py starter/schemas.py ./
EXPOSE 8197
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8197"]
