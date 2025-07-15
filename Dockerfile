FROM ubuntu:latest
ARG PYTHON_VERSION=3.8.2

RUN apt-get update && apt-get install -y \
        curl \
    && rm -rf /var/lib/apt/lists/*

ENV RYE_HOME="/root/.rye"
ENV RYE_INSTALL_OPTION="--yes"
ENV RYE_NO_AUTO_INSTALL="true"
RUN curl -sSf https://rye.astral.sh/get | bash
ENV PATH="/root/.rye/shims:${PATH}"

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY tests ./tests
COPY fire ./fire

RUN rye pin cpython@${PYTHON_VERSION} && \
    rye sync --all-features

CMD ["rye", "run", "fire", "tests"]
