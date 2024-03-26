
# Python Ollama Starter

A simple Flask app customized to work with LLM models using Ollama


## Run Locally

Clone the project

```bash
  git clone https://github.com/zakerby/python-ollama-starter my-project
```

Go to the project directory

```bash
  cd my-project
```

Run Docker Compose

```bash
  docker-compose up -d
```


## Endpoints test

To get available models
```bash
curl http://127.0.0.1:5000/ollama/available-models 
```


To create a new model

```bash
curl -X POST http://127.0.0.1:5000/ollama/create-model -H 'Content-Type: application/json' -d '{"model_name":"test", "base_model_name": "gemma:2b", "model_description": "I am a gardener, act as an helpful gardener for the users"}'    
```

To query an existing model

```bash
curl -X POST http://127.0.0.1:5000/ollama/query-model -H 'Content-Type: application/json' -d '{"model_name":"test", "query": "How are you?"}'
```



## Roadmap

- Add training model support

- Add API key login mgmt

