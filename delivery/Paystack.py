from django.conf import settings
import requests

class PayStack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url =  'https://api.paystack.co/'

    def verify_payment(self, ref, *args, **kwargs):
        path = ('transaction/verify/{ref}')

        headers = {
            'Authorization': f"Bearer {self.PAYSTACK_SECRET_KEY}",
            'Content-Type': 'application/json'
        }
        url = self.base_url + path
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            print(( response_data['data']['status'] == 'success', response_data['data']))
            return response_data['data']['status'] == 'success', response_data['data']

        response_data = response.json()
        return response_data['status'],  response_data['message']

    
    def generate_checkout_url(self, delivery, *args, **kwargs):
        path = ('transaction/initialize/')

        headers = {
            'Authorization': f"Bearer {self.PAYSTACK_SECRET_KEY}",
            'Content-Type': 'application/json'
        }

        url = self.base_url + path
        body = {
            'email': delivery.customer.account.email,
            'amount': delivery.get_delivery_amount() * 100,
            'reference': delivery.ref,
        }

        print(url)
        response = requests.post(url, headers=headers, json=body)

        return response.json().get('data').get('authorization_url')