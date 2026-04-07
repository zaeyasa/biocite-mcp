<p align="center">
  <img src="logo.jpg" alt="BioCite-MCP Logo" width="300">
</p>

# BioCite-MCP 🧬

[![PyPI version](https://img.shields.io/pypi/v/biocite-mcp.svg)](https://pypi.org/project/biocite-mcp/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://pypi.org/project/biocite-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-fastmcp-blue.svg)](https://modelcontextprotocol.io)

**BioCite-MCP** is an advanced Model Context Protocol (MCP) server that acts as a real-time bridge between LLMs and academic literature databases (Europe PMC & Crossref). It eliminates citation hallucinations by forcing AI models to retrieve verified, peer-reviewed paper metadata and real DOIs directly within their workflow.

---

## 🌟 Key Features

### 🔍 Literature Discovery
- **`search_literature`**: Query Europe PMC for real biological papers. Returns structured metadata including DOIs and abstracts.
- **`find_related_papers`**: Discovers semantically related research using Europe PMC's Recommendations engine with an automated Citations/References fallback.

### 📝 Citation & Formatting
- **`resolve_citation`**: Converts any DOI into publication-ready citation strings (APA or Nature style).
- **`export_bibtex`**: Retrieves professional BibTeX entries directly via Crossref content negotiation.

### 🛡️ Manuscript Auditing & Support
- **`audit_manuscript`**: Scans your text for DOIs to verify them and flags potential citations that lack DOIs.
- **`summarize_paper`**: Fetches abstracts and prepares high-quality summarization prompts optimized for LLMs like Claude.
- **`check_duplicate_citations`**: Uses fuzzy matching (`rapidfuzz`) to identify and group duplicate research in your lists.

### 📚 Integration
- **`push_to_zotero`**: Seamlessly add verified papers to your Zotero library via the Web API.

---

## 🚀 Installation

```bash
pip install biocite-mcp
```
*Note: For development, use `pip install -e .` in the repository root.*

---

## 🔧 Configuration

Add `biocite-mcp` to your MCP host configuration (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "biocite-mcp": {
      "command": "python",
      "args": ["-m", "biocite_mcp"]
    }
  }
}
```

---

## 🛠️ Usage Examples

1. **Search**: "Find recent papers about DREB2A drought stress in tomato."
2. **Resolve**: "Format the citation for DOI 10.1093/jxb/erx393 in Nature style."
3. **Analyze**: "Audit this manuscript draft for citation accuracy: [Your Text Here]" (Alternatively, for analyzing a manuscript, you can use Claude’s “file_system” module to scan for citations in 'specific files you point to the LLM')
4. **Export**: "Give me the BibTeX for 10.1111/j.1365-313X.2006.02701.x"

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Developed by ZaEyAsa — Your Advanced Agentic Bio-Citation Assistant.**
