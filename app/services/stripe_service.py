import os
from stripe import StripeClient

def stripe_query(email):
    """Get stripe customer and related subscriptions"""
    client = StripeClient(os.getenv('STRIPE_KEY'))
    customers = client.customers.list({'email': email})
    
    if customers.data:
        subscriptions = client.subscriptions.list({'customer': customers.data[0].id}) 
        return {"response": {
            "customer_id": customers.data[0].id,
            "created": customers.data[0].created,
            "subscriptions": subscriptions.data
        }}
    return {"response": "No customer found."}

def stripe_cancel(subscription_id):
    """Cancel a subscription"""
    client = StripeClient(os.getenv('STRIPE_KEY'))
    subscription = client.subscriptions.cancel(
        subscription_exposed_id=subscription_id,
        params={'prorate': True}
    )
    
    if subscription.status == 'canceled':
        return {"response": {"status": f"{subscription.status} at {subscription.canceled_at}"}}
    return {"response": "No results found."}

def stripe_payments_list(customer_id):
    """List payments from a customer id"""
    client = StripeClient(os.getenv('STRIPE_KEY'))
    charges = client.charges.list(params={'customer': customer_id})
    if charges:
        return {"response": {"payments": charges}}
    return {"response": "No payments found."}

def stripe_refund(charge_id):
    """Refund a charge with charge id"""
    client = StripeClient(os.getenv('STRIPE_KEY'))
    refund = client.refunds.create(params={'charge': charge_id})
    if refund:
        return {"response": {"refund": refund}}
    return {"response": "Can't refund."}
