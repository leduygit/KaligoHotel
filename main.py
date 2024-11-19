import json
from dataclasses import asdict
from adapters import AcmeAdapter, PatagoniaAdapter, PaperfliesAdapter
from suppliers import AcmeSupplier, PatagoniaSupplier, PaperfliesSupplier
from hotel_merger import HotelMerger
from merge_strategy import default_merge
from hotel_data import Hotel
import argparse


class SupplierFactory:
    def __init__(self, supplier_mapping):
        self.suppliers = [
            SupplierClass(AdapterClass())
            for SupplierClass, AdapterClass in supplier_mapping.values()
        ]

    def get_suppliers(self):
        return self.suppliers


class HotelService:
    def __init__(self, hotel_list):
        self.hotel_list = hotel_list.copy()

    def get_hotel(self, args):
        result = []

        if (len(args) == 0):
            return self.hotel_list

        for arg_set in args: 
            for hotel in self.hotel_list:
                satisfies = True

                for key, value in arg_set.items():
                    if value is not None and str(getattr(hotel, key, None)) != str(value):
                        satisfies = False
                        break

                if satisfies:
                    result.append(hotel)
                    break 
        return result


def fetch_all_data():
    supplier_mapping = {
        "Acme": (AcmeSupplier, AcmeAdapter),
        "Patagonia": (PatagoniaSupplier, PatagoniaAdapter),
        "Paperflies": (PaperfliesSupplier, PaperfliesAdapter),
    }

    suppliers = SupplierFactory(supplier_mapping).get_suppliers()

    raw_data = []
    for supplier in suppliers:
        raw_data.extend(supplier.get_hotel())

    return raw_data


def merge_hotels(hotel_list):
    merge_strategies = {
        "images": default_merge,
    }

    DataClass = Hotel

    hotel_merger = HotelMerger(DataClass, merge_strategies)
    
    return hotel_merger.merge_hotels(hotel_list)

def argument_parsing(keys):
    parser = argparse.ArgumentParser()
    for key in keys:
        parser.add_argument(f"{key}", type=str, help=f"{key} values")
    
    args = parser.parse_args()

    # Convert 'none' to None and split values by commas
    args_map = {key: [None if value == "none" else value for value in getattr(args, key).split(",")] for key in keys}

    args = []

    max_len = max(len(args_map[key]) for key in args_map)

    for i in range(max_len):
        args.append({key: args_map[key][i] if i < len(args_map[key]) else None for key in args_map})

    return args


def main():
    args_key = [
        "id", "destination_id"
    ]
    args = argument_parsing(args_key)

    # Fetch and merge data
    raw_data = fetch_all_data()
    merged_data = merge_hotels(raw_data)
    service = HotelService(merged_data)

    # define the arguments mapping, assuming they might change in the future
    result = service.get_hotel(args)

    print(json.dumps([asdict(hotel) for hotel in result], indent=4))


if __name__ == "__main__":
    main()
