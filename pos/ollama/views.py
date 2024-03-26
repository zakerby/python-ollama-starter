from flask import Blueprint, request
from llama_index.llms.ollama import Ollama

import ollama

ollama_view = Blueprint('ollama_view', __name__, url_prefix='/ollama')

ollama_instance = Ollama(host='localhost', port=11434)


@ollama_view.route('/available-models')
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
