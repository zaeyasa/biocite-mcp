"""BibTeX export tool for BioCite-MCP."""

import requests
from typing import Dict, Any

def export_bibtex(doi: str) -> Dict[str, Any]:
    """Retrieve the BibTeX citation for a given DOI using Crossref content negotiation.
    
    Args:
        doi: The DOI of the paper to export.
    """
    # Crossref supports content negotiation via Accept header
    url = f"https://doi.org/{doi}"
    headers = {"Accept": "application/x-bibtex"}
    
    try:
        # Crossref redirects to its metadata service
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        if response.status_code != 200:
            return {
                "error": True,
                "message": f"Failed to retrieve BibTeX from Crossref (Status: {response.status_code})",
                "code": "HTTP_ERROR"
            }
            
        bibtex_string = response.text.strip()
        
        if not bibtex_string or "@" not in bibtex_string:
            return {
                "error": True,
                "message": "Invalid BibTeX response received from Crossref",
                "code": "INTERNAL_ERROR"
            }
            
        return {
            "doi": doi,
            "bibtex": bibtex_string,
            "next_tool_hint": None
        }
        
    except requests.exceptions.Timeout:
        return {
            "error": True,
            "message": "DOI resolver timed out (10s)",
            "code": "TIMEOUT"
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"An unexpected error occurred: {str(e)}",
            "code": "INTERNAL_ERROR"
        }
