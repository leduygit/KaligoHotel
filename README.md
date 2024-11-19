# Hotel Data Merger and Supplier Adapter

This project is designed to fetch, merge, and filter hotel data from multiple suppliers. The data format from each supplier is transformed using an adapter to conform to a common target format. The merging logic is customizable, allowing for different strategies to handle conflicts when combining hotel records.

## Components

### 1. **Adapters**

Adapters are used to transform the supplier-specific data format into a standard target format. The `SupplierFactory` class uses a mapping of suppliers to their respective adapter classes to instantiate them.

**Usage Example:**

```python
supplier_mapping = {
    "Acme": (AcmeSupplier, AcmeAdapter),
    "Patagonia": (PatagoniaSupplier, PatagoniaAdapter),
    "Paperflies": (PaperfliesSupplier, PaperfliesAdapter),
}

suppliers = SupplierFactory(supplier_mapping).get_suppliers()
```

### 2. **HotelMerger**

The `HotelMerger` class is responsible for merging hotel data from multiple suppliers. It takes a `hotel_data_class` (which is a target format data class) and a dictionary of custom merge strategies for handling specific fields (like `images`).

The merge function can be customized via a `merge_strategies` dictionary, allowing different fields to use different merge functions.

**Usage Example:**

```python
merge_strategies = {
    "images": default_merge,
}

DataClass = Hotel
hotel_merger = HotelMerger(DataClass, merge_strategies)

merged_data = hotel_merger.merge_hotels(hotel_list)
```

### 3. **HotelService**

The `HotelService` class is responsible for filtering merged hotel data based on specific arguments provided by the user. The `get_hotel` method iterates over the provided filter arguments and checks if each hotel matches the criteria.

**Usage Example:**

```python
service = HotelService(merged_data)
result = service.get_hotel(args)
```

### 4. **Argument Parsing**

The `argument_parsing` function processes command-line arguments and converts them into a structure compatible with the filtering logic in `HotelService`. It handles arguments like `id` and `destination_id` and allows for flexible argument length.

**Usage Example:**

```python
args_key = ["id", "destination_id"]
args = argument_parsing(args_key)
```

### 5. **Merging and Fetching Data**

The main process involves the following steps:

1. **Fetch Data:** Collect raw hotel data from the different suppliers via their respective adapters.
2. **Merge Data:** Use the `HotelMerger` class to merge hotel data into a unified format.
3. **Filter Data:** Apply the provided filters to the merged data using `HotelService`.

**Usage Example:**

```python
raw_data = fetch_all_data()  # Fetch raw data from suppliers
merged_data = merge_hotels(raw_data)  # Merge the raw data into a unified format
service = HotelService(merged_data)  # Create a service to filter the merged data
result = service.get_hotel(args)  # Filter the data based on provided arguments
```

### 6. **Main Function**

The `main()` function brings everything together. It parses the arguments, fetches and merges the hotel data, filters it using `HotelService`, and prints the results in JSON format.

```python
def main():
    args_key = ["id", "destination_id"]
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
```

---

## Future Considerations

1. **Dynamic Supplier Support:**

   - The system is built to support additional suppliers by simply adding them to the `supplier_mapping`. This makes the code easily extensible if new suppliers need to be integrated.

2. **Argument Filter Changes:**

   - The `get_hotel` function and `argument_parsing` can be modified through the `arg_key` to support new filters or different argument structures in the future.

3. **Change of Supplier Format:**

   - If the supplier's data format changes, the corresponding adapter can be updated and simply changing the `supplier_mapping` without affecting the core logic of the system.

4. **Custom Merge Strategies:**
   - You can define custom merging strategies in the `merge_strategy.py` file, then mapping them the `merge_hotels` function to handle more complex merge scenarios.

---
