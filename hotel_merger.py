from typing import List, Dict, Callable
from collections import defaultdict
from copy import deepcopy
from dataclasses import is_dataclass
from merge_strategy import default_merge

class HotelMerger:
    def __init__(self, hotel_data_class, merge_strategies: Dict[str, Callable] = None):
        if not is_dataclass(hotel_data_class):
            raise TypeError("The hotel_data_class must be a dataclass.")
        self.hotel_data_class = hotel_data_class
        self.merge_strategies = merge_strategies or {}

    def merge_hotels(self, hotel_list) -> List:
        merge_key = lambda hotel: hotel.get("id")

        grouped_hotels = defaultdict(lambda: deepcopy(self.hotel_data_class()))

        for hotel in hotel_list:
            key = merge_key(hotel)
            if not key:
                continue

            for field, value in hotel.items():
                current_value = getattr(grouped_hotels[key], field, None)
                merge_strategy = self.merge_strategies.get(field, default_merge)

                merged_value = merge_strategy(current_value, value)

                setattr(grouped_hotels[key], field, merged_value)

        return list(grouped_hotels.values())

