from llama_index.llms.ollama import Ollama
from llama_index.core.query_engine import RetrieverQueryEngine
import ollama

from pos.extensions.vector_store import get_vector_store
from pos.extensions.rag import VectorDBRetriever
from pos.extensions.llm import get_llm

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
    vector_store = get_vector_store()
    llm = get_llm()
    retriever = VectorDBRetriever(vector_store, llm)
    query_engine = RetrieverQueryEngine.from_args(retriever, llm=llm)
    response = query_engine.query(query)
    print(response)
    return response


def get_ollama_instance(model_name: str):
    return Ollama(host='localhost', port=11434, model=model_name)
