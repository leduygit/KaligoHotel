from typing import List, Dict, Callable
from collections import defaultdict
from copy import deepcopy
from dataclasses import is_dataclass

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
                merge_strategy = self.merge_strategies.get(field, self.default_merge)

                merged_value = merge_strategy(current_value, value)

                setattr(grouped_hotels[key], field, merged_value)

        return list(grouped_hotels.values())

    def default_merge(self, current_value, new_value):
        if isinstance(current_value, list):
            return list(set(current_value + (new_value or [])))  # Merge lists, handle None
        elif isinstance(current_value, dict):
            current_value.update(new_value or {})  # Merge dictionaries, handle None
            return current_value
        elif isinstance(current_value, str):
            # Return the longest string
            if not new_value or (current_value and len(current_value) >= len(new_value)):
                return current_value
            return new_value
        else:
            # Handle other cases, prioritize non-None values
            return current_value if current_value is not None else new_value
