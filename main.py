from dataclasses import dataclass, field
from typing import List, Optional
import json
from dataclasses import asdict
from adapters import BaseAdapter, AcmeAdapter, PatagoniaAdapter, PaperfliesAdapter
from suppliers import BaseSupplier, AcmeSupplier, PatagoniaSupplier, PaperfliesSupplier
from hotel_merger import HotelMerger
from merge_strategy import merge_general_field, merge_images_field
from hotel_data import Hotel
import requests


class SupplierFactory:
    def __init__(self, supplier_mapping):
        self.supplier_mapping = supplier_mapping

    def create_supplier(self):
        return [
            SupplierClass(AdapterClass())
            for SupplierClass, AdapterClass in self.supplier_mapping.values()
        ]
    
    
def fetch_all_data():
    supplier_mapping = {
        "Acme": (AcmeSupplier, AcmeAdapter),
        "Patagonia": (PatagoniaSupplier, PatagoniaAdapter),
        "Paperflies": (PaperfliesSupplier, PaperfliesAdapter),
    }

    # Create suppliers dynamically
    supplier_factory = SupplierFactory(supplier_mapping)
    suppliers = supplier_factory.create_supplier()

    raw_data = []
    for supplier in suppliers:
        raw_data.extend(supplier.get_hotel())

    return raw_data


def merge_hotels(hotel_list):
    merge_strategies = {
        "images": merge_images_field,
    }

    hotel_merger = HotelMerger(Hotel, merge_strategies)
    return hotel_merger.merge_hotels(hotel_list)


def main():
    raw_data = fetch_all_data()
    merged_data = merge_hotels(raw_data)

    # write to result.json
    with open("result.json", "w") as f:
        json.dump([asdict(hotel) for hotel in merged_data], f, indent=4)


if __name__ == "__main__":
    main()