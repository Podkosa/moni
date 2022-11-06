FROM python:3.11

WORKDIR /moni

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src ./

CMD ["uvicorn", "bot:app", "--host", "0.0.0.0", "--port", "6767"]
