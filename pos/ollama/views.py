from flask import Blueprint, request
import ollama

ollama_view = Blueprint('query_model', __name__, url_prefix='/ollama')


@ollama_view.route('/get-models')
def get_models():
    models = ollama.list()
    return models


@ollama_view.route('/create-model', methods=['POST']) 
def create_model():
    base_model_name = request["base_model_name"]
    model_name = request["model_name"]
    model_description = request["model_description"]
    
    # first we need to check if another model with the same name exists
    model_file = f"""
        FROM {base_model_name}
        SYSTEM {model_description}
    """
    model = ollama.create(model=model_name, 
                          model_file=model_file)    
    return model
