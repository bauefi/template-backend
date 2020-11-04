from google.cloud import datastore
import datetime
import logging

datastore_client = datastore.Client()

def create_new_subscription(client_id, stripe_customer_id, stripe_subscription_id, payment_status):
    logging.info("Function call: create_new_subscription")
    new_customer = datastore.Entity(key=datastore_client.key('subscription', stripe_subscription_id))

    new_customer.update({
        'client_id': client_id,
        'stripe_customer_id': stripe_customer_id,
        'payment_status': payment_status
    })

    datastore_client.put(new_customer)

def update_subscription_payment_status(stripe_subscription_id, payment_status):
    logging.info("Function call: update_subscription_payment_status")
    key = datastore_client.key('subscription', stripe_subscription_id)
    subscription = datastore_client.get(key)
    subscription["payment_status"] = payment_status
    datastore_client.put(subscription)

def get_all_customers():
    logging.info("Function call: get_all_customers")
    query = datastore_client.query(kind='customers')
    customers = query.fetch()
    for c in customers:
        print(c)
    return "Success"

# def get_user_by_client_reference_id(client_reference_id):
#     logging.info("Function call: get_user_payment_status")
#     query = datastore_client.query(kind='customers')
#     query.add_filter('client_id', '=', client_reference_id)
#     customers = list(query.fetch(1)) # query fetch returns iterator
#     assert len(customers) < 2 # Either empty or one otherwise throw execption
#     if len(customers):
#         return customers[0]
#     else:
#         return None

def get_subscription_by_client_reference_id(client_reference_id):
    logging.info("Function call: get_subscription_by_client_reference_id")
    query = datastore_client.query(kind='subscription')
    query.add_filter('client_id', '=', client_reference_id)
    customers = list(query.fetch(1)) # query fetch returns iterator
    assert len(customers) < 2 # Either empty or one otherwise throw execption
    if len(customers):
        return customers[0]
    else:
        return None

def delete_subscription(stripe_subscription_id):
    logging.info("Function call: delete_subscription")
    key = datastore_client.key('subscription', stripe_subscription_id)
    datastore_client.delete(key)
