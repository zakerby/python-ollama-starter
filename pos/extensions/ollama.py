from llama_index.llms.ollama import Ollama
import ollama

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


def get_ollama_instance(model_name: str):
    return Ollama(host='localhost', port=11434, model=model_name)
