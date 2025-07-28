import os
import json
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Base URL for the Maximo API
MAXIMO_API_URL = os.environ.get("MAXIMO_API_URL")

# API Key for authentication
API_KEY = os.environ.get("MAXIMO_API_KEY")

def get_asset(asset_id: str, lean: int = None, ignorecollectionref: int = None):
    """
    Retrieves details of a specific asset by its ID.
    """
    headers = {
        "apikey": API_KEY,
        "Accept": "application/json"
    }
    params = {}
    if lean is not None:
        params["lean"] = lean
    if ignorecollectionref is not None:
        params["ignorecollectionref"] = ignorecollectionref
    response = requests.get(f"{MAXIMO_API_URL}/os/mxasset/{asset_id}?lean=1&ignorecollectionref=1", headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def list_assets(page_size: int = 10, page_num: int = 1, where: str = None, lean: int = None, ignorecollectionref: int = None):
    """
    Lists all assets, with optional filtering and pagination.
    """
    headers = {
        "apikey": API_KEY,
        "Accept": "application/json"
    }
    params = {
        "oslc.select": "assetnum,siteid,status,location,description",
        "pageno": page_num,
        "oslc.pageSize": page_size,
    }
    if where:
        params["oslc.where"] = where

    response = requests.get(f"{MAXIMO_API_URL}/os/mxasset?lean=1&ignorecollectionref=1&", headers=headers, params=params)
    response.raise_for_status()
    return response.json()

@app.route('/tools/get_asset/<string:asset_id>', methods=['GET'])
def get_asset_tool(asset_id: str):
    lean = request.args.get('lean', type=int)
    ignorecollectionref = request.args.get('ignorecollectionref', type=int)
    try:
        result = get_asset(asset_id, lean, ignorecollectionref)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tools/list_assets', methods=['GET'])
def list_assets_tool():
    page_size = request.args.get('page_size', 10, type=int)
    page_num = request.args.get('page_num', 1, type=int)
    where = request.args.get('oslc.where')
    lean = request.args.get('lean', type=int)
    ignorecollectionref = request.args.get('ignorecollectionref', type=int)
    try:
        result = list_assets(page_size, page_num, where, lean, ignorecollectionref)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tools', methods=['GET'])
def get_tools():
    with open('manifest.json', 'r') as f:
        manifest = f.read()
    return jsonify(json.loads(manifest))

if __name__ == '__main__':
    app.run(port=5001)
