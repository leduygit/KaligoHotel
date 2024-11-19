# Define custom merge strategies

def default_merge(current_value, new_value):
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


