FROM python:3.11-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements/prod.txt .

RUN pip install -r prod.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]