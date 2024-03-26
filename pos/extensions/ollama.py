from llama_index.llms.ollama import Ollama
from llama_index.legacy import VectorStoreIndex, ServiceContext, SimpleDirectoryReader
from llama_index.legacy.vector_stores.qdrant import QdrantVectorStore
from llama_index.legacy.storage import StorageContext
import ollama

from pos.extensions import qdrant_db


ollama_client = ollama.Client(host='http://localhost:11434')


def list_ollama_model():
    models = ollama_client.list()
    return models


def ollama_model_exists(model_name: str):
    model = ollama_client.show(model_name)
    return model is not None


def create_ollama_model(base_model_name: str,
                        model_name: str,
                        model_description: str):
    model_file = f"""FROM {base_model_name}
                    SYSTEM \"\"\"
                        {model_description}
                    \"\"\"
                """
    model = ollama_client.create(model=model_name, modelfile=model_file)
    return model


def query_ollama_model(model_name: str, query: str):
    resp = ollama_client.generate(model=model_name, prompt=query)
    return resp.get('response')


def rag_query_ollama_model(model_name: str, collection_name: str, query: str):
    documents = SimpleDirectoryReader("./data").load_data()        
    vector_store = QdrantVectorStore(
        client=qdrant_db,
        collection_name=collection_name)
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store)

    ollama_model = get_ollama_instance(model_name)
    service_context = ServiceContext.from_defaults(
        llm=ollama_model,
        embed_model='local')
    
    idx = VectorStoreIndex.from_documents(
        documents,
        service_context=service_context,
        storage_context=storage_context)
    query_engine = idx.as_query_engine()
    response = query_engine.query(query)
    return response


def get_ollama_instance(model_name: str):
    return Ollama(host='localhost', port=11434, model=model_name)
