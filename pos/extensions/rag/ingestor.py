from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.readers.file import PyMuPDFReader
from llama_index.core.schema import TextNode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from typing import List


class VectorDBIngestor:
    """Ingestor of PDF documents over a postgres vector store."""

    def __init__(
        self,
        vector_store: PGVectorStore,
        embed_model: HuggingFaceEmbedding = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en"
        ),
    ) -> None:
        """Init params."""
        self._vector_store = vector_store
        self._text_parser = SentenceSplitter(
            chunk_size=1024,
            # separator=" ",
        )
        self._loader = PyMuPDFReader()
        self._embed_model = embed_model

    def process_document(self, document_path: str) -> None:
        documents = self._loader.load(file_path=document_path)

        text_chunks = []
        # maintain relationship with source doc index, to help inject doc metadata in (3)
        doc_idxs = []
        for doc_idx, doc in enumerate(documents):
            cur_text_chunks = self._text_parser.split_text(doc.text)
            text_chunks.extend(cur_text_chunks)
            doc_idxs.extend([doc_idx] * len(cur_text_chunks))

        nodes = []
        for idx, text_chunk in enumerate(text_chunks):
            node = TextNode(
                text=text_chunk,
            )
            src_doc = documents[doc_idxs[idx]]
            node.metadata = src_doc.metadata
            nodes.append(node)
        self.ingest_batch(nodes)

    def ingest(self, node: TextNode) -> None:
        """Ingest."""
        node_embedding = self._embed_model.get_text_embedding(
            node.get_content(metadata_mode="all")
        )
        node.embedding = node_embedding
        self._vector_store.add([node])

    def ingest_batch(self, nodes: List[TextNode]) -> None:
        """Ingest batch"""
        for node in nodes:
            node_embedding = self._embed_model.get_text_embedding(
                node.get_content(metadata_mode="all")
            )
            node.embedding = node_embedding
        self._vector_store.add(nodes)
