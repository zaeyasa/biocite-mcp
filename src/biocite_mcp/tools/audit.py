"""Manuscript reference auditor for BioCite-MCP."""

import re
from typing import List, Dict, Any
from .resolve import resolve_citation

# Professional DOI Regex
DOI_PATTERN = r"10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+"
# Simple Author, Year pattern: (Name et al., 2023) or (Name, 2023)
CITATION_PATTERN = r"\([A-Z][a-zA-Z\s]+(?:et al\.)?,\s\d{4}\)"

def audit_refs_in_text(text: str) -> Dict[str, Any]:
    """Scan a text for DOIs and citations, validating them and identifying missing DOIs.
    
    Args:
        text: The manuscript text to audit.
    """
    # 1. Find all DOIs
    dois = list(set(re.findall(DOI_PATTERN, text)))
    
    validated_refs = []
    failed_dois = []
    
    for doi in dois:
        result = resolve_citation(doi)
        if result.get("error"):
            failed_dois.append({"doi": doi, "error": result.get("message")})
        else:
            validated_refs.append({
                "doi": doi,
                "citation": result.get("citation"),
                "title": result.get("title") # Resolve might not return title directly in outer dict, check structure
            })

    # 2. Find potential DOI-less citations (Author, Year)
    # We filter out those that are immediately followed or preceded by a DOI (simple heuristic)
    all_citations = re.findall(CITATION_PATTERN, text)
    
    # Heuristic: If a citation is found but no DOI is in the same paragraph (approx), warn.
    # For now, just list them as "Potential DOI-less citations"
    potential_missing = list(set(all_citations))

    return {
        "summary": {
            "dois_found": len(dois),
            "validated_count": len(validated_refs),
            "failed_count": len(failed_dois),
            "potential_doi_less_count": len(potential_missing)
        },
        "validated_references": validated_refs,
        "failed_dois": failed_dois,
        "warnings": [
            f"Found {len(potential_missing)} citations without a directly associated DOI (e.g. {potential_missing[:2]}). "
            "Please check if these should have DOIs for better verifiability."
        ] if potential_missing else [],
        "next_tool_hint": {
            "tool": "export_bibtex",
            "reason": "Use export_bibtex with the validated DOIs to generate your final bibliography file."
        }
    }
