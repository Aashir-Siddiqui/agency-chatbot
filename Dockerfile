FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# CPU-only PyTorch pehle install karo — CUDA packages avoid karne ke liye
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Render free tier RAM/CPU limited hai — 1 worker rakha hai; ingest.py pehle vector store banata hai, phir server start hota hai
CMD sh -c "python ingest.py && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"