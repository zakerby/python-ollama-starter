from flask import Blueprint, request

from llama_index.legacy import VectorStoreIndex, ServiceContext, SimpleDirectoryReader
from llama_index.legacy.vector_stores.qdrant import QdrantVectorStore
from llama_index.legacy.storage import StorageContext


from pos.extensions import list_ollama_model
from pos.extensions import create_ollama_model
from pos.extensions import ollama_model_exists
from pos.extensions import query_ollama_model
from pos.extensions import get_ollama_instance

from pos.extensions import qdrant_db

ollama_view = Blueprint('ollama_view', __name__, url_prefix='/ollama')


@ollama_view.route('/available-models')
def get_models():
    return list_ollama_model()


@ollama_view.route('/create-model', methods=['POST'])
def create_model():
    data = request.get_json()
    base_model_name = data["base_model_name"]
    model_name = data["model_name"]
    model_description = data["model_description"]
    # first we need to check if the model model_name already exists
    if not ollama_model_exists(model_name):
        model = create_ollama_model(base_model_name,
                                    model_name,
                                    model_description)
        return model
    else:
        return {"message": "Model already exists"}, 400


@ollama_view.route('/query-model', methods=['POST'])
def query_model():
    data = request.get_json()
    model_name = data["model_name"]
    query = data["query"]
    if ollama_model_exists(model_name):
        response = query_ollama_model(model_name, query)
        return response
    else:
        return {"message": "Model does not exist, create it first before querying it"}, 400
    
    
@ollama_view.route('/query-specialized-model', methods=['POST'])
def query_specialized_model():
    data = request.get_json()
    model_name = data["model_name"]
    query = data["query"]
    
    if ollama_model_exists(model_name):
        documents = SimpleDirectoryReader("./data").load_data()        
        vector_store = QdrantVectorStore(client=qdrant_db, collection_name="test")
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
    else:
        return {"message": "Model does not exist, create it first before querying it"}, 400