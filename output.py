from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import openai
import google.generativeai as genai
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

load_dotenv()


result="""Your Itinerary:
2-Day Travel Itinerary for Bangalore

Day 1: Exploring Bangalore's Museums and Shopping Centers

Morning: Arrival and Check-in


Arrival: Land in Bangalore early morning from Delhi.

Hotel Check-in: Holiday Inn Bengaluru Racecourse

Price: $100 per night

Highlights: Modern hotel with comfortable rooms, a rooftop pool, and proximity to major attractions.

Reason: It offers a balance of comfort, amenities, and accessibility to key locations.




Late Morning: Visvesvaraya Industrial and Technological Museum


Location: Kasturba Road, Bengaluru-560001, INDIA.

Details: Offers interactive exhibits on science and technology.

Reason: Perfect for museum enthusiasts with a keen interest in science and technology.


Lunch: MTR (Mavalli Tiffin Rooms)


Location: 14, Lalbagh Road, Bangalore 560027, Karnataka, India.

Cuisine: Traditional South Indian breakfast and meals.

Reason: Renowned for authentic South Indian cuisine, especially the dosas and filter coffee.


Afternoon: National Gallery of Modern Art


Location: 49, Palace Road, Manikyavelu Mansion, Vasanth Nagar, Bengaluru, Karnataka 560052.

Details: Showcases contemporary Indian art and hosts various exhibitions.

Reason: Ideal for art lovers looking to explore modern Indian art.


Evening: Shopping at UB City Mall


Location: 24, Vittal Mallya Road, Bangalore 560001, Karnataka, India.

Details: A luxury shopping destination with high-end brands, fine dining, and entertainment options.

Reason: Offers a mix of shopping, dining, and entertainment in a luxurious setting.


Dinner: Karavalli


Location: The Gateway Hotel, Residency Road, Bangalore 560025, Karnataka, India.

Cuisine: Authentic coastal cuisine from Kerala, Karnataka, and Goa.

Reason: Known for its unique coastal flavors and a must-visit for food enthusiasts.


Day 2: Cultural Exploration and Local Delights

Morning: Lalbagh Botanical Garden


Location: Mavalli, Bengaluru, Karnataka 560004, India.

Details: Known for its stunning flower shows and diverse plant species.

Reason: A serene start to the day with a leisurely walk amidst nature.


Late Morning: HAL Aerospace Museum


Location: Old Airport Road, Marathahalli, Bengaluru, Karnataka 560037.

Details: Provides insights into India's aviation history and aerospace technology.

Reason: Offers a unique perspective on India's advancements in aerospace.


Lunch: Vidyarthi Bhavan


Location: 32, Gandhi Bazaar Main Rd, Gandhi Bazaar, Basavanagudi, Bengaluru, Karnataka 560004, India.

Cuisine: Famous for crispy dosas and South Indian snacks.

Reason: An iconic eatery known for its delicious dosas and traditional South Indian fare.


Afternoon: Bangalore Palace


Location: Vasanth Nagar, Bangalore 560052, Karnataka, India.

Details: Resembling England’s Windsor Castle, it offers a glimpse into Bangalore’s royal heritage.

Reason: Provides a historical and architectural exploration of Bangalore's royal past.


Evening: VV Puram Food Street


Location: Old Market Road, Sajjan Rao Circle, VV Puram, Bengaluru, Karnataka 560004, India.

Details: A must-visit for food lovers, offering a variety of street food delicacies.

Reason: Perfect for experiencing local street food and flavors.


Dinner: Toit Brewpub


Location: 298, Namma Metro Pillar 62, 100 Feet Road, Indiranagar, Bangalore 560038, Karnataka, India.

Cuisine: Popular for craft beers and a diverse food menu.

Reason: A great place to unwind with craft beers and a diverse menu.


Packing Suggestions


Clothing: Light, breathable fabrics for the warm weather. A mix of casual and semi-formal attire.

Footwear: Comfortable walking shoes for exploring the city.

Essentials: Sunscreen, sunglasses, hat, and a reusable water bottle.

Weather Gear: A light jacket or umbrella for occasional rain showers.


Budget Breakdown


Flights: Approx. $127 (Round trip fare with IndiGo)

Accommodation: $200 (2 nights at Holiday Inn Bengaluru Racecourse)

Meals: $60 (approx. $30 per day for meals)

Attractions and Activities: $50 (entry fees and miscellaneous expenses)

Local Transportation: $30 (Metro, auto-rickshaws, and cabs)

Shopping and Souvenirs: $100


Total Estimated Budget: $567


Conclusion

This 2-day itinerary for Bangalore ensures a balanced mix of cultural exploration, shopping, and culinary delights, all while keeping the budget in check. Enjoy your trip!"""

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

system = """You are given a detailed {number_of_days} days travel itinerary for {arrival_city}. Your task is to extract and list only the locations mentioned, categorized by the day. 
Make sure to omit any descriptions, reasons, prices, or other details. Focus strictly on the location names based on the day."""

def get_gemini_responses(input_text, system_prompt):
    # Combine the system prompt and input text
    combined_input = f"{system_prompt}\n\nInput: {input_text}"
    response = model.generate_content(combined_input)
    return response.text

result = get_gemini_responses(r, system)
print(result)


