import openai
import logging
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Your API keys
GOOGLE_API_KEY = "AIzaSyAwODBLH8Fx2jEMckzjYfK0_PNnNZT7Tu4"
OPENAI_API_KEY = "sk-proj-az68uw8juyuoiBMCkE8CT3BlbkFJrrTAC98UOOxpQgdtH5re"

openai.api_key = OPENAI_API_KEY

app = FastAPI()

# CORS configuration
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:5500",  # Change or add frontend origin if necessary
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Function to fetch tourist attractions
async def get_tourist_attractions(city_name: str):
    try:
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=tourist+attractions+in+{city_name}&key={GOOGLE_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if "results" not in data or not data["results"]:
            raise HTTPException(status_code=404, detail="No tourist attractions found")

        attractions = [
            {
                "name": place["name"],
                "address": place.get("formatted_address"),
                "rating": place.get("rating"),
                "website": place.get("website"),
                "reviews": place.get("user_ratings_total")
            }
            for place in data["results"]
        ]

        return {"city": city_name, "attractions": attractions}

    except requests.RequestException as e:
        logger.error(f"Request error in get_tourist_attractions: {e}")
        raise HTTPException(status_code=500, detail="Error fetching data from Google Maps API")
    except Exception as e:
        logger.error(f"General error in get_tourist_attractions: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

# Function to generate response using OpenAI
async def generate_openai_responses(prompt: str, user_prompt: str):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=700,  # Adjust token limit as needed
            stop=None,
            temperature=0.1
        )
        return response.choices[0].message["content"]

    except Exception as e:
        logger.error(f"Error in generate_openai_responses: {e}")
        return "Sorry, I couldn't process your request."

# Function to combine attractions and generate a travel plan
async def get_attractions_and_generate_response(city_name: str, days: int):
    try:
        # Fetch tourist attractions
        attractions_data = await get_tourist_attractions(city_name)
        attractions_list = attractions_data["attractions"]

        if not attractions_list:
            return "No tourist attractions found."

        # Format the attractions data for OpenAI prompt
        attractions_info = "\n".join([
            f"{attr['name']}, Address: {attr['address']}, Rating: {attr['rating']}" 
            for attr in attractions_list
        ])
        user_prompt = f'''
        Here are some tourist attractions in {city_name}. Please create a custom travel plan for {days} days, including the best places to visit. 
        Use the provided information as a reference for the places to include. The itinerary should include specific time slots for each day, 
        highlighting key attractions, activities, and experiences. Provide details about entry fees, timings, and notable aspects of each place. 
        Additionally, suggest places to eat, shopping areas, and any special activities. The plan should cover a mix of historical sites, 
        cultural experiences, nature spots, and leisure activities. Use the following format for each day:
        
        Day [1]:
        [Time Slot]: [Activity/Place Description]
        [Time Slot]: [Activity/Place Description]
        ...
        
        Day [2]:
        [Time Slot]: [Activity/Place Description]
        ...
        
        Where to Eat: [List of restaurants or food spots]
        Shopping: [Shopping areas or unique local products]
        Special Activities: [Optional activities or experiences]
        '''

        # Generate the response using OpenAI
        openai_prompt = "Create a custom travel plan for the given number of days, prioritizing the best tourist attractions near the specified location."
        response = await generate_openai_responses(openai_prompt, user_prompt)

        if response is None:
            return "Sorry, I couldn't process your request."

        # Clean up the response
        clean_response = response.replace("*", "").replace("#", "").strip()
        return clean_response

    except HTTPException as e:
        logger.error(f"HTTP error in get_attractions_and_generate_response: {e}")
        raise e
    except Exception as e:
        logger.error(f"General error in get_attractions_and_generate_response: {e}")
        return "Sorry, I couldn't process your request."

# API endpoint to get attractions and generate a travel plan
@app.get("/get-attractions/{city_name}/{days}")
async def get_attractions(city_name: str, days: int):
    return await get_attractions_and_generate_response(city_name, days)

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
