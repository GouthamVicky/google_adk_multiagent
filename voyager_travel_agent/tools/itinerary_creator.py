import json
from typing import Dict, Any
from google.adk.agents import Agent
from google.adk.tools      import FunctionTool, ToolContext
import google.genai.types as types

# # 1) Rewrite the helper to return a dict
# def write_itinerary_to_file(data: Dict[str, Any], file_path: str = "itinerary.json") -> Dict[str, Any]:
#     """
#     Serialize the provided itinerary dict to JSON and write it to disk.

#     Args:
#         data (dict): The itinerary data to save.
#         file_path (str): Path where to write the JSON file.

#     Returns:
#         dict: {
#             "status": "success"|"error",
#             "file_path": str (if success),
#             "error": str (if error)
#         }
#     """
#     try:
#         with open(file_path, "w", encoding="utf-8") as f:
#             json.dump(data, f, indent=2)
#         return {"status": "success", "file_path": file_path}
#     except Exception as e:
#         return {"status": "error", "error": str(e)}
    
# # Wrap as an ADK tool
# save_itinerary_file = FunctionTool(
#     func=write_itinerary_to_file
# )

def save_itinerary_artifact(
    itinerary: dict,
    tool_context: ToolContext
) -> dict:
    """
    Save the given itinerary dict as a versioned JSON artifact.

    This will store the JSON under the current session in ADK's ArtifactService.
    Each call with the same filename bumps the version.

    Args:
        itinerary (dict): The itinerary data to persist.
        tool_context (ToolContext): ADK context, gives you save_artifact().

    Returns:
        dict: {
            "status": "success"|"error",
            "filename": str,
            "version": int,        # artifact version number
            "error": str (if any)
        }
    """
    try:
        # 1. Serialize to bytes
        payload = json.dumps(itinerary, indent=2)

        # # 2. Wrap in a types.Part with mime_type application/json
        # json_artifact = types.Part(
        #     inline_data=types.Blob(data=payload, mime_type="application/json")
        # )

        # 3. Save into the session-scoped artifact store
        filename = "/workspaces/NovaTech_Prototypes/voyager_travel_agent/data/itinerary.json"
        #version = tool_context.save_artifact(filename=filename, artifact=json_artifact)  # :contentReference[oaicite:0]{index=0}
        try:
            with open(filename, "w", encoding="utf-8") as f:
                #json.dump(payload, f, indent=2)
                f.write(payload)
                return {"status": "success", "filename": filename}
        except Exception as e:
            return {"status": "error", "error": str(e)}
        
        #return {"status": "success", "filename": filename, "version": version}
    except Exception as e:
        return {"status": "error", "error": str(e)}
    

def create_travel_website(path: str, itinerary_design_html: str) -> dict:
    """
    Write the given itinerary HTML content to a file at the specified path.

    Args:
        path (str): Filesystem path where to save the content.
        content (str): The text to write into the file.

    Returns:
        dict: {
            "status": "success" or "error",
            "path": the path written on success,
            "error": error message if failed
        }
    """
    try:
        path="/workspaces/NovaTech_Prototypes/voyager_travel_agent/data/travel_webpage.html"
        with open(path, "w", encoding="utf-8") as f:
            f.write(itinerary_design_html)
        return {"status": "success", "path": path}
    except Exception as e:
        return {"status": "error", "error": str(e)}