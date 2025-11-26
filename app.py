from flask import Flask, render_template, request, redirect, url_for, session
import random

# Globalna varijabla s pitanjima - ona može ostati vani.
questions = [
    {"question": "Glavni grad Hrvatske?", "options": ["Zagreb", "Split", "Rijeka"], "answer": "Zagreb"},
    {"question": "Najveći hrvatski otok?", "options": ["Krk", "Cres", "Hvar"], "answer": "Cres"},
    {"question": "Autor 'Pjesnika u nevolji'?", "options": ["Krleža", "Andrić", "Šenoa"], "answer": "Krleža"},
    {"question": "Koji je najviši vrh svijeta?", "options": ["Kilimanjaro", "Everest", "Mont Blanc"], "answer": "Everest"},
    {"question": "Tko je bio prvi predsjednik Hrvatske?", "options": ["Tuđman", "Mesić", "Josipović"], "answer": "Tuđman"},
    {"question": "Koji planet je poznat kao Crveni planet?", "options": ["Venera", "Mars", "Jupiter"], "answer": "Mars"},
    {"question": "U kojoj godini je počeo Drugi svjetski rat?", "options": ["1939", "1941", "1945"], "answer": "1939"},
    {"question": "Koji ocean je najveći na svijetu?", "options": ["Atlantski", "Tihi", "Indijski"], "answer": "Tihi"},
    {"question": "Tko je napisao 'Romeo i Julija'?", "options": ["Shakespeare", "Dante", "Goethe"], "answer": "Shakespeare"},
    {"question": "U kojem gradu su održane Olimpijske igre 2008.?", "options": ["Peking", "London", "Atina"], "answer": "Peking"}
]

def create_app():
    # Inicijalizacija aplikacije je sada unutar ove funkcije.
    app = Flask(__name__)
    app.secret_key = 'super-secret-key'

    # Sve rute su sada definirane unutar 'create_app' funkcije.
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
