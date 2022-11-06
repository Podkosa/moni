FROM python:3.11 as base

COPY requirements.txt .

RUN pip install wheel && \
    pip wheel -r requirements.txt --wheel-dir=/wheels

FROM python:3.11-slim

COPY --from=base /wheels /wheels

WORKDIR /moni

COPY --from=base requirements.txt ./

RUN pip install -r requirements.txt --no-index --find-links=/wheels && \
    rm -rf /wheels

COPY src ./

CMD ["uvicorn", "bot:app", "--host", "0.0.0.0", "--port", "6767"]
