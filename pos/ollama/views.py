from flask import Blueprint, request

from pos.extensions import list_ollama_model, create_ollama_model

ollama_view = Blueprint('ollama_view', __name__, url_prefix='/ollama')

@ollama_view.route('/available-models')
def get_models():
    return list_ollama_model()


@ollama_view.route('/create-model', methods=['POST'])
def create_model():
    base_model_name = request["base_model_name"]
    model_name = request["model_name"]
    model_description = request["model_description"]
    model = create_ollama_model(base_model_name, model_name, model_description)
    
    return model
