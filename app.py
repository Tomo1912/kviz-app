from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'super-secret-key-123'  # Za upravljanje sesijama

# Pitanja na hrvatskom
questions = [
    {"question": "Koji je glavni grad Hrvatske?", "options": ["Zagreb", "Split", "Rijeka", "Osijek"], "correct": "Zagreb"},
    {"question": "Koji je najveći otok u Hrvatskoj?", "options": ["Krk", "Cres", "Hvar", "Brač"], "correct": "Cres"},
    {"question": "Tko je autor 'Povratak Filipa Latinovicza'?", "options": ["Krleža", "Ujević", "Cesarić", "Tadijanović"], "correct": "Krleža"},
]

@app.route('/')
def index():
    session.pop('score', None)
    session.pop('answers', None)
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'answers' not in session:
        session['answers'] = []
        session['score'] = 0
        session['question_index'] = 0
        session['shuffled_questions'] = random.sample(questions, len(questions))

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        current_question = session['shuffled_questions'][session['question_index']]
        session['answers'].append({
            'question': current_question['question'],
            'user_answer': user_answer,
            'correct_answer': current_question['correct']
        })
        if user_answer == current_question['correct']:
            session['score'] += 1
        session['question_index'] += 1

    if session['question_index'] >= len(session['shuffled_questions']):
        score = session['score']
        answers = session['answers']
        session.pop('answers', None)
        session.pop('score', None)
        session.pop('question_index', None)
        session.pop('shuffled_questions', None)
        return render_template('results.html', score=score, total=len(questions), answers=answers)

    current_question = session['shuffled_questions'][session['question_index']]
    return render_template('quiz.html', question=current_question, index=session['question_index'] + 1, total=len(questions))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
