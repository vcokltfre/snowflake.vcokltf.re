FROM python:3.8

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml

RUN pip install poetry
RUN poetry install

COPY . /app

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]