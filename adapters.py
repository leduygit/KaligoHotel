from hotel_data import Hotel

class BaseAdapter:
    def adapt(dto):
        raise NotImplementedError
    
class AcmeAdapter:
    @staticmethod
    def adapt(dto):
        # Dynamically generated image links from original data
        room_images = [
            {"link": image_url, "description": f"Room Image {i+1}"}
            for i, image_url in enumerate(dto.get("RoomImages", []))
        ]
        
        site_images = [
            {"link": image_url, "description": f"Site Image {i+1}"}
            for i, image_url in enumerate(dto.get("SiteImages", []))
        ]
        
        amenities_images = [
            {"link": image_url, "description": f"Amenities Image {i+1}"}
            for i, image_url in enumerate(dto.get("AmenitiesImages", []))
        ]
        
        return {
            "id": dto["Id"],
            "destination_id": dto["DestinationId"],
            "name": dto["Name"],
            "location": {
                "lat": dto["Latitude"],
                "lng": dto["Longitude"],
                "address": f"{dto['Address'].strip()}, {dto['PostalCode']}",
                "city": dto["City"],
                "country": dto["Country"]
            },
            "description": dto["Description"].strip(),
            "amenities": {
                "general": [facility.strip().lower().replace(" ", "") for facility in dto["Facilities"]]
            },
            "images": {
                "rooms": room_images,  # Dynamically extracted room images
                "site": site_images,   # Dynamically extracted site images
                "amenities": amenities_images  # Dynamically extracted amenities images
            },
            "booking_conditions": dto.get("BookingConditions", [])
        }

class PatagoniaAdapter:
    @staticmethod
    def adapt(dto):
        hotel_data = {
            "id": dto.get("id"),
            "destination_id": dto.get("destination"),
            "name": dto.get("name"),
            "location": {
                "lat": dto.get("lat"),
                "lng": dto.get("lng"),
                "address": dto.get("address"),
            },
            "description": dto.get("info", ""),
            "amenities": {
                "general": dto.get("amenities", [])
            },
            "images": {
                "rooms": [
                    {"link": image.get("url"), "description": image.get("description")}
                    for image in dto.get("images", {}).get("rooms", [])
                ],
                "amenities": [
                    {"link": image.get("url"), "description": image.get("description")}
                    for image in dto.get("images", {}).get("amenities", [])
                ]
            }
        }

        return hotel_data

class PaperfliesAdapter(BaseAdapter):
    @staticmethod
    def adapt(dto):
        return {
            "id": dto.get("hotel_id"),
            "destination_id": dto.get("destination_id"),
            "name": dto.get("hotel_name"),
            "location": {
                "address": dto["location"].get("address"),
                "country": dto["location"].get("country"),
            },
            "description": dto.get("details", ""),
            "amenities": {
                "general": dto["amenities"].get("general", []),
                "room": dto["amenities"].get("room", []),
            },
            "images": {
                "rooms": [
                    {"link": image.get("link"), "description": image.get("caption")}
                    for image in dto.get("images", {}).get("rooms", [])
                ],
                "site": [
                    {"link": image.get("link"), "description": image.get("caption")}
                    for image in dto.get("images", {}).get("site", [])
                ],
            },
            "booking_conditions": dto.get("booking_conditions", []),
        }
