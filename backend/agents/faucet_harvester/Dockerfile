FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY agent.py .
COPY log.txt .

EXPOSE 8080

CMD ["python", "agent.py"]