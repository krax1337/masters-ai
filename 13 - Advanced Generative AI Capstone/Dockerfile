FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1

RUN useradd -m -u 1000 user

USER user

WORKDIR /app

COPY . .

RUN uv sync --frozen

EXPOSE 7860

CMD ["uv", "run", "streamlit", "run", "main.py", "--server.port", "7860", "--server.address=0.0.0.0"]