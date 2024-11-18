# Define custom merge strategies

from hotel_data import Image, Images
from collections import defaultdict
from typing import List, Dict

def merge_general_field(current_value, new_value):
    if isinstance(current_value, list):
        return list(set(current_value + new_value))
    return new_value 

def merge_room_field(current_value, new_value):
    if isinstance(current_value, list):
        return list(set(current_value + new_value)) 
    return new_value


def validate_images(images):
    """
    Validate that the provided images data is properly formatted.
    If any field is missing or not a list, default to an empty list.
    """
    if images is None:
        images = Images(rooms=[], site=[], amenities=[])
    
    def validate_image_list(image_list):
        if not isinstance(image_list, list):
            return []
        # Ensure all items in the list are Image instances
        return [image for image in image_list if isinstance(image, Image)]

    return Images(
        rooms=validate_image_list(getattr(images, "rooms", [])),
        site=validate_image_list(getattr(images, "site", [])),
        amenities=validate_image_list(getattr(images, "amenities", [])),
    )


def merge_images_field(existing, new):
    """
    Merge the images field with validation for both existing and new images.
    """
    # Validate input data
    existing = validate_images(existing)
    new = validate_images(new)

    def merge_image_lists(existing_list: List[Image], new_list: List[Image]) -> List[Image]:
        # Use a dictionary to ensure unique links per description
        merged_dict: Dict[str, List[str]] = defaultdict(set)

        # Process existing images
        for image in existing_list:
            merged_dict[image.description].add(image.link)

        # Process new images
        for image in new_list:
            merged_dict[image.description].add(image.link)

        # Convert back to list of Image objects
        return [
            Image(link=link, description=description)
            for description, links in merged_dict.items()
            for link in links
        ]

    # Merge each category of images
    merged_rooms = merge_image_lists(existing.rooms, new.rooms)
    merged_site = merge_image_lists(existing.site, new.site)
    merged_amenities = merge_image_lists(existing.amenities, new.amenities)

    return Images(rooms=merged_rooms, site=merged_site, amenities=merged_amenities)

