from flask import Flask, render_template, request, redirect, url_for, session
import random
from datetime import timedelta

import json
import os

def load_questions():
    file_path = os.path.join(os.path.dirname(__file__), 'questions.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

questions = load_questions()

def create_app():
    # Inicijalizacija aplikacije je sada unutar ove funkcije.
    app = Flask(__name__)

    # Security: Use environment variable for secret key, fallback to random for dev
    app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

    # Security: Session expires after 30 minutes of inactivity
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookie over HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection

    # Sve rute su sada definirane unutar 'create_app' funkcije.
    @app.route('/')
    def index():
        session.clear()
        return render_template('index.html')

    @app.route('/quiz', methods=['GET', 'POST'])
    def quiz():
        if 'questions' not in session:
            session['questions'] = random.sample(questions, 10)
            session['current'] = 0
            session['score'] = 0
            session['answers'] = []  # Lista za pohranu odgovora
        
        if request.method == 'POST':
            user_answer = request.form.get('answer')
            correct_answer = session['questions'][session['current']]['answer']
            question_text = session['questions'][session['current']]['question']
            
            # Pohrani odgovor
            session['answers'].append({
                'question': question_text,
                'user_answer': user_answer,
                'correct_answer': correct_answer
            })
            
            # Provjeri točnost i ažuriraj rezultat
            if user_answer == correct_answer:
                session['score'] += 1
            session['current'] += 1
            
            # Ako su sva pitanja odgovorena
            if session['current'] >= len(session['questions']):
                score = session['score']
                answers = session['answers']
                session.clear()
                return render_template('results.html', score=score, total=len(answers), answers=answers)
        
        if session['current'] < len(session['questions']):
            question = session['questions'][session['current']]
            return render_template('quiz.html', question=question, current=session['current'] + 1, total=len(session['questions']))
        
        return redirect(url_for('index'))

    # Na kraju, funkcija mora vratiti 'app' objekt.
    return app

# Ovaj dio se više ne koristi jer Gunicorn i Flask CLI imaju svoje načine pokretanja servera.
# if __name__ == '__main__':
#     app = create_app()
#     app.run(host='0.0.0.0', port=5001)
