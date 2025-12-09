import stripe
from rifas_ganns.settings import env
from .factory import auto_register
from .base import BaseGateway
from apps.configurations.models import GatewayRequiredCustomerFields

@auto_register("stripe")
class StripeGateway(BaseGateway):
    def __init__(self):
        self.stripe = stripe
        self.stripe.api_key = env("STRIPE_API_KEY")

    def create_customer(self, *args, **kwargs):
        fields = GatewayRequiredCustomerFields.objects.filter(gateway__name="stripe")
        data = {}
        for k, v in kwargs.items():
            if isinstance(v, list):
                if len(v) > 0:
                    v = v[0]
            for field in fields:
                if field.required_field_name == k:
                    data[k] = v
        customer = self.stripe.Customer.create(**data)
        return customer.id

    def create_product(self, *args, **kwargs):
        product = self.stripe.Product.create(**kwargs)
        return product.id
    
    
