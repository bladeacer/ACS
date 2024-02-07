from flask import Flask, render_template, request, url_for, redirect, jsonify
import shelve
import stripe
from Forms import *
from Feedback import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    feedback_form = FeedbackForm(request.form)
    if request.method == 'POST':
        email = feedback_form.email.data
        category = feedback_form.category.data
        rating = feedback_form.rating.data
        print(feedback_form.feedback_content.data)
        feedback_content = feedback_form.feedback_content.data

        with shelve.open('feedback_data') as shelf:
            feedback_id = str(len(shelf) + 1)
            shelf[feedback_id] = Feedback(email, category, rating, feedback_content)
            feedback_list = list(shelf.values())

        return render_template('feedback_success.html')

    return render_template('feedback.html', error=None, form=feedback_form)


@app.route('/feedback_confirmation', methods=['GET', 'POST'])
def feedback_confirmation():
    with shelve.open('feedback_data') as shelf:
        feedback_list = list(shelf.values())
    return render_template('feedback_confirmation.html', feedback_list=feedback_list)


@app.route('/quiz', methods=['POST', 'GET'])
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
    return redirect(url_for('retrieve_score'))


@app.route('/retrieve_quiz_score', methods=['POST', 'GET'])
def retrieve_score():
    with shelve.open('user.db') as user_db:
        quiz_dict = user_db.get('Quiz', {})
        sorted_quiz_dict = {k: v for k, v in sorted(quiz_dict.items(), key=lambda item: item[1], reverse=True)}
        return render_template('retrieve_quiz_score.html', quiz_dict=sorted_quiz_dict)


@app.route('/leaderboard', methods=['POST'])
def leaderboard():
    latest_timestamp = request.form.get('timestamp')
    with shelve.open('user.db') as user_db:
        quiz_dict = user_db.get('Quiz', {})
        sorted_quiz_dict = {k: v for k, v in sorted(quiz_dict.items(), key=lambda item: item[1], reverse=True)}
    return jsonify(sorted_quiz_dict)


stripe.api_key = "sk_test_51OV8RyGhcaAHTPePp4osOLsSuB42K5ubwCf5DFCPj6DIhz8CUDa8Jo93JWeOFw14Fg1njkLQU3WQkusO4KsfLt9X002JqriVHj"

YOUR_DOMAIN = "http://localhost:5000"

payment_data = shelve.open("payment_data")


@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    return render_template('checkout.html')


@app.route('/create_checkout_session', methods=['POST'])
def create_checkout_session():
    try:
        email = request.form.get('email')
        quantity_item_1 = int(request.form.get('quantity_item_1', 1))
        quantity_item_2 = int(request.form.get('quantity_item_2', 1))
        quantity_item_3 = int(request.form.get('quantity_item_3', 1))
        quantity_item_4 = int(request.form.get('quantity_item_4', 1))
        quantity_item_5 = int(request.form.get('quantity_item_5', 1))
        quantity_item_6 = int(request.form.get('quantity_item_6', 1))
        quantity_item_7 = int(request.form.get('quantity_item_7', 1))

        # Fetch prices from Stripe API for accurate calculations
        price_item_1 = stripe.Price.retrieve("price_1OWK0IGhcaAHTPePhJRZOFVC")
        price_item_2 = stripe.Price.retrieve("price_1OWJxfGhcaAHTPePFCp1LlLC")
        price_item_3 = stripe.Price.retrieve("price_1OWJusGhcaAHTPePEY2ioRN0")
        price_item_4 = stripe.Price.retrieve("price_1Og0xYGhcaAHTPeP5kZ3l00J")
        price_item_5 = stripe.Price.retrieve("price_1Og14OGhcaAHTPePnCY2Tu8p")
        price_item_6 = stripe.Price.retrieve("price_1Og1VJGhcaAHTPePiUCOomCx")
        price_item_7 = stripe.Price.retrieve("price_1Og1XxGhcaAHTPePq3bNIGjU")

        line_items = []
        if quantity_item_1 > 0:
            line_items.append({
                "price": price_item_1['id'],
                "quantity": quantity_item_1,
            })
        if quantity_item_2 > 0:
            line_items.append({
                "price": price_item_2['id'],
                "quantity": quantity_item_2,
            })
        if quantity_item_3 > 0:
            line_items.append({
                "price": price_item_3['id'],
                "quantity": quantity_item_3,
            })
        if quantity_item_4 > 0:
            line_items.append({
                "price": price_item_4['id'],
                "quantity": quantity_item_4,
            })
        if quantity_item_5 > 0:
            line_items.append({
                "price": price_item_5['id'],
                "quantity": quantity_item_5,
            })
        if quantity_item_6 > 0:
            line_items.append({
                "price": price_item_6['id'],
                "quantity": quantity_item_6,
            })
        if quantity_item_7 > 0:
            line_items.append({
                "price": price_item_7['id'],
                "quantity": quantity_item_7,
            })

        if len(line_items) == 0:
            return "No items selected", 400

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            customer_email=email,
            mode="payment",
            success_url=YOUR_DOMAIN + "/success",
            cancel_url=YOUR_DOMAIN + "/cancel",
        )

        final_amount = sum([price_item['unit_amount'] * line_item['quantity'] for price_item, line_item in zip(
            [price_item_1, price_item_2, price_item_3, price_item_4, price_item_5, price_item_6, price_item_7],
            line_items)])

        payment_data[checkout_session.id] = {
            "email": email,
            "amount_total": final_amount,
            "payment_status": "Successful",
        }
        payment_data.sync()
    except stripe.error.StripeError as e:
        return str(e), 500

    return redirect(checkout_session.url, code=303)


def get_payment_data(checkout_session_id):
    return payment_data.get(checkout_session_id)


@app.route('/success')
def success():
    all_payment_data = list(payment_data.values())
    return render_template('success.html', payment_data=all_payment_data)


@app.route('/payment_data')
def view_payment_data():
    all_payment_data = list(payment_data.values())
    return render_template('payment_data.html', payment_data=all_payment_data)


@app.route('/cancel')
def cancel():
    return render_template('checkout.html')


if __name__ == "__main__":
    with shelve.open('user.db') as user_database:
        if 'Quiz' not in user_database:
            user_database['Quiz'] = {}
    app.run(debug=True)

    payment_data.close()
