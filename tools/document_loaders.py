# tools/document_loaders.py

from langchain.document_loaders import PyPDFLoader

class PdfDocumentLoader:
    @staticmethod
    def load_documents(path):
        """
        Loads one or multiple PDFs and returns a list of LangChain Document objects.
        Accepts a single path (str) or a list of paths.
        Handles errors gracefully.
        """
        docs = []
        if isinstance(path, str):
            paths = [path]
        else:
            paths = path
        for p in paths:
            try:
                pdocs = PyPDFLoader(p).load()
                docs.extend(pdocs)
            except Exception as e:
                print(f"Error loading PDF {p}: {e}")
        return docs
