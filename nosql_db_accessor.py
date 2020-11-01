from google.cloud import datastore
import datetime
import logging

datastore_client = datastore.Client()

def create_new_customer(client_id, stripe_customer_id, payment_status):
    logging.info("Function call: create_new_customer")
    new_customer = datastore.Entity(key=datastore_client.key('customers', stripe_customer_id))

    new_customer.update({
        'client_id': client_id,
        'payment_status': payment_status
    })

    datastore_client.put(new_customer)

def update_customer_payment_status(stripe_customer_id, payment_status):
    logging.info("Function call: update_customer_payment_status")
    key = datastore_client.key('customers', stripe_customer_id)
    customer = datastore_client.get(key)
    customer["payment_status"] = payment_status
    client.put(task)

def get_all_customers():
    logging.info("Function call: get_all_customers")
    query = datastore_client.query(kind='customers')
    customers = query.fetch()
    for c in customers:
        print(c)
    return "Success"

def get_user_by_client_reference_id(client_reference_id):
    logging.info("Function call: get_user_payment_status")
    query = datastore_client.query(kind='customers')
    query.add_filter('client_id', '=', client_reference_id)
    customers = list(query.fetch(1)) # query fetch returns iterator
    assert len(customers) < 2 # Either empty or one otherwise throw execption
    if len(customers):
        return customers[0]
    else:
        return None
