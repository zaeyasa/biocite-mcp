"""Metadata fetching utilities for BioCite-MCP."""

import requests
from typing import Dict, Any, Optional

def fetch_metadata(doi: str) -> Optional[Dict[str, Any]]:
    """Fetch metadata from Crossref with Europe PMC fallback."""
    # 1. Try Crossref
    metadata = _fetch_from_crossref(doi)
    if not metadata:
        metadata = _fetch_from_europepmc(doi)
    return metadata

def _fetch_from_crossref(doi: str) -> Optional[Dict[str, Any]]:
    """Fetch metadata from Crossref API."""
    url = f"https://api.crossref.org/works/{doi}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None
            
        item = response.json().get("message", {})
        
        # Extract authors
        author_list = item.get("author", [])
        raw_authors = []
        if author_list:
            for a in author_list:
                family = a.get("family", "")
                given = a.get("given", "")
                raw_authors.append({"first": given, "last": family})

        formatted_authors = []
        for a in raw_authors:
            if a["first"] and a["last"]:
                formatted_authors.append(f"{a['last']}, {a['first'][0]}.")
            elif a["last"]:
                formatted_authors.append(a["last"])
        authors_str = ", ".join(formatted_authors)

        # Extract year
        pub_date = item.get("published-print") or item.get("published-online") or item.get("issued")
        year = "N/A"
        if pub_date and pub_date.get("date-parts"):
            year = str(pub_date["date-parts"][0][0])

        return {
            "authors": authors_str,
            "raw_authors": raw_authors,
            "year": year,
            "title": item.get("title", ["N/A"])[0],
            "journal": item.get("container-title", ["N/A"])[0],
            "volume": item.get("volume", ""),
            "issue": item.get("issue", ""),
            "pages": item.get("page", ""),
            "doi": doi
        }
    except:
        return None

def _fetch_from_europepmc(doi: str) -> Optional[Dict[str, Any]]:
    """Fetch metadata from Europe PMC API as a fallback."""
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {"query": f'DOI:"{doi}"', "format": "json", "resultType": "core"}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return None
            
        results = response.json().get("resultList", {}).get("result", [])
        if not results:
            return None
            
        res = results[0]
        
        # Extract authors for Zotero compatibility
        author_list = res.get("authorList", {}).get("author", [])
        raw_authors = []
        for a in author_list:
            raw_authors.append({
                "first": a.get("firstName", ""),
                "last": a.get("lastName", "")
            })

        return {
            "authors": res.get("authorString", "N/A"),
            "raw_authors": raw_authors,
            "year": res.get("pubYear", "N/A"),
            "title": res.get("title", "N/A"),
            "journal": res.get("journalTitle", "N/A"),
            "volume": res.get("volume", ""),
            "issue": res.get("issue", ""),
            "pages": res.get("pageInfo", ""),
            "doi": doi
        }
    except:
        return None
