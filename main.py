import json

import quart
import quart_cors
from quart import request

# Note: Setting CORS to allow chat.openapi.com is required for ChatGPT to access your plugin
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# "none" and "user_http" are supported
_PLUGIN_AUTH_TYPE = "none"
_USER_AUTH_KEY = "REPLACE_ME"
_TODOS = {}


def assert_auth_header(req):
    if _PLUGIN_AUTH_TYPE == "user_http":
        assert req.headers.get(
            "Authorization", None) == f"Bearer {_USER_AUTH_KEY}"


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
        # This is a trick we do to populate the constants in the manifest
        text = text.replace("PLUGIN_AUTH_TYPE", _PLUGIN_AUTH_TYPE)
        text = text.replace("PLUGIN_HOSTNAME", f"{proto}://{host}")
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