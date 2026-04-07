"""Zotero integration tool for BioCite-MCP."""

import requests
import json
from typing import Dict, Any, List
from ..utils.metadata import fetch_metadata

def push_to_zotero(doi: str, zotero_key: str, library_id: str, library_type: str = "user", collection_id: str = None) -> Dict[str, Any]:
    """Push a paper's metadata to a Zotero library.
    
    Args:
        doi: The DOI of the paper to add.
        zotero_key: Your Zotero API Key.
        library_id: Your Zotero User ID or Group ID.
        library_type: "user" or "group".
        collection_id: (Optional) ID of the collection to add the paper to.
    """
    # 1. Fetch Metadata
    metadata = fetch_metadata(doi)
    if not metadata:
        return {"error": True, "message": f"Could not fetch metadata for DOI {doi}", "code": "NOT_FOUND"}

    # 2. Format for Zotero
    # Format creators (authors)
    creators = []
    for raw_author in metadata.get("raw_authors", []):
        creators.append({
            "creatorType": "author",
            "firstName": raw_author.get("first", ""),
            "lastName": raw_author.get("last", "")
        })
    
    if not creators:
        creators = [{"creatorType": "author", "name": metadata.get("authors", "N/A")}]

    zotero_item = {
        "itemType": "journalArticle",
        "title": metadata.get("title", "N/A"),
        "creators": creators,
        "publicationTitle": metadata.get("journal", "N/A"),
        "volume": metadata.get("volume", ""),
        "issue": metadata.get("issue", ""),
        "pages": metadata.get("pages", ""),
        "date": metadata.get("year", "N/A"),
        "DOI": doi,
        "url": f"https://doi.org/{doi}"
    }
    
    if collection_id:
        zotero_item["collections"] = [collection_id]

    # 3. POST to Zotero
    base_url = f"https://api.zotero.org/{library_type}s/{library_id}/items"
    headers = {
        "Zotero-API-Key": zotero_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(base_url, headers=headers, json=[zotero_item], timeout=10)
        
        if response.status_code == 201: # Success: Created
            data = response.json()
            return {
                "success": True,
                "message": f"Paper successfully added to Zotero library {library_id}",
                "zotero_items_created": data.get("successful", {}),
                "next_tool_hint": None
            }
        else:
            return {
                "error": True,
                "message": f"Zotero API error: {response.text}",
                "code": "API_ERROR"
            }
            
    except Exception as e:
        return {
            "error": True,
            "message": f"An unexpected error occurred: {str(e)}",
            "code": "INTERNAL_ERROR"
        }
