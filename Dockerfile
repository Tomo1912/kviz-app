FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001

# Gunicorn: Call create_app() function from app.py
# Security: Changed log-level from debug to info (less verbose in production)
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--log-level=info", "--access-logfile=-", "--error-logfile=-", "app:create_app()"]
