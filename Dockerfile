FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY data/ data/

RUN python src/analyze_all.py

CMD ["python", "src/analyze_all.py"]
