
from fastapi import FastAPI, HTTPException, Query
import requests
import http.client
import json

app = FastAPI()

# API keys
RAPIDAPI_KEY = "ca5430f17cmsh7fb1167ba92187ep1e6e1ejsnc5c25c02d5d5"
GOOGLE_API_KEY = "AIzaSyAwODBLH8Fx2jEMckzjYfK0_PNnNZT7Tu4"  # Replace with your Google API key

@app.get("/hotels/")
async def get_hotels(
    city: str,
    checkin_date: str,
    checkout_date: str,
    adults_number: int,
    children_number: int = Query(1, ge=0),  # Default to 1
    room_number: int = Query(1, ge=1),  # Default to 1
    page_number: int = Query(0, ge=0),  # Default to 0
    children_ages: str = Query("5", description="Comma-separated ages of children")  # Default to "5"
):
    try:
        # Step 1: Get latitude and longitude using Google Places API
        google_places_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={city}&key={GOOGLE_API_KEY}"
        geocode_response = requests.get(google_places_url)
        geocode_data = geocode_response.json()

        if not geocode_data.get('results'):
            raise HTTPException(status_code=404, detail="City not found")

        location = geocode_data['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        print(f"Latitude: {latitude}, Longitude: {longitude}")  # Log coordinates

        # Step 2: Validate children_number and children_ages consistency
        children_ages_list = []
        if children_number > 0:
            children_ages_list = children_ages.split(",")
            children_ages_list = [age.strip() for age in children_ages_list if age.strip()]
            print(f"Parsed children_ages: {children_ages_list}")
            print(f"Children number provided: {children_number}")
            print(f"Number of ages provided: {len(children_ages_list)}")

            if len(children_ages_list) != children_number:
                raise HTTPException(status_code=422, detail="The number of children does not correspond to the number of ages")
        else:
            raise HTTPException(status_code=422, detail="The number of children must be at least 1 with corresponding ages.")

        # Step 3: Construct the query string
        query = (
            f"/v2/hotels/search-by-coordinates?include_adjacency=true"
            f"&categories_filter_ids=class%3A%3A2%2Cclass%3A%3A4%2Cfree_cancellation%3A%3A1"
            f"&children_ages={children_ages}&order_by=popularity"
            f"&longitude={longitude}&latitude={latitude}"
            f"&room_number={room_number}&children_number={children_number}"
            f"&adults_number={adults_number}&locale=en-gb"
            f"&checkin_date={checkin_date}&checkout_date={checkout_date}"
            f"&page_number={page_number}&filter_by_currency=INR&units=metric"
        )

        print(f"Constructed Booking.com API query: {query}")  # Log the constructed query

        # Step 4: Send the request
        conn = http.client.HTTPSConnection("booking-com.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "booking-com.p.rapidapi.com"
        }
        conn.request("GET", query, headers=headers)
        res = conn.getresponse()
        data = res.read()
        conn.close()

        # Log the response status and data
        print(f"Booking.com API response status: {res.status}")
        print(f"Booking.com API response reason: {res.reason}")
        print(f"Booking.com API response data: {data.decode('utf-8')}")

        if res.status != 200:
            raise HTTPException(status_code=res.status, detail=f"Error fetching hotel data: {data.decode('utf-8')}")

        # Decode and parse the response
        hotels_data = json.loads(data.decode("utf-8"))

        # Extract relevant information
        hotels_info = []
        for hotel in hotels_data['results']:
            hotel_info = {
                "name": hotel.get("name"),
                "price": f"INR {hotel['priceBreakdown']['grossPrice']['value']}",
                "mainPhotoUrl": hotel.get("photoMainUrl"),
                "photoUrls": hotel.get("photoUrls", []),
                "review": hotel.get("reviewScore")
            }
            hotels_info.append(hotel_info)

        # Return the filtered and formatted response
        return {"results": hotels_info}

    except HTTPException as e:
        print(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Run the server with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
