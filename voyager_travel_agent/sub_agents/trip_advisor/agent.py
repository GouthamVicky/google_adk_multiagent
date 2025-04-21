"""Inspiration agent. A pre-booking agent covering the ideation part of the trip."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from voyager_travel_agent.shared_libraries.types import DesintationIdeas, POISuggestions, json_response_config
from voyager_travel_agent.sub_agents.trip_advisor import prompt
from voyager_travel_agent.tools.places import map_tool


place_agent = Agent(
    model="gemini-2.0-flash",
    name="place_agent",
    instruction=prompt.PLACE_AGENT_INSTR,
    description="This agent suggests a few destination given some user preferences",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=DesintationIdeas,
    output_key="place",
    generate_content_config=json_response_config,
)

explorer_agent = Agent(
    model="gemini-2.0-flash",
    name="explorer_agent",
    description="This agent suggests a few activities and points of interests given a destination",
    instruction=prompt.POI_AGENT_INSTR,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=POISuggestions,
    output_key="poi",
    generate_content_config=json_response_config,
)

trip_advisor_agent = Agent(
    model="gemini-2.0-flash",
    name="trip_advisor_agent",
    description="A travel adivsor agent who inspire users, and discover their next vacations; Provide information about places, activities, interests,",
    instruction=prompt.INSPIRATION_AGENT_INSTR,
    tools=[AgentTool(agent=place_agent), AgentTool(agent=explorer_agent), map_tool],
)