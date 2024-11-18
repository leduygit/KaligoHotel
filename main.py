from dataclasses import dataclass, field
from typing import List, Optional
import json
from dataclasses import asdict
from adapters import BaseAdapter, AcmeAdapter, PatagoniaAdapter, PaperfliesAdapter
from suppliers import BaseSupplier, AcmeSupplier, PatagoniaSupplier, PaperfliesSupplier
import requests


@dataclass
class Image:
    link: str
    description: str

@dataclass
class Images:
    rooms: List[Image]
    site: List[Image]
    amenities: List[Image]

@dataclass
class Amenities:
    general: List[str]
    room: List[str]

@dataclass
class Location:
    lat: float
    lng: float
    address: str
    city: str
    country: str

@dataclass
class Hotel:
    id: str
    destination_id: int
    name: str
    location: Location
    description: str
    amenities: Amenities
    images: Images
    booking_conditions: List[str]


class SupplierFactory:
    def __init__(self, supplier_mapping):
        self.supplier_mapping = supplier_mapping

    def create_supplier(self):
        return [
            SupplierClass(AdapterClass())
            for SupplierClass, AdapterClass in self.supplier_mapping.values()
        ]

supplier_mapping = {
    "Acme": (AcmeSupplier, AcmeAdapter),
    "Patagonia": (PatagoniaSupplier, PatagoniaAdapter),
    "Paperflies": (PaperfliesSupplier, PaperfliesAdapter),
}

# Create suppliers dynamically
supplier_factory = SupplierFactory(supplier_mapping)
suppliers = supplier_factory.create_supplier()

# Get hotel data from all suppliers
for supplier in suppliers:
    hotel = supplier.get_hotel()
    print(hotel)
    


# print hotel in json format

# json_output = json.dumps(asdict(hotel), indent=4)
# print(json_output)