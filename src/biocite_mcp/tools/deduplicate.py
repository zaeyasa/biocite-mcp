"""Citation deduplication tool for BioCite-MCP."""

from typing import List, Dict, Any
from rapidfuzz import fuzz

def detect_duplicates(papers: List[Dict[str, Any]], threshold: int = 90) -> Dict[str, Any]:
    """Identify duplicate papers in a list based on DOI and Title similarity.
    
    Args:
        papers: List of paper objects (must contain 'title', may contain 'doi').
        threshold: Similarity score (0-100) above which titles are considered duplicates.
    """
    duplicates = []
    seen_indices = set()
    
    for i in range(len(papers)):
        if i in seen_indices:
            continue
            
        current_paper = papers[i]
        current_doi = str(current_paper.get("doi", "")).lower().strip()
        current_title = str(current_paper.get("title", "")).lower().strip()
        
        group = [current_paper]
        
        for j in range(i + 1, len(papers)):
            if j in seen_indices:
                continue
                
            other_paper = papers[j]
            other_doi = str(other_paper.get("doi", "")).lower().strip()
            other_title = str(other_paper.get("title", "")).lower().strip()
            
            is_duplicate = False
            
            # 1. DOI Match (Highest confidence)
            if current_doi and other_doi and current_doi == other_doi and current_doi != "n/a":
                is_duplicate = True
            
            # 2. Fuzzy Title Match
            if not is_duplicate and current_title and other_title:
                score = fuzz.token_sort_ratio(current_title, other_title)
                if score >= threshold:
                    is_duplicate = True
            
            if is_duplicate:
                group.append(other_paper)
                seen_indices.add(j)
        
        if len(group) > 1:
            duplicates.append({
                "count": len(group),
                "papers": group,
                "reason": "DOI match" if (current_doi and group[1].get("doi") == current_doi) else f"Title similarity >= {threshold}%"
            })
            seen_indices.add(i)

    return {
        "original_count": len(papers),
        "duplicate_groups_found": len(duplicates),
        "duplicates": duplicates,
        "next_tool_hint": {
            "tool": "resolve_citation",
            "reason": "Once duplicates are removed, use resolve_citation to get clean, formatted strings for your final selection."
        }
    }
