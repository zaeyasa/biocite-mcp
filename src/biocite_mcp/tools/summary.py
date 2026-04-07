"""Paper summarization tool for BioCite-MCP."""

import requests
from typing import Dict, Any

def summarize_paper(doi: str) -> Dict[str, Any]:
    """Fetch a paper's abstract and prepare it for host LLM summarization.
    
    Args:
        doi: The DOI of the paper to summarize.
    """
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {
        "query": f"DOI:{doi}",
        "format": "json",
        "resultType": "core"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            return {
                "error": True,
                "message": f"Europe PMC API returned status code {response.status_code}",
                "code": "HTTP_ERROR"
            }
            
        data = response.json()
        results = data.get("resultList", {}).get("result", [])
        
        if not results:
            return {
                "error": True,
                "message": f"Abstract for DOI {doi} not found",
                "code": "NOT_FOUND"
            }
            
        res = results[0]
        abstract = res.get("abstractText", "No abstract available.")
        title = res.get("title", "N/A")
        authors = res.get("authorString", "N/A")
        journal = res.get("journalTitle", "N/A")
        year = res.get("pubYear", "N/A")
        
        return {
            "doi": doi,
            "title": title,
            "authors": authors,
            "journal": journal,
            "year": year,
            "abstract_content": abstract,
            "instructions": (
                "Please provide a concise, academic summary of the abstract above. "
                "Highlight the core objectives, methodology, key findings, and biological significance."
            )
        }
        
    except requests.exceptions.Timeout:
        return {
            "error": True,
            "message": "Europe PMC API timed out",
            "code": "TIMEOUT"
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"An unexpected error occurred: {str(e)}",
            "code": "INTERNAL_ERROR"
        }
