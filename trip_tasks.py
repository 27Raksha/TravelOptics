from crewai import Task
from textwrap import dedent

class TripTasks:

    def analyze_task(self, agent, arrival_city, departure_city, interests, arrival_date, departure_date, number_of_days):
        return Task(
            description=dedent(f"""
                Analyze the specified arrival city: {arrival_city}.
                Your task is to provide a detailed report on this city,
                considering factors such as weather patterns, seasonal
                events, travel costs, and accommodation options.

                Focus on the following aspects for {arrival_city}:
                1. Current and forecasted weather conditions for the travel dates
                2. Upcoming cultural or seasonal events during the visit
                3. Overall travel expenses, including flight costs to and from {departure_city}
                4. Hotel options and their prices
                5. Main attractions and their relevance to the traveler's interests

                Your final answer must be a comprehensive report on {arrival_city},
                including all the information you've gathered about it. Make sure
                to include actual flight costs, specific hotel recommendations,
                a detailed weather forecast, and attractions that align with
                the traveler's interests.

                {self.__tip_section()}

                Arrival Date: {arrival_date}
                Departure Date: {departure_date}
                Traveling from: {departure_city}
                Traveling to: {arrival_city}
                Traveler Interests: {interests}
                Number of days: {number_of_days}
            """),
            agent=agent,
            expected_output="Detailed report on the specified arrival city including flight costs, weather forecast, hotel recommendations, and attractions tailored to the traveler's interests"
        )

    def gather_task(self, agent, arrival_city, departure_city, interests, arrival_date, departure_date, number_of_days):
        return Task(
            description=dedent(f"""
                As a local expert on {arrival_city}, compile an 
                in-depth guide for someone traveling there and wanting 
                to have THE BEST trip ever!
                Gather information about key attractions, local customs,
                special events, and daily activity recommendations.
                Find the best spots to go to, the kind of place only a
                local would know.
                This guide should provide a thorough overview of what 
                the city has to offer, including hidden gems, cultural
                hotspots, must-visit landmarks, weather forecasts, and
                high level costs.
                
                The final answer must be a comprehensive city guide, 
                rich in cultural insights and practical tips, 
                tailored to enhance the travel experience.
                {self.__tip_section()}

                Arrival Date: {arrival_date}
                Departure Date: {departure_date}
                Traveling from: {departure_city}
                Traveling to: {arrival_city}
                Traveler Interests: {interests}
                Number of days: {number_of_days}
            """),
            agent=agent,
            expected_output="Comprehensive city guide including hidden gems, cultural hotspots, and practical travel tips"
        )

    def plan_task(self, agent, arrival_city, departure_city, interests, arrival_date, departure_date, number_of_days):
        return Task(
            description=dedent(f"""
                Expand the city guide into a full {number_of_days}-day travel 
                itinerary for {arrival_city} with detailed per-day plans, including 
                weather forecasts, places to eat, packing suggestions, 
                and a budget breakdown.
                
                You MUST suggest actual places to visit, actual hotels 
                to stay and actual restaurants to go to.
                
                This itinerary should cover all aspects of the trip, 
                from arrival to departure, integrating the city guide
                information with practical travel logistics.
                
                Your final answer MUST be a complete expanded travel plan,
                formatted as markdown, encompassing a daily schedule,
                anticipated weather conditions, recommended clothing and
                items to pack, and a detailed budget, ensuring THE BEST
                TRIP EVER. Be specific and give it a reason why you picked
                each place, what makes them special! {self.__tip_section()}

                Arrival Date: {arrival_date}
                Departure Date: {departure_date}
                Traveling from: {departure_city}
                Traveling to: {arrival_city}
                Traveler Interests: {interests}
                Number of days: {number_of_days}
            """),
            agent=agent,
            expected_output="Complete expanded travel plan with daily schedule, weather conditions, packing suggestions, and budget breakdown"
        )

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $100!"