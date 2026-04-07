"""Europe PMC literature search tool for BioCite-MCP."""

import requests
from typing import Dict, Any, List

def search_literature(query: str, limit: int = 5) -> Dict[str, Any]:
    """Query Europe PMC to retrieve real, peer-reviewed papers matching a biological query."""
    base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {
        "query": query,
        "format": "json",
        "resultType": "core",
        "pageSize": limit
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        
        if response.status_code != 200:
            return {
                "error": True,
                "message": f"Europe PMC API returned status code {response.status_code}",
                "code": "HTTP_ERROR",
                "next_tool_hint": None
            }
            
        data = response.json()
        results_list = data.get("resultList", {}).get("result", [])
        total_found = data.get("hitCount", 0)
        
        formatted_results = []
        for res in results_list:
            formatted_results.append({
                "title": res.get("title", "N/A"),
                "authors": res.get("authorString", "N/A"),
                "journal": res.get("journalTitle", "N/A"),
                "year": res.get("pubYear", "N/A"),
                "doi": res.get("doi", "N/A"),
                "abstract": res.get("abstractText", "N/A")
            })
            
        if not formatted_results:
            return {
                "query": query,
                "total_found": 0,
                "results": [],
                "message": "No results found for your query. Try broadly searching for gene names or species.",
                "next_tool_hint": None
            }
            
        return {
            "query": query,
            "total_found": total_found,
            "results": formatted_results,
            "next_tool_hint": {
                "tool": "resolve_citation",
                "reason": "Use resolve_citation with a DOI from these results to get a formatted citation string ready for manuscript insertion."
            }
        }
        
    except requests.exceptions.Timeout:
        return {
            "error": True,
            "message": "Europe PMC API timed out",
            "code": "TIMEOUT",
            "next_tool_hint": None
        }
    except requests.exceptions.ConnectionError:
        return {
            "error": True,
            "message": "Network unreachable",
            "code": "NETWORK_ERROR",
            "next_tool_hint": None
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"An unexpected error occurred: {str(e)}",
            "code": "INTERNAL_ERROR",
            "next_tool_hint": None
        }
def find_related_papers(doi: str, limit: int = 5) -> Dict[str, Any]:
    """Find related papers using Recommendations API with a Citations fallback."""
    # 1. Resolve DOI to Source and ID
    search_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    search_params = {"query": f'DOI:"{doi}"', "format": "json", "resultType": "lite"}
    
    try:
        search_res = requests.get(search_url, params=search_params, timeout=10)
        if search_res.status_code != 200:
            return {"error": True, "message": "Failed to resolve DOI metadata", "code": "HTTP_ERROR"}
            
        search_data = search_res.json()
        results = search_data.get("resultList", {}).get("result", [])
        if not results:
            return {"error": True, "message": f"DOI {doi} not found in Europe PMC", "code": "NOT_FOUND"}
            
        source = results[0].get("source")
        ext_id = results[0].get("id")
        
        # 2. Try Recommendations first
        rec_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{source}/{ext_id}/recommendations"
        rec_res = requests.get(rec_url, params={"format": "json", "pageSize": limit}, timeout=10)
        
        related_results = []
        if rec_res.status_code == 200:
            related_results = rec_res.json().get("resultList", {}).get("result", [])
            
        # 3. Fallback to Citations if no recommendations
        if not related_results:
            cite_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{source}/{ext_id}/citations"
            cite_res = requests.get(cite_url, params={"format": "json", "pageSize": limit}, timeout=10)
            if cite_res.status_code == 200:
                related_results = cite_res.json().get("citationList", {}).get("citation", [])

        # 4. Final fallback to References
        if not related_results:
            ref_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{source}/{ext_id}/references"
            ref_res = requests.get(ref_url, params={"format": "json", "pageSize": limit}, timeout=10)
            if ref_res.status_code == 200:
                related_results = ref_res.json().get("referenceList", {}).get("reference", [])

        if not related_results:
            return {
                "source_doi": doi,
                "results": [],
                "message": "No related papers (recommendations, citations, or references) found for this DOI.",
                "next_tool_hint": None
            }
            
        formatted_results = []
        for res in related_results:
            # Different endpoints use slightly different keys (e.g., 'title' vs 'titleText')
            formatted_results.append({
                "title": res.get("title") or res.get("titleText") or "N/A",
                "authors": res.get("authorString") or res.get("authorList", {}).get("author", [{}])[0].get("fullName") or "N/A",
                "journal": res.get("journalTitle") or res.get("journalAbbreviation") or "N/A",
                "year": res.get("pubYear") or res.get("year") or "N/A",
                "doi": res.get("doi") or "N/A",
                "abstract": res.get("abstractText", "N/A")
            })
            
        return {
            "source_doi": doi,
            "method": "recommendations" if rec_res.status_code == 200 and rec_res.json().get("resultList", {}).get("result") else "citations/references",
            "results": formatted_results,
            "next_tool_hint": {
                "tool": "resolve_citation",
                "reason": "Use resolve_citation with a DOI from these results to get a formatted citation string."
            }
        }
    except Exception as e:
        return {"error": True, "message": f"An unexpected error occurred: {str(e)}", "code": "INTERNAL_ERROR"}
    except Exception as e:
        return {"error": True, "message": f"An unexpected error occurred: {str(e)}", "code": "INTERNAL_ERROR"}
