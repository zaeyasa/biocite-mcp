"""BioCite-MCP Server Entry Point."""

from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Any, Optional
from .tools.search import search_literature as search_logic, find_related_papers as related_logic
from .tools.resolve import resolve_citation as resolve_logic
from .tools.summary import summarize_paper as summary_logic
from .tools.deduplicate import detect_duplicates as dedup_logic
from .tools.export import export_bibtex as export_logic
from .tools.audit import audit_refs_in_text as audit_logic
from .tools.zotero import push_to_zotero as zotero_logic

# Initialize FastMCP server
mcp = FastMCP("BioCite-MCP")

@mcp.tool()
def search_literature(query: str, limit: int = 5) -> str:
    """Query Europe PMC to retrieve real, peer-reviewed papers matching a biological query.
    
    Args:
        query: Free-text search query (e.g., "DREB2A drought stress tomato")
        limit: Maximum number of results to return (1-25)
    """
    safe_limit = max(1, min(limit, 25))
    result = search_logic(query, safe_limit)
    return str(result)

@mcp.tool()
def resolve_citation(doi: str, style: str = "apa") -> str:
    """Convert a known DOI into a formatted, publication-ready citation string.
    
    Args:
        doi: A valid DOI string (e.g., 10.1093/jxb/erx393)
        style: Citation style: "apa" or "nature"
    """
    result = resolve_logic(doi, style)
    return str(result)

@mcp.tool()
def find_related_papers(doi: str, limit: int = 5) -> str:
    """Find semantically related papers based on a given DOI.
    
    Args:
        doi: The DOI of the source paper.
        limit: Maximum number of related papers to return (1-10)
    """
    safe_limit = max(1, min(limit, 10))
    result = related_logic(doi, safe_limit)
    return str(result)

@mcp.tool()
def summarize_paper(doi: str) -> str:
    """Fetch a paper's abstract and metadata for the LLM to summarize.
    
    Args:
        doi: The DOI of the paper to summarize.
    """
    result = summary_logic(doi)
    return str(result)

@mcp.tool()
def check_duplicate_citations(papers_json: str, threshold: int = 90) -> str:
    """Identify duplicate papers in a list based on DOI and Title similarity.
    
    Args:
        papers_json: A JSON string containing a list of paper objects with 'title' and optional 'doi'.
        threshold: Similarity threshold (0-100) for title matching.
    """
    import json
    try:
        papers = json.loads(papers_json)
        if not isinstance(papers, list):
            return str({"error": True, "message": "Input must be a JSON array of papers"})
        result = dedup_logic(papers, threshold)
        return str(result)
    except Exception as e:
        return str({"error": True, "message": f"Invalid JSON input: {str(e)}"})

@mcp.tool()
def export_bibtex(doi: str) -> str:
    """Retrieve the BibTeX citation for a given DOI.
    
    Args:
        doi: The DOI of the paper to export.
    """
    result = export_logic(doi)
    return str(result)

@mcp.tool()
def audit_manuscript(text: str) -> str:
    """Scan a text for DOIs and citations, validating them and identifying missing DOIs.
    
    Args:
        text: The manuscript text (markdown, txt, etc.) to audit.
    """
    result = audit_logic(text)
    return str(result)

@mcp.tool()
def push_to_zotero(doi: str, zotero_key: str, library_id: str, library_type: str = "user", collection_id: Optional[str] = None) -> str:
    """Push a paper's metadata to a Zotero library.
    
    Args:
        doi: The DOI of the paper to add.
        zotero_key: Your Zotero API Key (Secret).
        library_id: Your Zotero User ID or Group ID.
        library_type: "user" or "group".
        collection_id: (Optional) ID of the collection to add the paper to.
    """
    result = zotero_logic(doi, zotero_key, library_id, library_type, collection_id)
    return str(result)

def main():
    """Main entry point for the server."""
    mcp.run()

if __name__ == "__main__":
    main()
