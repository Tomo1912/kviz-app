FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001

# OVO JE ISPRAVNA NAREDBA
# Govorimo Gunicornu: "U datoteci 'app' (.py), pozovi funkciju 'create_app()' da dobiješ aplikaciju."
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--log-level=debug", "--access-logfile=-", "--error-logfile=-", "app:create_app()"]
