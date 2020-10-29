from google.cloud import datastore
import datetime
import logging

datastore_client = datastore.Client()

def create_new_customer(client_id, stripe_customer_id, payment_status):
    logging.info("Function call: create_new_customer")
    new_customer = datastore.Entity(key=datastore_client.key('customers', stripe_customer_id))

    new_customer.update({
        'client_id': client_id,
        'stripe_customer_id': stripe_customer_id,
        'payment_status': payment_status
    })

    datastore_client.put(new_customer)

def update_customer_payment_status(stripe_customer_id, payment_status):
    logging.info("Function call: update_customer_payment_status")
    # customer = datastore.Entity(key=datastore_client.key('customers', stripe_customer_id))
    # print(customer)
    # customer["payment_status"] = payment_status
    # print(customer)
    # datastore_client.put(customer)

    key = datastore_client.key('customers', stripe_customer_id)
    customer = client.get(key)

    customer["payment_status"] = payment_status

    client.put(task)


    pass

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
    customer = query.fetch(1) # returns iterator
    print(customer)
    return list(customer)
    # return next(customer)
    #return customer[0]
