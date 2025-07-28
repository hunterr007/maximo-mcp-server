# Maximo MCP Server

This project implements an MCP Server for the IBM Maximo API. It provides a set of tools to interact with Maximo resources like Assets, Work Orders, etc.

## High-Level Flow

1.  The MCP client sends a request to the MCP Server.
2.  The MCP Server receives the request and calls the appropriate tool function.
3.  The tool function makes a request to the Maximo API.
4.  The Maximo API returns a response to the tool function.
5.  The tool function returns the response to the MCP Server.
6.  The MCP Server returns the response to the MCP client.

## Files

-   `mcp_server.py`: The main application file. It contains the Flask server and the tool implementations.
-   `requirements.txt`: The project dependencies.
-   `.env`: The environment variables for the project.
-   `manifest.json`: The tool manifest file.
-   `README.md`: This file.

## Tools

- `get_asset`: Retrieves details of a specific asset by its ID.
- `list_assets`: Lists all assets, with optional filtering and pagination.

### Note on HTTP Methods

The tool endpoints use the `POST` method to receive parameters in a JSON payload, which is a standard practice for MCP servers, even for operations that fetch data.

### `list_assets` Parameters

-   `page_size` (optional, default: 10): The number of assets to return per page.
-   `page_num` (optional, default: 1): The page number to return.
-   `where` (optional): A filter to apply to the query. The value should be a valid Maximo `oslc.where` clause. For example, to filter for assets with a status of "OPERATING", you would use `"status=\"OPERATING\""`.

## Running the Maximo AI Assistant

This project includes an interactive web application built with Streamlit that allows you to chat with an AI assistant powered by Gemini and your Maximo MCP server.

### 1. Set Up Environment

First, install the required Python packages:

```bash
pip install -r requirements.txt
```

You will also need to create a `.env` file in the root of the project with your Maximo and Google API keys:

```
MAXIMO_API_URL=https://your-maximo-instance.com
MAXIMO_API_KEY=your-maximo-api-key
GOOGLE_API_KEY=your-google-api-key
```

### 2. Run the MCP Server

In your first terminal, start the MCP server:

```bash
python mcp_server.py
```

The server will start on `http://localhost:5001`. Keep this terminal running.

### 3. Run the Streamlit App

In a **new terminal window**, run the Streamlit application:

```bash
streamlit run streamlit_app.py
```

The application will open in your web browser. You can now chat with the Maximo AI Assistant and ask it questions about your assets.
