# search_tools.py

from duckduckgo_search import DDGS
import wikipedia
import arxiv
import re
import os

class WebSearchTool:
    """Tool for performing real-time web search using DuckDuckGo."""
    @staticmethod
    def search(query, num_results=5):
        results = []
        try:
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=num_results):
                    results.append({
                        "title": r.get("title", ""),
                        "snippet": r.get("body", ""),
                        "url": r.get("href", "")
                    })
        except Exception as e:
            results.append({
                "title": "Error",
                "snippet": f"Web search failed: {e}",
                "url": ""
            })
        return results

class WikipediaTool:
    """Tool for extracting summaries from Wikipedia."""
    @staticmethod
    def search(query, sentences=3):
        results = []
        try:
            summary = wikipedia.summary(query, sentences=sentences, auto_suggest=True)
            page = wikipedia.page(query, auto_suggest=True)
            results.append({
                "title": page.title,
                "snippet": summary,
                "url": page.url
            })
        except Exception as e:
            results.append({
                "title": "Wikipedia Error",
                "snippet": f"Wikipedia lookup failed: {e}",
                "url": ""
            })
        return results

class ArxivSearchTool:
    """Tool for searching academic papers on arXiv and downloading PDFs."""
    
    @staticmethod
    def search(query, max_results=3):
        results = []
        try:
            search = arxiv.Search(query=query, max_results=max_results)
            for res in search.results():
                results.append({
                    "title": res.title,
                    "snippet": res.summary,
                    "url": res.entry_id,      # e.g., 'https://arxiv.org/abs/2208.00733v1'
                    "arxiv_id": ArxivSearchTool._extract_arxiv_id(res.entry_id)
                })
        except Exception as e:
            results.append({
                "title": "arXiv Error",
                "snippet": f"arXiv search failed: {e}",
                "url": "",
                "arxiv_id": ""
            })
        return results

    @staticmethod
    def _extract_arxiv_id(url):
        """Extracts the arXiv ID from the abs URL."""
        match = re.search(r'arxiv\.org\/abs\/([\w\.\-\/]+)', url)
        print(match)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def download_pdf(arxiv_id, paper_title,dirpath="data/arxiv/files", filename=None):
        """
        Downloads the PDF by arXiv ID to the specified location and filename.
        Auto-creates the directory if missing.
        """
        try:
            os.makedirs(dirpath, exist_ok=True)  # Ensure the folder exists!
            client = arxiv.Client()
            search = arxiv.Search(id_list=[arxiv_id])
            paper = next(client.results(search))
            if not filename:
                # Default: use arxiv_id.pdf
                filename = f"{arxiv_id.replace('/', '_')}({paper_title}).pdf"
            full_path = os.path.join(dirpath, filename)
            paper.download_pdf(dirpath=dirpath, filename=filename)
            return full_path
        except Exception as e:
            return f"PDF download failed: {e}"

