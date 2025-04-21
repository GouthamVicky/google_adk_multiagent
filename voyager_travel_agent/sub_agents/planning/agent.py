"""Planning agent. A pre-booking agent covering the planning part of the trip."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig
from voyager_travel_agent.shared_libraries import types
from voyager_travel_agent.sub_agents.planning import prompt
from voyager_travel_agent.tools.memory import memorize
from google.adk.tools      import FunctionTool, ToolContext
from voyager_travel_agent.tools.itinerary_creator import save_itinerary_artifact,create_travel_website
from google.adk.tools import google_search


save_itinerary_tool = FunctionTool(
    func=save_itinerary_artifact,
)

itinerary_agent = Agent(
    model="gemini-2.0-flash-001",
    name="itinerary_agent",
    description="Helps user to Create a itinerary in JSON format",
    instruction=prompt.ITINERARY_AGENT_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=types.Itinerary,
    output_key="itinerary",
    #tools=[save_itinerary_artifact],
    generate_content_config=types.json_response_config,
)

hotel_agent = Agent(
    model="gemini-2.0-flash-001",
    name="hotel_agent",
    description="Help users find hotel around a specific geographic area and Help users with the room choices for a hotel",
    instruction=prompt.HOTEL_SEARCH_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=types.HotelsSelection,
    output_key="hotel",
    generate_content_config=types.json_response_config,
)



flight_agent = Agent(
    model="gemini-2.0-flash-001",
    name="flight_agent",
    description="Helps users search and track flights using Google Search results.",
    instruction=prompt.FLIGHT_SEARCH_INSTR_WITH_TOOL,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    #output_schema=types.FlightsSelection,
    output_key="flight",
    tools=[google_search],
    generate_content_config=types.json_response_config,
)

create_travel_website = FunctionTool(
    func=create_travel_website,
)

travel_guide_designer_agent=Agent(
    model="gemini-2.0-flash-001",
    name="travel_guide_designer_agent",
    description="Agent that creates a html content from the given itinerary json and saves provided text content to a html file on disk.",
    instruction=prompt.TRAVEL_GUIDE_DESIGNER_AGENT,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_key="itinerary_design_html",
    #tools=[save_html_tool],
    generate_content_config=types.json_response_config,
)

planning_agent = Agent(
    model="gemini-2.0-flash-001",
    description="""Helps users turn their travel ideas into reality by planning personalized itineraries, uncovering great deals on flights and hotels, 
                and ensuring a hassle-free vacation journey.""",
    name="planning_agent",
    instruction=prompt.PLANNING_AGENT_INSTR,
    tools=[
        AgentTool(agent=flight_agent),
        AgentTool(agent=hotel_agent),
        AgentTool(agent=itinerary_agent),
        memorize,
        save_itinerary_artifact,
        AgentTool(agent=travel_guide_designer_agent),
        create_travel_website
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.1, top_p=0.5
    )
)