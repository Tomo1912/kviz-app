# Knowledge quiz

## Description
Built a simple Quiz application using Python and Flask for development. Deployed on a Hetzner VPS using Docker, Nginx as a reverse proxy, and Certbot for HTTPS. The application is publicly available at https://kvizap.duckdns.org.

## Features
- **Answer Questions**: Accessible through a web interface
- **Public Availability**: Hosted at https://kvizap.duckdns.org with HTTPS.
- **Result Display**: Shows score at the end with option to restart

## Technologies
### Technology Stack
Backend: Python with Flask for web requests.
Frontend: HTML with Jinja2 for the user interface.
Containerization: Docker and docker-compose for service orchestration.
Web Server: Nginx as a reverse proxy with HTTPS support.
SSL: Certbot for Let's Encrypt certificates.
CI/CD: GitHub Actions with Playwright for automated testing.
Hosting: Hetzner Cloud VPS (CAX11, Specs: 2 vCPU, 4 GB RAM, 40 GB disk).



Domain: DuckDNS for free domain name.

## Project Setup from Scratch

### 1. Local Setup of the Application
#### 1.1. Project Creation
Created a project directory and set up a virtual environment:
```bash
mkdir kvizprojekt
cd kvizprojekt
python3 -m venv venv
source venv/bin/activate

pip install flask gunicorn
```

#### 1.2. Building the Application
Created **app.py**:
* Added a basic Flask application with quiz logic
* Code snippet:
```python
from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'super-secret-key'

questions = [
    {"question": "Glavni grad Hrvatske?", "options": ["Zagreb", "Split", "Rijeka"], "answer": "Zagreb"},
    {"question": "Najveći hrvatski otok?", "options": ["Krk", "Cres", "Hvar"], "answer": "Cres"},
    {"question": "Autor 'Pjesnika u nevolji'?", "options": ["Krleža", "Andrić", "Šenoa"], "answer": "Krleža"}
    {"question": "Koji je najviši vrh svijeta?", "options": ["Kilimanjaro", "Everest", "Mont Blanc"], "answer": "Everest"},
    {"question": "Tko je bio prvi predsjednik Hrvatske?", "options": ["Tuđman", "Mesić", "Josipović"], "answer": "Tuđman"},
    {"question": "Koji planet je poznat kao Crveni planet?", "options": ["Venera", "Mars", "Jupiter"], "answer": "Mars"},
    {"question": "U kojoj godini je počeo Drugi svjetski rat?", "options": ["1939", "1941", "1945"], "answer": "1939"},
    {"question": "Koji ocean je najveći na svijetu?", "options": ["Atlantski", "Tihi", "Indijski"], "answer": "Tihi"},
    {"question": "Tko je napisao 'Romeo i Julija'?", "options": ["Shakespeare", "Dante", "Goethe"], "answer": "Shakespeare"},
    {"question": "U kojem gradu su održane Olimpijske igre 2008.?", "options": ["Peking", "London", "Atina"], "answer": "Peking"}
]

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'questions' not in session:
        session['questions'] = random.sample(questions, 3)
        session['current'] = 0
        session['score'] = 0
    
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = session['questions'][session['current']]['answer']
        if user_answer == correct_answer:
            session['score'] += 1
        session['current'] += 1
        
        if session['current'] >= len(session['questions']):
            score = session['score']
            session.clear()
            return render_template('results.html', score=score, total=len(questions))
    
    if session['current'] < len(session['questions']):
        question = session['questions'][session['current']]
        return render_template('quiz.html', question=question, current=session['current'] + 1, total=len(session['questions']))
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
```

Created a **templates** directory for storing HTML templates:
```bash
mkdir templates
```

Created **index.html** for the web interface:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Kviz Znanja</title>
</head>
<body>
    <h1>Dobro došli u Kviz Znanja!</h1>
    <p>Testirajte svoje znanje kroz tri pitanja.</p>
    <a href="/quiz">Započni Kviz</a>
</body>
</html>
```

Created **quiz.html** for questions:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Kviz - Pitanje {{ current }}</title>
</head>
<body>
    <h1>Pitanje {{ current }} od {{ total }}</h1>
    <p>{{ question.question }}</p>
    <form method="post">
        {% for option in question.options %}
            <input type="radio" name="answer" value="{{ option }}" required> {{ option }}<br>
        {% endfor %}
        <button type="submit">Pošalji</button>
    </form>
</body>
</html>
```

Created **results.html** for results:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Rezultati Kviza</title>
</head>
<body>
    <h1>Vaš rezultat: {{ score }} od {{ total }}</h1>
    <p>Hvala na sudjelovanju!</p>
    <a href="/">Igraj ponovo</a>
</body>
</html>
```

#### 1.3. Creating **requirements.txt**
Generated requirements file for dependencies:
```bash
pip freeze > requirements.txt
```

Content of **requirements.txt**:
```
Flask==2.3.2
gunicorn==21.2.0
```

### 2. Pushing to GitHub
#### 2.1. Initializing Git Repository
Initialized Git and added project files:
```bash
git init
git add app.py templates/index.html templates/quiz.html templates/results.html requirements.txt Dockerfile
git commit -m "Initial Quiz App files"
```

#### 2.2. Creating a **Dockerfile**
Created a **Dockerfile** to containerize the application:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
```

Committed the Dockerfile:
```bash
git add Dockerfile
git commit -m "Add Dockerfile"
```
#### 2.2. Adding docker-compose.yml
Created docker-compose.yml to orchestrate kviz-app, nginx, and certbot services:
```bash
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5001:5001"
    volumes:
      - .:/app
    networks:
      - quiz-network
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certbot/conf:/etc/letsencrypt:ro
      - ./certbot/www:/var/www/certbot:ro
    depends_on:
      - app
    networks:
      - quiz-network
  certbot:
    image: certbot/certbot
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
    networks:
      - quiz-network
networks:
  quiz-network:
    driver: bridge
```
#### 2.3. Pushing to GitHub
```bash
git remote add origin https://github.com/Tomo1912/kviz-app.git
git branch -M main
git push -u origin main
```
#### 2.3 Committed docker-compose.yml:
```bash
git add docker-compose.yml
git commit -m "Add docker-compose.yml for kviz-app, nginx, and certbot services"
```
### 3. Deployment on Hetzner VPS
#### 3.1. Creating the VPS
Set up a **Hetzner CAX11** server with **Ubuntu 24.04**.

#### 3.2. Connecting to the VPS
Connected via SSH:
```bash
ssh root@37.27.8.233
```
#### 2.4 Configuring Nginx for HTTPS
Created nginx-certbot.conf for Certbot validation:
```bash
events {}

http {
    server {
        listen 80;
        server_name kvizap.duckdns.org;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 404;
        }
    }
}
```
Created nginx.conf for Nginx reverse proxy and HTTPS:
```bash
events {}

http {
    server {
        listen 80;
        server_name kvizap.duckdns.org;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 301 https://$host$request_uri;
        }
    }

    server {
        listen 443 ssl;
        server_name kvizap.duckdns.org;

        ssl_certificate /etc/letsencrypt/live/kvizap.duckdns.org/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/kvizap.duckdns.org/privkey.pem;

        location / {
            proxy_pass http://app:5001;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```
Committed Nginx configurations:
```bash
git add nginx-certbot.conf nginx.conf
git commit -m "Add nginx-certbot.conf for Certbot validation and nginx.conf for HTTPS"
```
#### 2.5 Setting up SSL with Certbot
Ran a temporary Nginx container for Certbot validation:
```bash
docker run -d --name temp-nginx -v $(pwd)/nginx-certbot.conf:/etc/nginx/nginx.conf:ro -v $(pwd)/certbot/www:/var/www/certbot:ro -p 80:80 nginx:latest
```
Obtained SSL certificates:
```bash
docker run --rm -v $(pwd)/certbot/conf:/etc/letsencrypt -v $(pwd)/certbot/www:/var/www/certbot certbot/certbot certonly --webroot --webroot-path=/var/www/certbot -d kvizap.duckdns.org --non-interactive --agree-tos --email maurs993@gmail.com
```

Stopped and removed temporary Nginx:
```bash
docker stop temp-nginx
docker rm temp-nginx
```
#### 2.6 Running with Docker compose
```bash
docker-compose up -d
```
#### 2.7 Pushing to GitHub
Initialized Git and pushed files:
```bash
git init
git add app.py templates/index.html templates/quiz.html templates/results.html requirements.txt Dockerfile docker-compose.yml nginx.conf nginx-certbot.conf
git commit -m "Initial Quiz App with HTTPS, Nginx, and docker-compose"
git remote add origin https://github.com/Tomo1912/kviz-app.git
git branch -M main
git push -u origin main
```
#### 3. Installing Required Tools
```bash
apt update
apt install -y git nginx
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

#### 3.1. Cloning the Repository
```bash
cd ~
git clone https://github.com/tvoj-username/kviz-app.git
cd kviz-app
```

#### 3.2. Running the App with Docker Compose
```bash
docker-compose up -d
```
