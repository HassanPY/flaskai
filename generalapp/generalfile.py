from flask import Blueprint, render_template

general_bp = Blueprint('general_bp', __name__)


@general_bp.route('/')
def home():
    return "its me ... Home Page"
