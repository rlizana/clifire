FROM python:3.8.2-slim

WORKDIR /app

COPY pyproject.toml README.md src ./

RUN sed -i 's/coverage = ">=7.9.1"/coverage = ">=6.0.0,<7.0.0"/' pyproject.toml

RUN pip install --upgrade pip && \
    pip install pytest "coverage<7.0.0" && \
    pip install -e .

CMD ["bash", "-c", "python -m pytest -v"]
