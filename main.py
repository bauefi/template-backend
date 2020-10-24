import os
import stripe
from flask_cors import CORS, cross_origin

import json

from flask import Flask, jsonify, request
# from flask import Flask, render_template, jsonify, request, send_from_directory, redirect
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = 'sk_test_51HeN8eH4w9X1EWMYc1gRVyPgI7Dm9j6wjAyEKPJMzBohyIk2Yu3v8NVpFUYAxw595JioVs8uf15rdu5F87Dqstna00HmgQhF30'

@app.route('/create-checkout-session', methods=['POST'])
@cross_origin()
def create_checkout_session():
  session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
      # Replace `price_...` with the actual price ID for your subscription
      # you created in step 2 of this guide.
      'price': 'price_1HeNI8H4w9X1EWMYAR1N08gE',
      'quantity': 1,
    }],
    client_reference_id= 'SomeTestIdThatINeedToReiveThroughTheWebHook',
    mode='subscription',
    success_url='http://localhost:3000/success',
    cancel_url='http://localhost:3000/',
  )

  return jsonify(id=session.id)

@app.route('/webhook', methods=['POST'])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    # webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    webhook_secret = 'whsec_phTbXiZIQeBOoyONRkEucUkmSaDIqzZn' # I copied this from the command line when pairing the CLI with my account
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

    print('event ' + event_type)

    # if event_type == 'checkout.session.completed':
    #     print('🔔 Payment succeeded!')

    # Add to the database the new customer
    if event_type == 'customer.created':
        print('A new customer was created')
        print(data_object)
        # Here I get the email
        email = data_object["email"]
        stripe_customer_id = ["id"] # This id is also in the customer.subscription.created message
        # put that into the firestore
    if event_type == 'customer.subscription.created':
        print('A new subscriptions was created!')
        print(data_object)


    # I guess I can get an id for the custoemr when the customer is created

    # Then when a new subscription is created I associate the two

    # Here I need the personse credentials or some identifier

    return jsonify({'status': 'success'})


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
