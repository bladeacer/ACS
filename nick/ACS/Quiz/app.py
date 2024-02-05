from flask import Flask, render_template, request, redirect, url_for
import shelve

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def quiz():
    return render_template('quiz.html')


@app.route('/process', methods=['POST'])
def process():
    user_id = 0
    data = request.form.get('data')
    result = data
    with shelve.open('user.db') as user_db:
        quiz_dict = user_db.get('Quiz', {})  # Use get to handle the case when 'Quiz' is not present
        user_id = len(quiz_dict) + 1
        quiz_dict[user_id] = result
        user_db['Quiz'] = quiz_dict
        print(quiz_dict)  # Print the dictionary contents here
    return redirect(url_for('retrieve_score'))


@app.route('/retrieve_quiz_score', methods=['POST', 'GET'])
def retrieve_score():
    with shelve.open('user.db') as user_db:
        quiz_dict = user_db.get('Quiz', {})  # Use get to handle the case when 'Quiz' is not present
        return render_template('retrieve_quiz_score.html', quiz_dict=quiz_dict)


if __name__ == "__main__":
    with shelve.open('user.db') as user_database:
        if 'Quiz' not in user_database:
            user_database['Quiz'] = {}
    app.run(debug=True)
