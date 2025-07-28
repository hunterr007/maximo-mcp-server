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

## How to Use the Tools

You can use a tool like `curl` to interact with the server.

### Get Asset

To get the details of a specific asset, you need to send a `GET` request to the `/tools/get_asset/<asset_id>` endpoint, where `<asset_id>` is the ID of the asset you want to retrieve.

```bash
curl http://127.0.0.1:5001/tools/get_asset/YOUR_ASSET_ID
```

### List Assets

To list assets, you can send a `POST` request to the `/tools/list_assets` endpoint. You can also provide optional parameters for pagination and filtering.

**Basic List:**
```bash
curl -X POST http://127.0.0.1:5001/tools/list_assets
```

**With Pagination:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"page_size": 5, "page_num": 2}' http://127.0.0.1:5001/tools/list_assets
```

**With Filtering:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"where": "status=\\\"OPERATING\\\""}' http://127.0.0.1:5001/tools/list_assets
```
