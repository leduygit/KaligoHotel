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
        pass

class PaperfliesAdapter:
    @staticmethod
    def adapt(dto):
        pass