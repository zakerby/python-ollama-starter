from flask import Blueprint, request

from pos.extensions import list_ollama_model
from pos.extensions import create_ollama_model
from pos.extensions import ollama_model_exists
from pos.extensions import query_ollama_model
from pos.extensions import rag_query_llm_model


ollama_view = Blueprint("ollama_view", __name__, url_prefix="/ollama")


@ollama_view.route("/available-models")
def get_models():
    return list_ollama_model()


@ollama_view.route("/create-model", methods=["POST"])
def create_model():
    data = request.get_json()
    base_model_name = data["base_model_name"]
    model_name = data["model_name"]
    model_description = data["model_description"]
    # first we need to check if the model model_name already exists
    if not ollama_model_exists(model_name):
        model = create_ollama_model(base_model_name, model_name, model_description)
        return model
    else:
        return {"message": "Model already exists"}, 400


@ollama_view.route("/query-model", methods=["POST"])
def query_model():
    data = request.get_json()
    model_name = data["model_name"]
    query = data["query"]
    if ollama_model_exists(model_name):
        response = query_ollama_model(model_name, query)
        return response
    else:
        return {
            "message": "Model does not exist, create it first before querying it"
        }, 400


@ollama_view.route("/query-specialized-model", methods=["POST"])
def query_specialized_model():
    data = request.get_json()
    model_name = data["model_name"]
    query = data["query"]
    collection_name = data["collection_name"]

    response = rag_query_llm_model(model_name, collection_name, query)

    return {"response": response}, 200
