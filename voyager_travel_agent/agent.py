from google.adk.agents import Agent

from voyager_travel_agent import prompt
from voyager_travel_agent.sub_agents.planning.agent import planning_agent
from voyager_travel_agent.sub_agents.trip_advisor.agent import trip_advisor_agent
from voyager_travel_agent.sub_agents.payments.agent import booking_agent
from voyager_travel_agent.tools.memory import _load_precreated_itinerary


root_agent = Agent(
    model="gemini-2.0-flash-001",
    name="root_agent",
    description="""A central travel concierge agent designed to coordinate specialized sub-agents for planning, 
                booking, and managing personalized travel experiences. The root agent intelligently delegates user requests 
                to the appropriate sub-agent based on intent, ensuring smooth and efficient travel assistance.""",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[trip_advisor_agent,
        planning_agent,
        booking_agent
    ],
    before_agent_callback=_load_precreated_itinerary,
)