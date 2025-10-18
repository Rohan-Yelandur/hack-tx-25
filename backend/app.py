from flask import Flask
from flask_cors import CORS
from api_routes import register_routes
from settings import settings

app = Flask(__name__)
CORS(app)

# Register routes
register_routes(app)


if __name__ == "__main__":
    app.run(port=settings.PORT, debug=settings.DEBUG)