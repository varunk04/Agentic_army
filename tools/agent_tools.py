# agent_tools.py

from langchain.tools import Tool
from tools.search_tools import WebSearchTool, WikipediaTool, ArxivSearchTool
import os

def web_search_tool_func(query: str) -> str:
    results = WebSearchTool.search(query)
    txts = [f"Title: {r['title']}\nSnippet: {r['snippet']}\nURL: {r['url']}" for r in results]
    return '\n\n'.join(txts)

def wikipedia_tool_func(query: str) -> str:
    results = WikipediaTool.search(query)
    txts = [f"Title: {r['title']}\nSummary: {r['snippet']}\nURL: {r['url']}" for r in results]
    return '\n\n'.join(txts)

def arxiv_search_tool_func(query: str) -> str:
    results = ArxivSearchTool.search(query)
    txts = [f"Title: {r['title']}\nSummary: {r['snippet']}\nURL: {r['url']}" for r in results]
    return '\n\n'.join(txts)

# Optionally, you can add the download function as its own Tool too.
def arxiv_download_tool_func(query: str) -> str:
    if not isinstance(query, str) or "|" not in query:
        return "Error: arXivDownload expects a single string in the format 'arxiv_id|paper_title'."
    arxiv_id, paper_title = query.split('|', 1)
    full_path = ArxivSearchTool.download_pdf(arxiv_id, paper_title)
    if os.path.exists(full_path):
        return f"Downloaded to: {full_path}"
    else:
        return f"Download failed or file not found at: {full_path}"


# agent_tools.py - Updated tool descriptions

web_search = Tool(
    name="WebSearch",
    func=web_search_tool_func,
    description="Search the web for recent articles, industry reports, and current developments. "
                "Use this for: news, industry trends, recent breakthroughs, company announcements. "
                "Returns: title, snippet, and URL for each result."
)

wikipedia_search = Tool(
    name="WikipediaSearch",
    func=wikipedia_tool_func,
    description="Search Wikipedia for established concepts, definitions, and foundational knowledge. "
                "Use this for: background information, concept definitions, historical context. "
                "Returns: article title, summary, and Wikipedia URL."
)

arxiv_search = Tool(
    name="ArxivSearch",
    func=arxiv_search_tool_func,
    description="Search arXiv for academic papers and technical research. "
                "Use this for: peer-reviewed research, technical papers, scientific studies. "
                "Returns: paper title, abstract, arXiv URL, and complete arXiv ID with version."
)

arxiv_download = Tool(
    name="ArxivDownload",
    func=arxiv_download_tool_func,
    description="Download a single arXiv paper as PDF. "
                "Input format: 'complete_arxiv_id|paper_title' (e.g., '2506.01463v1|Paper Title'). "
                "CRITICAL: Always use the complete arXiv ID including version (v1, v2, etc.). "
                "Download papers individually - never attempt multiple downloads in one action."
)

