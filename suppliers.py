import requests
from adapters import BaseAdapter


# https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme 
# https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia 
# https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies

class BaseSupplier:
    def __init__(self, adapter: BaseAdapter):
        self.adapter = adapter

    def endpoint():
        raise NotImplementedError

    def get_hotel(self):
        response = requests.get(self.endpoint())
        raw_data = response.json()

        return [
            self.adapter.adapt(dto)
            for dto in raw_data
        ]
    
class AcmeSupplier(BaseSupplier):
    @staticmethod
    def endpoint():
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme'

class PatagoniaSupplier(BaseSupplier):
    @staticmethod
    def endpoint():
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia'
    
class PaperfliesSupplier(BaseSupplier):
    @staticmethod
    def endpoint():
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies'
    
