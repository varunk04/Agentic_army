from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

class ChromaVectorStoreManager:
    def __init__(self, persist_directory="chroma_storage", model_name="all-MiniLM-L6-v2"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)

    def build_vector_store(self, chunks, metadata=None):
        # chunks: list of strings (your chunked text)
        # metadata: optional list of dicts (one per chunk)
        if metadata is None:
            # Chroma can still store w/o metadata, but source traceability is best practice
            metadata = [{}] * len(chunks)
        return Chroma.from_texts(
            texts=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            metadatas=metadata
        )

    def load_vector_store(self):
        # To retrieve without re-embedding each time
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

    def retrieve_chunks(self, query, vector_store, top_k=5):
        # Returns list of Documents (with page_content + metadata)
        return vector_store.similarity_search(query, k=top_k)
