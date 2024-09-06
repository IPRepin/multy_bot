FROM python:3.11-alpine
WORKDIR /multy_bot
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt

COPY . .
CMD ["python", "bot.py"]