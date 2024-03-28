from llama_index.core import QueryBundle
from llama_index.core.schema import NodeWithScore
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.vector_stores import VectorStoreQuery
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from typing import Any, List, Optional

from llama_index.readers.file import PyMuPDFReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import TextNode

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")


class VectorDBIngestor:
    """Ingestor over a postgres vector store."""

    def __init__(self, vector_store: PGVectorStore) -> None:
        """Init params."""
        self._vector_store = vector_store
        self._text_parser = SentenceSplitter(
            chunk_size=1024,
            # separator=" ",
        )
    def process_document_batch(self, document_path: str) -> None:
        loader = PyMuPDFReader()
        documents = loader.load(file_path=document_path)
        
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
        node_embedding = embed_model.get_text_embedding(
            node.get_content(metadata_mode="all")
        )
        node.embedding = node_embedding
        self._vector_store.add([node])

    def ingest_batch(self, nodes: List[TextNode]) -> None:
        """Ingest batch"""
        for node in nodes:
            node_embedding = embed_model.get_text_embedding(
                node.get_content(metadata_mode="all")
            )
            node.embedding = node_embedding
        self._vector_store.add(nodes)




# TODO: Abstract it to manage differents vector stores
class VectorDBRetriever(BaseRetriever):
    """Retriever over a postgres vector store."""

    def __init__(
        self,
        vector_store: PGVectorStore,
        embed_model: Any,
        query_mode: str = "default",
        similarity_top_k: int = 2,
    ) -> None:
        """Init params."""
        self._vector_store = vector_store
        self._embed_model = embed_model
        self._query_mode = query_mode
        self._similarity_top_k = similarity_top_k
        super().__init__()

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """Retrieve."""
        query_embedding = embed_model.get_query_embedding(
            query_bundle.query_str
        )
        vector_store_query = VectorStoreQuery(
            query_embedding=query_embedding,
            similarity_top_k=self._similarity_top_k,
            mode=self._query_mode,
        )
        query_result = self._vector_store.query(vector_store_query)

        nodes_with_scores = []
        for index, node in enumerate(query_result.nodes):
            score: Optional[float] = None
            if query_result.similarities is not None:
                score = query_result.similarities[index]
            nodes_with_scores.append(NodeWithScore(node=node, score=score))

        return nodes_with_scores
