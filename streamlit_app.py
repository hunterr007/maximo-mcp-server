import os
import requests
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="Maximo AI Assistant",
    page_icon="Logo.jpg",
    layout="wide"
)

# --- Model and Tool Configuration ---
try:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    MCP_SERVER_URL = "http://127.0.0.1:5001/"
except Exception as e:
    st.error(f"Error configuring Google AI. Make sure your GOOGLE_API_KEY is set in the .env file. Details: {e}")
    st.stop()


# --- MCP Server Interaction ---
# --- Tool Functions ---
def get_asset(asset_id: str):
    """Gets details for a specific asset."""
    return requests.get(f"{MCP_SERVER_URL}/tools/get_asset/{asset_id}").json()

def list_assets(where: str = ""):
    """Lists assets, optionally filtering with an OSLC where clause."""
    return requests.get(f"{MCP_SERVER_URL}/tools/list_assets", params={"oslc.where": where}).json()


# --- MCP Server Interaction ---
@st.cache_data(ttl=3600) # Cache for 1 hour
def get_tools_from_mcp():
    """Fetches and prepares tools from the MCP server."""
    try:
        response = requests.get(f"{MCP_SERVER_URL}/tools")
        response.raise_for_status()
        # This is a simplified mapping. A real implementation would dynamically
        # build the tool function definitions from the manifest.
        return {
            "get_asset": get_asset,
            "list_assets": list_assets,
        }
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to MCP Server at {MCP_SERVER_URL}. Is it running? Details: {e}")
        return None

# --- Streamlit UI ---
st.title("🤖 Maximo AI Assistant")
st.caption("Your intelligent interface for IBM Maximo. Powered by Gemini and MCP.")

tools = get_tools_from_mcp()

from google.generativeai.types import FunctionDeclaration, Tool

if tools:
    # --- Model and Tool Configuration ---
    asset_tools = Tool(
        function_declarations=[
            FunctionDeclaration(
                name="get_asset",
                description="Gets details for a specific asset by its ID.",
                parameters={
                    "type": "object",
                    "properties": {
                        "asset_id": {"type": "string", "description": "The ID of the asset to retrieve."}
                    },
                    "required": ["asset_id"]
                },
            ),
            FunctionDeclaration(
                name="list_assets",
                description="Lists assets, optionally filtering with a where clause.",
                parameters={
                    "type": "object",
                    "properties": {
                        "where": {"type": "string", "description": "The where clause to filter assets."}
                    },
                },
            ),
        ]
    )

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        tools=[asset_tools],
    )
    chat = model.start_chat()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What would you like to know about your Maximo data?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Thinking..."):
            response = chat.send_message(prompt)

        function_response = None
        # Check for function calls
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            function_name = function_call.name
            function_args = function_call.args

            if function_name in tools:
                function_to_call = tools[function_name]
                function_response = function_to_call(**function_args)

                # Send the function's response back to the model
                response = chat.send_message(
                    [{"function_response": {"name": function_name, "response": function_response}}]
                )

        response_text = response.text
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response_text)
            if function_response:
                if function_name == "list_assets":
                    st.dataframe(function_response.get("member", []))
                elif function_name == "get_asset":
                    st.json(function_response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_text})
else:
    st.warning("Could not load tools from MCP Server. The assistant is offline.")
