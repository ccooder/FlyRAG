FROM python:3.12.10-slim-bullseye
WORKDIR /app
COPY . /app
COPY docker/.env /app
RUN pip install uv
RUN uv sync
EXPOSE 8000
CMD ["/app/.venv/bin/python", "main.py"]