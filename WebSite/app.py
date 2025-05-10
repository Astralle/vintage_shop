from flask import Flask
from routes import register_routes
import os

# Setup Flask app
app = Flask(
    __name__,
    template_folder="public/html",
    static_folder="public/static",
    static_url_path="/static"
)

# Register routes from routes.py
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
