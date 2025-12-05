import stripe
from rifas_ganns.settings import env

class Stripe:
    def __init__(self):
        self.stripe = stripe
        self.stripe.api_key = env("STRIPE_API_KEY")

    def create_customer(self, *args, **kwargs):
        return self.stripe.Customer.create(**kwargs)

    def create_product(self, *args, **kwargs):
        return self.stripe.Product.create(**kwargs)
    
    
