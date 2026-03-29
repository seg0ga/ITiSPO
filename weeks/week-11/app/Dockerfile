FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN useradd -m -u 1000 appuser

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN useradd -m test
USER test

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]