from flask import Blueprint, request

from pos.extensions import list_ollama_model, create_ollama_model

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
    model = create_ollama_model(base_model_name, model_name, model_description)
    
    return model
