# ChatGPT Plugin: TODO List

This repository contains a simple ChatGPT plugin for managing a TODO list. The project derives from the code found in [OpenAI API plugin examples](https://platform.openai.com/docs/plugins/examples) and adds a few important improvements:

* Valid OpenAPI specification
* Ability to choose between three plugin authentication methods: `"none"`, `"service_http"` and `"user_http"`
* Support for HTTP for local deployments.

## Quick Start

1. Install Python 3.9, if not already installed.
2. Clone this repository.
3. Navigate to the cloned repository directory: `cd chatgpt-todo-plugin`
4. Create a new virtual environment: `python3 -m venv ./venv`
5. Activate the virtual environment: `source ./venv/bin/activate`
6. Install project requirements: `pip3 install -r requirements.txt`
7. Edit `main.py` and set the authentication constants to your desired values:
```
_PLUGIN_AUTH_TYPE = AUTH_TYPE_NONE
# Auth token for "service_http" or "user_http" authentication
_AUTH_KEY = "REPLACE_ME"
# OpenAI verification token for "service_http" authentication
_OPENAI_VERIFICATION_TOKEN = "REPLACE_ME"
```
8. Run the plugin locally: `python3 main.py`
9. The API will be available at `http://localhost:5002`.

## Example Requests

The request below will add a new item to the global TODO, without authentication.

```
curl -X POST http://0.0.0.0:5002/todos/global \
  -H 'Content-Type: application/json' \
  -d '{"todo": "Wash the car"}'
```

Add the bearer token for the `"service_http"` and `"user_http"` auth methods:

```
curl -X POST http://0.0.0.0:5002/todos/global \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer REPLACE_ME' \
  -d '{"todo": "Wash the car"}'
```

See the plugin's OpenAPI specification in `openapi.yaml` for the other available methods.
