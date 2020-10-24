from google.cloud import datastore
import datetime

datastore_client = datastore.Client()

def create_new_customer(client_id, stripe_customer_id, payment_status):
    print("Function call: create_new_customer")
    entity = datastore.Entity(key=datastore_client.key('customers'))
    entity.update({
        'client_id': client_id,
        'stripe_customer_id': stripe_customer_id,
        'payment_status': payment_status
    })

    datastore_client.put(entity)

def get_all_customers():
    print("Function call: get_all_customers")
    query = datastore_client.query(kind='customers')
    customers = query.fetch()
    for c in customers:
        print(c)
    return "Success"
