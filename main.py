import os
import stripe
import json
import datetime
import logging
from flask_cors import CORS, cross_origin

from flask import Flask, jsonify, request

from nosql_db_accessor import (
    get_all_customers,
    get_subscription_by_client_reference_id,
    update_subscription_payment_status,
    create_new_subscription,
    delete_subscription
)

# from flask import Flask, render_template, jsonify, request, send_from_directory, redirect
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = 'sk_test_51HeN8eH4w9X1EWMYc1gRVyPgI7Dm9j6wjAyEKPJMzBohyIk2Yu3v8NVpFUYAxw595JioVs8uf15rdu5F87Dqstna00HmgQhF30'

@app.route('/')
def root():
    # Store the current access time in Datastore.
    #store_time(datetime.datetime.now())

    # Fetch the most recent 10 access times from Datastore.
    return get_all_customers()

"""
############ Stripe #############
"""
@app.route('/get-payment-status', methods=['GET'])
@cross_origin()
def get_payment_status():
    try:
        client_reference_id = request.args.get('client_reference_id')
        subscription =  get_subscription_by_client_reference_id(client_reference_id)
        payment_status = "UNPAID"
        if subscription:
            payment_status = subscription["payment_status"]
        return jsonify({'uid': client_reference_id, 'payment_status': payment_status})
    except:
        logging.exception("message")
        return jsonify({'status': 'failure'}), 400

@app.route('/create-checkout-session', methods=['POST'])
@cross_origin()
def create_checkout_session():
    try:
        request_data = json.loads(request.data)
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_1HeNI8H4w9X1EWMYAR1N08gE',
                'quantity': 1,
            }],
            client_reference_id = request_data["client_reference_id"],
            customer_email = request_data["email"],
            mode='subscription',
            success_url='http://localhost:3000/success',
            cancel_url='http://localhost:3000/',
        )

        return jsonify(id=session.id)
    except:
        logging.exception("message")
        return jsonify({'status': 'failure'}), 400

@app.route('/cancel-subscription', methods=['POST'])
@cross_origin()
def cancel_subscription():
    try:
        request_data = json.loads(request.data)

        # 1. Need to fetch the customer id from database
        subscription = get_subscription_by_client_reference_id(request_data["client_reference_id"])

        # 2. Delete the subscription
        result = stripe.Subscription.delete(subscription.key.path[0]["name"])
        assert result["status"] == "canceled"

        return jsonify({'status': 'success'}), 200
    except:
        logging.exception("message")
        return jsonify({'status': 'failure'}), 400

@app.route('/webhook', methods=['POST'])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    # webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    webhook_secret = 'whsec_phTbXiZIQeBOoyONRkEucUkmSaDIqzZn' # I copied this from the command line when pairing the CLI with my account

    try:
        request_data = json.loads(request.data)

        if webhook_secret:
            # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
            signature = request.headers.get('stripe-signature')
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.data, sig_header=signature, secret=webhook_secret)
                data = event['data']
            except Exception as e:
                return e
            # Get the type of webhook event sent - used to check the status of PaymentIntents.
            event_type = event['type']
        else:
            data = request_data['data']
            event_type = request_data['type']
        data_object = data['object']

        if event_type == 'checkout.session.completed':
            logging.info('Event: checkout.session.completed')
            client_id = data_object["client_reference_id"]
            customer_stripe_id = data_object["customer"]
            subscription_stripe_id = data_object["subscription"]
            payment_status = data_object["payment_status"]
            create_new_subscription(client_id, customer_stripe_id, subscription_stripe_id, payment_status)
        elif event_type == 'invoice.paid':
            logging.info('Event: invoice.paid')
            stripe_subscription_id = data_object["subscription"]
            update_subscription_payment_status(stripe_subscription_id, 'paid')
        elif event_type == 'invoice.payment_failed':
            logging.info('Event: invoice.payment_failed')
            stripe_subscription_id = data_object["subscription"]
            update_subscription_payment_status(stripe_subscription_id, 'UNPAID')
        elif event_type == 'customer.subscription.deleted':
            logging.info('Event: customer.subscription.deleted')
            stripe_subscription_id = data_object["id"]
            delete_subscription(stripe_subscription_id)

        return jsonify({'status': 'success'})

    except:
        logging.exception("message")
        return jsonify({'status': 'failure'}), 400



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
