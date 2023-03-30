import json

import quart
import quart_cors
from quart import request

# Note: Setting CORS to allow chat.openapi.com is required for ChatGPT to access your plugin
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

AUTH_TYPE_NONE = "none"
AUTH_TYPE_SERVICE_HTTP = "service_http"
AUTH_TYPE_USER_HTTP = "user_http"

_PLUGIN_AUTH_TYPE = AUTH_TYPE_NONE
# Auth token for "service_http" or "user_http" authentication
_AUTH_KEY = "REPLACE_ME"
# OpenAI verification token for "service_http" authentication
_OPENAI_VERIFICATION_TOKEN = "REPLACE_ME"
_TODOS = {}


def assert_auth_header(req):
    if _PLUGIN_AUTH_TYPE == "user_http":
        assert req.headers.get(
            "Authorization", None) == f"Bearer {_AUTH_KEY}"


@app.post("/todos/<string:username>")
async def add_todo(username):
    assert_auth_header(quart.request)
    request = await quart.request.get_json(force=True)
    if username not in _TODOS:
        _TODOS[username] = []
    _TODOS[username].append(request["todo"])
    return quart.Response(response='OK', status=200)


@app.get("/todos/<string:username>")
async def get_todos(username):
    assert_auth_header(quart.request)
    return quart.Response(response=json.dumps(_TODOS.get(username, [])), status=200)


@app.delete("/todos/<string:username>/<int:todo_idx>")
async def delete_todo(username, todo_idx):
    assert_auth_header(quart.request)
    if 0 <= todo_idx < len(_TODOS[username]):
        _TODOS[username].pop(todo_idx)
    return quart.Response(response='OK', status=200)


@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    proto = request.scheme
    host = request.headers['Host']
    with open("ai-plugin.json") as f:
        text = f.read()

        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the manifest
        text = text.replace("PLUGIN_HOSTNAME", f"{proto}://{host}")

        # Insert auth specification
        manifest = json.loads(text)
        manifest["auth"] = {
            "type": _PLUGIN_AUTH_TYPE
        }
        if _PLUGIN_AUTH_TYPE == AUTH_TYPE_SERVICE_HTTP or _PLUGIN_AUTH_TYPE == AUTH_TYPE_USER_HTTP:
            manifest["auth"]["authorization_type"] = "bearer"
            if _PLUGIN_AUTH_TYPE == AUTH_TYPE_SERVICE_HTTP:
                manifest["auth"]["verification_tokens"] = {
                    "openai": _OPENAI_VERIFICATION_TOKEN
                }
        text = json.dumps(manifest, indent=2)

        return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    proto = request.scheme
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the OpenAPI spec
        text = text.replace("PLUGIN_HOSTNAME", f"{proto}://{host}")
        return quart.Response(text, mimetype="text/yaml")


def main():
    app.run(debug=True, host="0.0.0.0", port=5002)


if __name__ == "__main__":
    main()