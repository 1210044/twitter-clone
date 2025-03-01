# Первый этап: builder
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app

# # Устанавливаем зависимости с помощью uv
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Копируем остальные файлы приложения
COPY . /app

# Устанавливаем зависимости с помощью uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Второй этап: финальный образ
FROM python:3.12-slim-bookworm

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем установленные зависимости из предыдущего этапа
COPY --from=builder --chown=app:app /app /app

# Устанавливаем переменные окружения
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]