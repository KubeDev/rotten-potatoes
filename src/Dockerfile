FROM python:3.8

LABEL mantainer="Deyvisson Eduardo deyvissoneduardo22@gmail.com"

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--workers=1", "--bind", "0.0.0.0:5000", "app:app"]