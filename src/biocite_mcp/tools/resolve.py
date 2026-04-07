"""DOI resolution tool for BioCite-MCP."""

import re
from typing import Dict, Any
from ..utils.formatting import format_apa, format_nature
from ..utils.metadata import fetch_metadata

DOI_REGEX = r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$"

def resolve_citation(doi: str, style: str = "apa") -> Dict[str, Any]:
    """Convert a known DOI into a formatted, publication-ready citation string."""
    
    # 1. Validate DOI format
    if not re.match(DOI_REGEX, doi, re.IGNORECASE):
        return {
            "error": True,
            "message": "Invalid DOI format",
            "code": "INVALID_INPUT",
            "next_tool_hint": None
        }

    # 2. Fetch metadata using centralized utility
    metadata = fetch_metadata(doi)
        
    if not metadata:
        return {
            "error": True,
            "message": f"DOI {doi} could not be resolved in Crossref or Europe PMC",
            "code": "NOT_FOUND",
            "next_tool_hint": None
        }

    # 3. Format citation
    if style.lower() == "nature":
        citation = format_nature(metadata)
    else:
        citation = format_apa(metadata)

    return {
        "doi": doi,
        "style": style.lower(),
        "citation": citation,
        "title": metadata.get("title", "N/A"),
        "authors": metadata.get("authors", "N/A"),
        "next_tool_hint": {
            "tool": "search_literature",
            "reason": "Use search_literature to find related papers on the same topic for a more comprehensive reference list."
        }
    }
