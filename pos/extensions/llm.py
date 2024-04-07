from llama_index.llms.llama_cpp import LlamaCPP


DEFAULT_MODEL_URL = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q4_0.gguf"


def get_llm(model_url=DEFAULT_MODEL_URL) -> LlamaCPP:

    llm_model = LlamaCPP(
        # You can pass in the URL to a GGML model to download it automatically
        # optionally, you can set the path to a pre-downloaded model instead of model_url
        model_path="/home/zakerby/Projects/llm/python-ollama-starter/llm_models/gemma-2b.gguf",
        temperature=0.1,
        max_new_tokens=256,
        # llama2 has a context window of 4096 tokens,
        # but we set it lower to allow for some wiggle room
        context_window=3900,
        # kwargs to pass to __call__()
        generate_kwargs={},
        # kwargs to pass to __init__()
        # set to at least 1 to use GPU
        model_kwargs={"n_gpu_layers": 1},
        verbose=True,
    )
    return llm_model
