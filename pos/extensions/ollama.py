from llama_index.llms.ollama import Ollama
import ollama

ollama_instance = Ollama(host='localhost', port=11434, model='gemma:2b')

ollama_client = ollama.Client(host='http://localhost:11434')


def list_ollama_model():
    models = ollama_client.list()
    return models


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
