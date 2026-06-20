FROM python:3.10-slim

WORKDIR /app

# Eng kerakli Linux paketlarini yangilab olamiz
RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
