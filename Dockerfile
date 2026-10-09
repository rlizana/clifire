FROM ubuntu:latest
ARG PYTHON_VERSION=3.8

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock README.md SKILL.md ./
COPY src ./src
COPY tests ./tests
COPY fire ./fire

ENV UV_PYTHON="${PYTHON_VERSION}"
ENV UV_PYTHON_DOWNLOADS=auto
RUN uv sync --frozen

CMD ["uv", "run", "fire", "tests"]
