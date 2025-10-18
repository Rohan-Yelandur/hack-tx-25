"""Routes package for Flask endpoints."""

from flask import Blueprint

# Create blueprints
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Import routes to register them with blueprints
from . import solve_text, solve_pdf

__all__ = ['api_bp']

