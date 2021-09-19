FROM python:3.8-slim-buster
EXPOSE 5000
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
WORKDIR /app
COPY . /app
CMD ["gunicorn", "--workers=3", "--bind", "0.0.0.0:5000", "app:app"]
