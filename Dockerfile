FROM python:3.12.10-slim-bullseye
LABEL image="flyrag-api"
WORKDIR /app
COPY ./common /app/common
COPY ./flyrag /app/flyrag
COPY ./prompt /app/prompt
COPY ./main.py /app
COPY ./pyproject.toml /app
COPY ./uv.lock /app
COPY docker/.env /app
RUN pip install uv
RUN uv sync
EXPOSE 8000
CMD ["/app/.venv/bin/python", "main.py"]