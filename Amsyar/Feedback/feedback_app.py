from flask import Flask, render_template, request
import shelve
from Forms import *
from Feedback import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def feedback():
    feedback_form = FeedbackForm(request.form)
    if request.method == 'POST':
        email = feedback_form.email.data
        category = feedback_form.category.data
        rating = feedback_form.rating.data
        print(feedback_form.feedback_content.data)
        feedback_content = feedback_form.feedback_content.data

        # Validate the form data (add more validation as needed)
        # if not email or not category or not rating or not feedback:
        #     return render_template('feedback.html', error='Please fill in all fields.')

        # Save the feedback to the shelf
        with shelve.open('feedback_data') as shelf:
            feedback_id = str(len(shelf) + 1)
            shelf[feedback_id] = Feedback(email, category, rating, feedback_content)
            feedback_list = list(shelf.values())

        return render_template('feedback_confirmation.html', feedback_list=feedback_list)

    return render_template('feedback.html', error=None, form=feedback_form)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
