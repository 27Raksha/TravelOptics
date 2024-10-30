from crewai import Crew
from textwrap import dedent
from trip_agents import TripAgents
from trip_tasks import TripTasks
from langchain_core.prompts import ChatPromptTemplate
import openai
import google.generativeai as genai
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

class TripCrew:

  def __init__(self, arrival_city, departure_city, interests, arrival_date, departure_date, number_of_days):
    self.arrival_city = arrival_city
    self.departure_city = departure_city
    self.interests = interests
    self.arrival_date = arrival_date
    self.departure_date = departure_date
    self.number_of_days = number_of_days

  def run(self):
    agents = TripAgents()
    tasks = TripTasks()

    city_analysis_agent = agents.city_analysis_agent()
    local_expert_agent = agents.local_expert()
    travel_concierge_agent = agents.travel_concierge()

    analyze_task = tasks.analyze_task(
      city_analysis_agent,
      self.arrival_city,
      self.departure_city,
      self.interests,
      self.arrival_date,
      self.departure_date,
      self.number_of_days,
    )
    gather_task = tasks.gather_task(
      local_expert_agent,
      self.arrival_city,
      self.departure_city,
      self.interests,
      self.arrival_date,
      self.departure_date,
      self.number_of_days,
    )
    plan_task = tasks.plan_task(
      travel_concierge_agent, 
      self.arrival_city,
      self.departure_city,
      self.interests,
      self.arrival_date,
      self.departure_date,
      self.number_of_days,
    )

    crew = Crew(
      agents=[
        city_analysis_agent, local_expert_agent, travel_concierge_agent
      ],
      tasks=[analyze_task, gather_task, plan_task],
      verbose=True
    )

    result = crew.kickoff()
    return result

if __name__ == "__main__":
  print("## Welcome to Travel Optix")
  print('-------------------------------')
  departure_city = input(
    dedent("""
      What is your departure city?
    """))
  arrival_city = input(
    dedent("""
      What is your destination city?
    """))
  arrival_date = input(
    dedent("""
      What is your arrival date? Please provide it in the format DD-MM-YYYY.
    """))
  departure_date = input(
    dedent("""
      What is your departure date? Please provide it in the format DD-MM-YYYY.
    """))
  number_of_days = input(
    dedent("""
      How many days are you planning for this trip?
    """))
  interests = input(
    dedent("""
      What are some of your high level interests and hobbies?
    """))
  
  trip_crew = TripCrew(arrival_city, departure_city, interests, arrival_date, departure_date, number_of_days)
  result = trip_crew.run()
  print("\n\n########################")
  print("## Here is your detailed trip itinerary, carefully crafted to ensure an enjoyable and well-organized travel experience. It includes all the key destinations, activities, and timelines to make your trip memorable and hassle-free.")
  print("########################\n")
  print(result)


def get_gemini_responses(input_text, system):
    # Combine the system prompt and input text
    system = """You are given a detailed {number_of_days} days travel itinerary for {arrival_city}. Your task is to extract and list only the locations mentioned, categorized by the day. 
    Make sure to omit any descriptions, reasons, prices, or other details. Focus strictly on the location names based on the day."""
    combined_input = f"{system_prompt}\n\nInput: {input_text}"
    response = model.generate_content(combined_input)
    return response.text

