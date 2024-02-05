from flask import Flask, redirect, render_template, request
import stripe
import shelve

app = Flask(__name__, static_url_path="", static_folder="payment")

stripe.api_key = "sk_test_51OV8RyGhcaAHTPePp4osOLsSuB42K5ubwCf5DFCPj6DIhz8CUDa8Jo93JWeOFw14Fg1njkLQU3WQkusO4KsfLt9X002JqriVHj"

YOUR_DOMAIN = "http://localhost:5000"

payment_data = shelve.open("payment_data")


@app.route('/create-checkout-session', methods=['POST'])
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
    return render_template('payment_data.html', payment_data=all_payment_data)


@app.route('/cancel')
def cancel():
    return render_template('cancel.html')


if __name__ == "__main__":
    app.run(port=5000, debug=True)

payment_data.close()