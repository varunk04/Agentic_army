# tools/document_loaders.py

from langchain.document_loaders import PyPDFLoader
import re

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

    @staticmethod
    def chunk_documents(documents, chunk_size=1000, overlap=200):
        """
        Given a list of LangChain Document objects (from load_documents),
        returns a unified list of string chunks with overlap for retrieval or embedding.
        """
        def chunk_text(text, chunk_size, overlap):
            # Split text into sentences—handles context boundaries better
            sentences = re.split(r'(?<=[.!?]) +', text)
            chunks = []
            current = ""
            for sentence in sentences:
                if len(current) + len(sentence) < chunk_size:
                    current += sentence + " "
                else:
                    chunks.append(current.strip())
                    # Add overlap
                    current = current[-overlap:] + sentence + " " if overlap > 0 else sentence + " "
            if current:
                chunks.append(current.strip())
            return chunks

        all_chunks = []
        for doc in documents:
            text = getattr(doc, "page_content", str(doc))
            all_chunks.extend(chunk_text(text, chunk_size, overlap))
        return all_chunks
