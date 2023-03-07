from django.conf import settings
import requests

class PayStack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url =  'https://api.paystack.co/'
    headers = {
            'Authorization': f"Bearer {PAYSTACK_SECRET_KEY}",
            'Content-Type': 'application/json'
        }
    
    def get_url(self, path):
        return self.base_url + path
    
    def verify_payment(self, ref, *args, **kwargs):
        path = (f'transaction/verify/{ref}')

        
        url = self.base_url + path
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['data']['status'] == 'success', response_data['data']

        
        response_data = response.json()
        return response_data['status'],  response_data['message']

    
    def generate_checkout_url(self, delivery, *args, **kwargs):
        path = ('transaction/initialize/')

        url = self.base_url + path
        body = {
            'email': delivery.customer.account.email,
            'amount': delivery.get_delivery_amount() * 100,
            'reference': delivery.get_uuid_string(),
        }

        response = requests.post(url, headers=self.headers, json=body)

        return response.json().get('data').get('authorization_url')
    
    def validate_account(self, **kwargs):
        path = ('bank/validate')
        url = self.get_url(path)

        body = {**kwargs}
        
        response = requests.post(url, headers=self.headers, json=body)
        
        response_data = response.json()
        if response.status_code == 200:
            return response_data['data']['status'] == 'success', response_data['data']

        return response_data['status'],  response_data['message']

    def resolve_account_detail(self, account_number: int, bank_code: int ):
        path = ('bank/resolve')
        url = self.get_url(path)

        payload={"account_number": account_number, "bank_code": bank_code}
        
        response = requests.get(url, headers=self.headers, params=payload)
        
        response_data = response.json()
        if response.status_code == 200:
            return response_data['status'], response_data['data']

        return response_data['status'],  response_data['message']


    def get_bank_list(self):
        path = ("bank?currency=NGN")
        url = self.get_url(path)
        response = requests.get(url, headers=self.headers)
                
        response_data = response.json()
        if response.status_code == 200:
            return response_data['status'] == 'True', response_data['data']

        return response_data['status'],  response_data['message']

    def generate_transfer_recipient(self, **kwargs):
        path = ("transferrecipient")
        url = self.get_url(path)

        response = requests.post(url, headers=self.headers, json={**kwargs})
                
        response_data = response.json()
        if response.status_code == 201:
            return response_data['status'], response_data['data']

        return response_data['status'],  response_data['message']
            
    def initiate_transfer(self, amount=None, recipient=None, reference=None):
        path = ("transfer")
        url = self.get_url(path)
        
        body = {
            "source": "balance",
            "reason": "Rider payment for earnings", 
            "amount": amount, 
            "recipient": recipient,
            "reference": reference
        }

        response = requests.post(url, headers=self.headers, json=body)
                
        response_data = response.json()
        if response.status_code == 200:
            return response_data['status'], response_data['data']

        return response_data['status'],  response_data['message']
    