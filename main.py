import os
import stripe
from flask_cors import CORS, cross_origin

from flask import Flask, jsonify

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
    mode='subscription',
    success_url='http://localhost:3000/success',
    cancel_url='http://localhost:3000/',
  )
  print(session)
  return jsonify(id=session.id)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
