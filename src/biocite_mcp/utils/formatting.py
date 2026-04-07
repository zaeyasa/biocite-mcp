"""Citation formatting utilities for BioCite-MCP."""

from typing import Dict, Any, List

def format_apa(metadata: Dict[str, Any]) -> str:
    """Format citation metadata in APA style.
    
    Expected keys: authors, year, title, journal, volume, issue, pages, doi
    """
    authors = metadata.get("authors", "N/A")
    year = metadata.get("year", "N/A")
    title = metadata.get("title", "N/A")
    journal = metadata.get("journal", "N/A")
    volume = metadata.get("volume", "")
    issue = metadata.get("issue", "")
    pages = metadata.get("pages", "")
    doi = metadata.get("doi", "")

    # Handle volume/issue formatting
    vol_iss = ""
    if volume and issue:
        vol_iss = f"{volume}({issue})"
    elif volume:
        vol_iss = volume
    
    citation = f"{authors} ({year}). {title}. {journal}"
    if vol_iss:
        citation += f", {vol_iss}"
    if pages:
        citation += f", {pages}"
    if doi:
        citation += f". https://doi.org/{doi}"
    
    return citation

def format_nature(metadata: Dict[str, Any]) -> str:
    """Format citation metadata in Nature style.
    
    Expected keys: authors, title, journal, volume, pages, year
    """
    authors = metadata.get("authors", "N/A")
    title = metadata.get("title", "N/A")
    journal = metadata.get("journal", "N/A")
    volume = metadata.get("volume", "")
    pages = metadata.get("pages", "")
    year = metadata.get("year", "N/A")

    citation = f"{authors}. {title}. {journal}"
    if volume:
        citation += f" {volume}"
    if pages:
        citation += f", {pages}"
    citation += f" ({year})."
    
    return citation
