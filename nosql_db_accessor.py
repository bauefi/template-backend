from google.cloud import datastore
import datetime

datastore_client = datastore.Client()

def create_new_customer(client_id, stripe_customer_id, payment_status):
    print("Function call: create_new_customer")
    new_customer = datastore.Entity(key=datastore_client.key('customers', stripe_customer_id))
    new_customer.update({
        'client_id': client_id,
        'stripe_customer_id': stripe_customer_id,
        'payment_status': payment_status
    })

    datastore_client.put(new_customer)

def update_customer_payment_status(stripe_customer_id, payment_status):
    print("Function call: update_customer_payment_status")
    customer = datastore.Entity(key=datastore_client.key('customers', stripe_customer_id))
    customer["payment_status"] = payment_status
    datastore_client.put(customer)

def get_all_customers():
    print("Function call: get_all_customers")
    query = datastore_client.query(kind='customers')
    customers = query.fetch()
    for c in customers:
        print(c)
    return "Success"
